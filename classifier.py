from sklearn.naive_bayes import *
from sklearn.linear_model import *
from sklearn.mixture import *
from scipy.stats import mode
from tqdm import tqdm
import pandas as pd
import numpy as np

class BaseClassifier():
    def train(self, dataset):
        print('train', self, 'on', dataset)
        self.trainset = dataset # include the trainset so the images are processed correctly on testing
        self.labelset = sorted(dataset.label_set())

    def classify(self, data, preprocess=True):
        assert hasattr(self, 'trainset'), 'model not trained'
        if preprocess:
            for key in data:
                data[key] = self.trainset.preprocess(data[key])
        return 'unknown'

    def update(self, label):
        return 'not updated - method not implemented'

    def test(self, dataset, update=False):
        print('test', self, 'on', dataset)
        confusion_matrix = pd.DataFrame(np.zeros((len(self.labelset), len(self.labelset))))
        confusion_matrix.columns = self.labelset
        confusion_matrix.index = self.labelset
        n_correct = n_total = 0
        for image, correct_label in tqdm(dataset, desc='testing'):
            # since our dataset only has images from one angle per item, use it twice and pretend it's from two angles
            # no need to preprocess since images are already in right shape from the testset (assume it has the same config as trainset)
            predict_label = self.classify(dict(image_top=image, image_side=image), preprocess=False)
            if update:
                self.update(correct_label)
            confusion_matrix.iloc[
                self.labelset.index(correct_label),
                self.labelset.index(predict_label),
            ] += 1
            if correct_label == predict_label:
                n_correct += 1
            n_total += 1
        accuracy = n_correct / n_total if n_total > 0 else 0
        print('accuracy', accuracy)
        print('confusion matrix')
        print(confusion_matrix)
        return accuracy, confusion_matrix


class FeatureExtractorClassifier(BaseClassifier):
    def __init__(self, feature_extractor):
        self.f = feature_extractor
        self.item_vectors = []
        self.item_labels = []

    def __repr__(self):
        return f'FeatureExtractorClassifier({self.f})'

    def train_feature_vector(self, image):
        return self.f.extract(image[None])

    def feature_vector(self, data):
        return self.f.extract(np.stack([
            data['image_top'],
            data['image_side'],
        ]))

    def train(self, dataset):
        super().train(dataset)
        for image, label in tqdm(dataset, desc='extracting features'):
            self.item_vectors.append( self.train_feature_vector(image) )
            self.item_labels.append( label )


class KNNClassifier(FeatureExtractorClassifier):
    def __init__(self, feature_extractor, threshold=0.8, k=1):
        super().__init__(feature_extractor)
        self.t = threshold
        self.k = k

    def __repr__(self):
        return f'KNNClassifier({self.f}, threshold={self.t}, k={self.k})'

    def cossim(self, query_vector):
        item_vectors = np.stack(self.item_vectors, axis=0).astype(np.float)
        item_vectors /= 1e-9 + np.linalg.norm(item_vectors, axis=1, keepdims=1)
        N, D = item_vectors.shape
        query_vector = query_vector.astype(np.float)
        query_vector = query_vector.reshape(D, 1)
        query_vector /= 1e-9 + np.linalg.norm(query_vector)
        return (item_vectors @ query_vector).reshape(N)

    def classify(self, data, preprocess=True):
        super().classify(data, preprocess=preprocess)
        v = self.last_v = self.feature_vector(data)
        c = self.cossim(v)
        topk = c.argsort()[::-1][:self.k]
        topk_labels = [self.item_labels[i] for i in topk]
        #score = c[topk].min()
        #if score < self.t:
        #    return 'unknown'
        #else:
        return mode(topk_labels).mode[0]

    def update(self, label):
        self.item_vectors.append(self.last_v)
        self.item_labels.append(label)
        return 'updated'


class SklearnClassifier(FeatureExtractorClassifier):
    def __init__(self, feature_extractor, sklearn_classifier):
        super().__init__(feature_extractor)
        self.l = sklearn_classifier

    def __repr__(self):
        return f'SklearnClassifier({self.f}, {self.l})'

    def train(self, dataset):
        super().train(dataset)
        X = self.item_vectors
        y = [self.labelset.index(l) for l in self.item_labels]
        print('fitting sklearn model...')
        self.l.fit(X, y)

    def classify(self, data, preprocess=True):
        super().classify(data, preprocess=preprocess)
        x = self.feature_vector(data)
        y = self.l.predict(x[None])[0] # extend dummy batch axis, then reduce it
        return self.labelset[y]

class GMMClassifier(FeatureExtractorClassifier):
    def __init__(self, feature_extractor, **params):
        super().__init__(feature_extractor)
        self.params = params

    def __repr__(self):
        return f'GMMClassifier({self.f}, {self.params})'

    def train(self, dataset):
        super().train(dataset)
        print('fitting a gmm on positive label...')
        self.gmms = [
            GaussianMixture(**self.params).fit([
                v for v, l_ in zip(self.item_vectors, self.item_labels) if l == l_
            ])
            for l in self.labelset
        ]

    def classify(self, data, preprocess=True):
        super().classify(data, preprocess=preprocess)
        x = self.feature_vector(data)
        scores = np.array([
            gmm.score(x[None]) for gmm in self.gmms
        ])
        y = scores.argmax()
        return self.labelset[y]


class VoteEnsembleClassifier(BaseClassifier):
    def __init__(self, *cfers):
        self.cfers = cfers

    def __repr__(self):
        return 'VoteEnsembleClassifier({})'.format( ', '.join(map(str, self.cfers)) )

    def train(self, dataset):
        super().train(dataset)
        for cfer in self.cfers:
            cfer.train(dataset)

    def classify(self, data, preprocess=True):
        super().classify(data, preprocess=preprocess)
        labels = []
        for cfer in self.cfers:
            labels.append( cfer.classify(data, preprocess=preprocess) )
        return mode(labels).mode[0] # each component classifier has a vote, return the most voted label

    def update(self, label):
        for cfer in self.cfers:
            cfer.update(label)

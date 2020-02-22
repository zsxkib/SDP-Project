from importlib.machinery import SourceFileLoader
from sklearn.naive_bayes import *
from sklearn.linear_model import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.mixture import *
from scipy.stats import mode
from tqdm import tqdm
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt
import lycon

def softmax(xs):
    xs = np.exp(xs)
    s = np.sum(xs)
    return np.array([x / s for x in xs])


class BaseClassifier():
    def train(self, dataset, cache={}):
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

    def test(self, dataset, update=False, cache={}, dump_dir=None):
        print('test', self, 'on', dataset)
        N = len(self.labelset)
        confusion_matrix = pd.DataFrame(np.zeros(( N + 1, N + 1 )))
        confusion_matrix.columns = self.labelset + ['accuracy']
        confusion_matrix.index = self.labelset + ['recall']
        n_correct = n_total = n_unknown = n_total_classified = n_correct_bin = 0
        for image, correct_label, filename in tqdm(dataset, desc='testing'):
            n_total += 1
            # since our dataset only has images from one angle per item, use it twice and pretend it's from two angles
            # no need to preprocess since images are already in right shape from the testset (assume it has the same config as trainset)
            if not isinstance(image, dict):
                # if testing on single image, duplicate the image to make it a dictionary
                image = dict(image_top=image, image_side=image)
            predict_label = self.classify(
                image,
                preprocess=False, cache_key=filename, cache=cache
            )
            if predict_label == 'unknown':
                n_unknown += 1
                continue
            if update:
                self.update(correct_label)
            confusion_matrix.iloc[
                self.labelset.index(predict_label),
                self.labelset.index(correct_label),
            ] += 1
            if correct_label != predict_label and dump_dir is not None:
                plt.imsave(f"{dump_dir}/Predict-{predict_label}-Correct-{correct_label}-{filename}.png", image['image_top'])
                #plt.imsave(f"{dump_dir}/Predict-{predict_label}-Correct-{correct_label}-{filename}-1.png", image['image_side'])
            if correct_label == predict_label:
                n_correct += 1
                n_correct_bin += 1
            elif correct_label != 'trash' and predict_label != 'trash':
                n_correct_bin += 1
            n_total_classified += 1
        confusion_matrix.loc[self.labelset, 'accuracy'] = (
            confusion_matrix.values[range(N), range(N)]
          / confusion_matrix.values[:N, :N].sum(1)
        )
        confusion_matrix.loc['recall', self.labelset] = (
            confusion_matrix.values[range(N), range(N)]
          / confusion_matrix.values[:N, :N].sum(0)
        )
        unknown_rate = n_unknown / n_total if n_total > 0 else 0
        accuracy = n_correct / n_total_classified if n_total_classified > 0 else 0
        bin_accuracy = n_correct_bin / n_total_classified if n_total_classified > 0 else 0
        print('unknown rate', unknown_rate)
        print('accuracy', accuracy)
        print('binary accuracy', bin_accuracy)
        print('confusion matrix')
        print(confusion_matrix)
        return accuracy, confusion_matrix


class NeuralNetClassifier(BaseClassifier):
    def __init__(self, model_dir, thres):
        super().__init__()
        self.model = keras.models.load_model(model_dir + 'model.h5')
        self.preproc = SourceFileLoader('preproc', model_dir + 'preproc.py').load_module().preproc
        labels_map = eval(open(model_dir + 'labels_map.txt').read())
        self.index_to_label = {v: k for k, v in labels_map.items()}
        self.labelset = list(labels_map.keys()) # for baseclassifier to use
        self.t = thres

    def __repr__(self):
        return f'NNClassifier(t={self.t})'

    def classify(self, data, **_):
        image_top = self.preproc(data['image_top'])
        image_side = self.preproc(data['image_side'])
        scores = self.model.predict(np.stack([image_top, image_side])).mean(0)
        #print(scores, self.index_to_label)
#hm
#        scores_top = softmax(scores[0])
#        scores_side = softmax(scores[1])
#        scores = 2 / ( 1 / scores_top + 1 / scores_side )
#max
#        if scores_top.max() > scores_side.max():
#            scores = scores_top
#        else:
#            scores = scores_side
        scores = softmax(scores)
        score = scores.max()
        if score > self.t:
            label = self.index_to_label[ scores.argmax() ]
            return label
        else:
            return 'unknown'


class FeatureExtractorClassifier(BaseClassifier):
    def __init__(self, feature_extractor):
        self.f = feature_extractor
        self.item_vectors = []
        self.item_labels = []

    def __repr__(self):
        return f'FeatureExtractorClassifier({self.f})'

    def train_feature_vector(self, image, filename, cache={}):
        return self.f.extract(image[None], cache_key=filename, cache=cache)

    def feature_vector(self, data, cache_key, cache):
        return self.f.extract(np.stack([
            data['image_top'],
            data['image_side'],
        ]), cache_key=cache_key, cache=cache) # todo support multiple keys

    def train(self, dataset, cache={}):
        super().train(dataset)
        for image, label, filename in tqdm(dataset, desc='extracting features'):
            self.item_vectors.append( self.train_feature_vector(image, filename, cache) )
            self.item_labels.append( label )

class RandomForest(FeatureExtractorClassifier):
    def __init__(self, feature_extractor, **params):
        super().__init__(feature_extractor)
        self.rc = RandomForestClassifier(**params)

    def train(self, dataset):
        super().train(dataset)
        y = [self.labelset.index(l) for l in self.item_labels]
        X = self.item_vectors
        self.rc.fit(X,y)

    def classify(self, data, preprocess=True):
        super().classify(data, preprocess=preprocess)
        x = self.feature_vector(data)
        y = self.rc.predict(x[None])[0] # extend dummy batch axis, then reduce it
        return self.labelset[y]

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

    def classify(self, data, preprocess=True, cache_key=None, cache={}):
        super().classify(data, preprocess=preprocess)
        v = self.last_v = self.feature_vector(data, cache_key=cache_key, cache=cache)
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
        print('fitting a gmm on each label...')
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
            labels.append( cfer.classify(data, preprocess=False) ) # avoid preprocessing twice
        return mode(labels).mode[0] # each component classifier has a vote, return the most voted label

    def update(self, label):
        for cfer in self.cfers:
            cfer.update(label)

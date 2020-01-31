from sklearn.linear_model import LogisticRegression
from sklearn.mixture import GaussianMixture
from sklearn.naive_bayes import MultinomialNB
from scipy.stats import mode
from tqdm import tqdm
import pandas as pd
import numpy as np

class FeatureExtractorClassifier():
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
        print('train', self, 'on', dataset)
        self.trainset = dataset # include the trainset so the images are processed correctly on testing
        self.labelset = sorted(dataset.label_set())
        for image, label in tqdm(dataset, desc='extracting features'):
            self.item_vectors.append( self.train_feature_vector(image) )
            self.item_labels.append( label )

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



class MNBClassifier(FeatureExtractorClassifier):
    def __init__(self, feature_extractor, **params):
        super().__init__(feature_extractor)
        self.params = params

    def __repr__(self):
        return f'MNBClassifier({self.f}, {self.params})'

    def train(self, dataset):
        super().train(dataset)
        print('fitting a MNB on positive label...')
        
        # I need two lists, vectors and their corresponding labels, here may need fix
        self.mnb = MultinomialNB(alpha=0.5).fit(self.item_vectors, self.labelset) 

    def classify(self, data, preprocess=True):
        super().classify(data, preprocess=preprocess)
        x = self.feature_vector(data)
        # scores = np.array([
        #     mnb.score(x[None]) for gmm in self.gmms
        # ])
        y = mnb.predict(x)
        return y
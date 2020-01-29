from scipy.stats import mode
from tqdm import tqdm
import pandas as pd
import numpy as np

class DummyClassifier():
    def __init__(self):
        pass
    
    def __repr__(self):
        return 'DummyClassifier()'

    def train(self, dataset):
        print('train', self, 'on', dataset)
        self.trainset = dataset # include the trainset so the images are processed correctly on testing

    def classify(self, data, preprocess=True):
        assert hasattr(self, 'trainset'), 'model not trained'
        if preprocess:
            for key in data:
                data[key] = self.trainset.preprocess(data[key])
        return 'unknown'

    def update(self, label):
        return 'updated'
    
    def test(self, dataset, update=False):
        print('test', self, 'on', dataset)
        labels = list( dataset.label_set() )
        confusion_matrix = pd.DataFrame(np.zeros((len(labels), len(labels))))
        confusion_matrix.columns = labels
        confusion_matrix.index = labels
        n_correct = n_total = 0
        for image, correct_label in tqdm(dataset, desc='testing'):
            # since our dataset only has images from one angle per item, use it twice and pretend it's from two angles
            # no need to preprocess since images are already in right shape from the testset (assume it has the same config as trainset)
            predict_label = self.classify(dict(image_top=image, image_side=image), preprocess=False)
            if update:
                self.update(correct_label)
            confusion_matrix.iloc[
                labels.index(correct_label),
                labels.index(predict_label),
            ] += 1
            if correct_label == predict_label:
                n_correct += 1
            n_total += 1
        accuracy = (n_correct / (n_total + 1e-9))
        print('accuracy', accuracy)
        print('confusion matrix')
        print(confusion_matrix)
        return accuracy, confusion_matrix

class KNNClassifier(DummyClassifier):
    def __init__(self, feature_extractor, threshold=0.8, k=1):
        self.f = feature_extractor
        self.t = threshold
        self.k = k
        self.item_vectors = []
        self.item_labels = []
    
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

    def train(self, dataset):
        super().train(dataset)
        for image, label in tqdm(dataset, desc='training'):
            self.item_vectors.append( self.train_feature_vector(image) )
            self.item_labels.append( label )
    
    def train_feature_vector(self, image):
        return self.f.extract(image[None])

    def feature_vector(self, data):
        return self.f.extract(np.stack([
            data['image_top'],
            data['image_side'],
        ]))

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

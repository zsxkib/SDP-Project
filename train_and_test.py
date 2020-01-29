from classifier import KNNClassifier
from feature_extractor import Resnet50
from dataset import DirDataset
import pickle

print('loading datasets and models...')
train_ds = DirDataset('demo1-dataset/train', 256, 256)
test_ds = DirDataset('demo1-dataset/test1', 256, 256)
cfer = KNNClassifier(Resnet50(), k=1)

cfer.train(train_ds)
cfer.test(test_ds)

pickle.dump(cfer, open('cfer.pkl', 'wb'))

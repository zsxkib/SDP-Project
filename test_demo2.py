from feature_extractor import *
from classifier import *
from dataset import *
import numpy as np
import pickle
import h5py

print('loading datasets and models...')

import sys
if sys.argv[1] == 'nn2':
    print('neural net trained on litterati')
    for t in np.linspace(0.3, 0.6, 10):
        custom_ds = DirDatasetPair('demo2-dataset/custom-test') #, 512, 512, proc=False)
        cfer = NeuralNetClassifier('../litterati/model/', thres=t)
        cfer.test(custom_ds, dump_dir='demo2-dataset/custom-test-dump2')
elif sys.argv[1] == 'nn1':
    print('neural net trained on litterati')
    for t in np.linspace(0.3, 0.6, 10):
        custom_ds = DirDataset('demo2-dataset/custom-test', 512, 512, proc=False)
        cfer = NeuralNetClassifier('../litterati/model/', thres=t)
        cfer.test(custom_ds, dump_dir='demo2-dataset/custom-test-dump1')
elif sys.argv[1] == 'knn':
    print('knn trained on trashnet')
    trashnet_ds = DirDataset('demo2-dataset/trashnet-photos', 512, 512)
    custom_ds = DirDataset('demo2-dataset/custom-test', 512, 512)
    cfer = KNNClassifier(Resnet("resnet50"),k=1)
    cfer.train(trashnet_ds)
    cfer.test(custom_ds)

from feature_extractor import *
from classifier import *
from dataset import *
import numpy as np
import pickle
import h5py

print('loading datasets and models...')
train_ds = DirDataset('demo1-dataset/train', 256, 256)
test_ds = DirDataset('demo1-dataset/test1', 256, 256)
seed = 42

print('grid searching best combination...')
grid = [
    c.format(e)
    for c in [
        'KNNClassifier({}, k=1)',
#        'SklearnClassifier({}, LogisticRegression(max_iter=1000))',
#        'SklearnClassifier({}, GaussianNB())',
#        'GMMClassifier({}, n_components=5, covariance_type="full")',
#        'RandomForest({})'
    ]
    for e in [
        'Resnet("resnet18")',
        'Resnet("resnet18")',
#        'Resnet("resnet34")',
#        'Resnet("resnet50")',
    ]
]
#grid = []
#grid.append('''\
#VoteEnsembleClassifier(
#    KNNClassifier(Resnet("resnet50"), k=1),
#    SklearnClassifier(Resnet("resnet18"), LogisticRegression(max_iter=1000)),
#    SklearnClassifier(Resnet("resnet50"), GaussianNB()),
#)''')

cache = h5py.File('cache.h5')

for i, g in enumerate(grid):
    np.random.seed(seed)
    print(i, g, flush=True)
    cfer = eval(g)
    cfer.train(train_ds, cache=cache)
    cfer.test(test_ds, cache=cache)
    pickle.dump(cfer, open(f'cfer{i}.pkl', 'wb'))
    print()

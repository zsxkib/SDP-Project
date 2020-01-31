from feature_extractor import *
from classifier import *
from dataset import *
import pickle

print('loading datasets and models...')
train_ds = DirDataset('demo1-dataset/train', 256, 256)
test_ds = DirDataset('demo1-dataset/test1', 256, 256)

print('grid searching best combination...')
grid = [
    c.format(e)
    for c in [
        'KNNClassifier({}, k=1)',
        'SklearnClassifier({}, LogisticRegression(max_iter=1000))',
        'SklearnClassifier({}, GaussianNB())',
        'GMMClassifier({}, n_components=5, covariance_type="full")',
    ]
    for e in [
        'Resnet("resnet18")',
        'Resnet("resnet34")',
        'Resnet("resnet50")',
    ]
]
#grid = []
#grid.append('''\
#VoteEnsembleClassifier(
#    KNNClassifier(Resnet("resnet50"), k=1),
#    SklearnClassifier(Resnet("resnet18"), LogisticRegression(max_iter=1000)),
#    SklearnClassifier(Resnet("resnet50"), GaussianNB()),
#)''')

for i, g in enumerate(grid):
    print(i, g, flush=True)
    cfer = eval(g)
    cfer.train(train_ds)
    cfer.test(test_ds)
    pickle.dump(cfer, open(f'cfer{i}.pkl', 'wb'))
    print()

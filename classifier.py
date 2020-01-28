from matplotlib import pyplot as plt
import numpy as np

class Classifier():
    def __init__(self, threshold=0):
        self.threshold = threshold
        # to do

    def classify(self, data):
        #self.last_feature = self.feature(data)
        plt.imshow(data['image_top'])
        plt.savefig('top.png')
        return 'unknown'

    def update(self, label):
        print('update', label)
        return 'updated'

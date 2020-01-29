import lycon
import os

class DirDataset():
    def __init__(self, d, width, height):
        self.d = d
        self.w = width
        self.h = height
        self.labels = [] # this is labels per file, not the label set as provided by method label_set()
        self.files = []
        for l in os.listdir(d):
            for f in os.listdir(os.path.join(d, l)):
                self.labels.append(l)
                self.files.append(os.path.join(d, l, f))

    def __repr__(self):
        return f'DirDataset({self.d}, {self.w}, {self.h})'

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        return (
            lycon.resize(lycon.load(self.files[i]), self.w, self.h) / 255,
            self.labels[i],
        )
    
    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
    
    def preprocess(self, image):
        return lycon.resize(image, self.w, self.h) / 255
    
    def label_set(self):
        return set(self.labels)

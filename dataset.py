from collections import defaultdict
import lycon
import os

class DirDataset():
    def __init__(self, d, width, height, proc=True):
        self.proc = proc
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
        img = lycon.load(self.files[i])
        if self.proc:
            img = self.preprocess(img)
        return (
            img,
            self.labels[i],
            os.path.basename(self.files[i]),
        )
    
    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
    
    def preprocess(self, image):
        return lycon.resize(image, self.w, self.h) / 255
    
    def label_set(self):
        return set(self.labels)

class DirDatasetPair():
    # used for nn only
    def __init__(self, d):
        self.d = d
        self.labels = {}
        self.files = defaultdict(lambda: [])
        for l in os.listdir(d):
            for f in os.listdir(os.path.join(d, l)):
                xs = f.split('-')
                name = '-'.join(xs[:-1])
                self.labels[name] = l
                self.files[name].append(os.path.join(d, l, f))
        self.labels = list(self.labels.values())
        self.files = list(self.files.values())

    def __repr__(self):
        return f'DirDatasetPair({self.d})'

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        img0 = lycon.load(self.files[i][0])
        if len(self.files[i]) > 1:
            img1 = lycon.load(self.files[i][1])
        else:
            img1 = img0
        return (
            dict(image_top=img0, image_side=img1),
            self.labels[i],
            os.path.basename(self.files[i][0]),
        )
    
    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
    
    def label_set(self):
        return set(self.labels)

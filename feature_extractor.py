from torchvision import models
import torch.nn.functional as F
import torch.nn as nn
import torch
import numpy as np

class Lambda(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.forward = fn

    @staticmethod
    def identity(x):
        return x

class Resnet():
    def __init__(self, model_name, device='cuda', weights=None):
        self.model_name = model_name
        self.device = device
        self.resnet = getattr(models, model_name)(pretrained=True).eval().to(device)
        # replace last layer with identity
        self.n_dim = self.resnet.fc.in_features
        self.resnet.fc = Lambda(Lambda.identity)
        self.weights = weights
        if weights is not None:
            self.resnet.load_state_dict(torch.load(weights, map_location=device))
    
    def __repr__(self):
        return f'Resnet({self.model_name}, weights={self.weights})'

    def extract(self, images, cache_key=None, cache={}):
        if cache_key is not None and cache_key in cache:
            return np.array( cache[cache_key] )
        # images: N x Height x Width x Channel
        x = torch.FloatTensor(images).permute(0, 3, 1, 2).to(self.device)
        with torch.no_grad():
            # average across images to get one single feature vector
            y = self.resnet(x).detach().cpu().numpy().mean(0)
        if cache_key is not None:
            cache[cache_key] = y
        return y

from torchvision import models
import torch.nn.functional as F
import torch.nn as nn
import torch

class Lambda(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.forward = fn

    @staticmethod
    def identity(x):
        return x

class Resnet50():
    def __init__(self, device='cuda', weights=None):
        self.device = device
        self.resnet50 = models.resnet50(pretrained=True).eval().to(device)
        # replace last layer with identity
        self.resnet50.fc = Lambda(Lambda.identity)
        self.weights = weights
        if weights is not None:
            self.resnet50.load_state_dict(torch.load(weights, map_location=device))
    
    def __repr__(self):
        return f'Resnet50(weights={self.weights})'

    def extract(self, images):
        # images: N x Height x Width x Channel
        x = torch.FloatTensor(images).permute(0, 3, 1, 2).to(self.device)
        with torch.no_grad():
            # average across images to get one single feature vector
            y = self.resnet50(x).detach().cpu().numpy().mean(0)
        return y

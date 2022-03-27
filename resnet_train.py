import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import torch
import torchvision
import tarfile
from torchvision import models
import torch.nn as nn
import numpy as np
from tqdm.notebook import tqdm
import torch.nn.functional as F
from torchvision.datasets.utils import download_url
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, SubsetRandomSampler
import torchvision.transforms as tt
from torch.utils.data import random_split
from torchvision.utils import make_grid

import matplotlib
import matplotlib.pyplot as plt
# matplotlib.rcParams['figure.facecolor'] = '#ffffff'


def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')


def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)


class DeviceDataLoader():
    """Wrap a dataloader to move data to a device"""

    def __init__(self, dl, device):
        self.dl = dl
        self.device = device

    def __iter__(self):
        """Yield a batch of data after moving it to device"""
        for b in self.dl:
            yield to_device(b, self.device)

    def __len__(self):
        """Number of batches"""
        return len(self.dl)


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))


class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch
        out = self(images)  # Generate predictions
        loss = F.cross_entropy(out, labels)  # Calculate loss
        return loss

    def validation_step(self, batch):
        images, labels = batch
        # images, labels = images.to(device), labels.to(device)
        out = self(images)  # Generate predictions
        loss = F.cross_entropy(out, labels)  # Calculate loss
        acc = accuracy(out, labels)  # Calculate accuracy
        return {'val_loss': loss.detach(), 'val_acc': acc}

    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()  # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()  # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}

    def epoch_end(self, epoch, result):
        print("Epoch [{}],{} train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch, "last_lr: {:.5f},".format(result['lrs'][-1]) if 'lrs' in result else '',
            result['train_loss'], result['val_loss'], result['val_acc']))


class MyModel(ImageClassificationBase):
    def __init__(self, num_classes, pretrained=True):
        super().__init__()

        # Use a pretrained model
        self.network = models.resnet34(pretrained=pretrained)
        # Replace last layer
        self.network.fc = nn.Linear(self.network.fc.in_features, num_classes)

    def forward(self, xb):
        return self.network(xb)


@torch.no_grad()
def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)


def fit(epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.SGD):
    history = []
    optimizer = opt_func(model.parameters(), lr)
    for epoch in range(epochs):
        # Training Phase
        model.train()
        train_losses = []
        for batch in tqdm(train_loader):
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        # Validation phase
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        model.epoch_end(epoch, result)
        history.append(result)
    return history


def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']


def fit_one_cycle(epochs, max_lr, model, train_loader, val_loader,
                  weight_decay=0, grad_clip=None, opt_func=torch.optim.SGD):
    torch.cuda.empty_cache()
    history = []

    # Set up custom optimizer with weight decay
    optimizer = opt_func(model.parameters(), max_lr, weight_decay=weight_decay)
    # Set up one-cycle learning rate scheduler
    sched = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr, epochs=epochs,
                                                steps_per_epoch=len(train_loader))

    for epoch in range(epochs):
        # Training Phase
        model.train()
        train_losses = []
        lrs = []
        for batch in tqdm(train_loader):
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()

            # Gradient clipping
            if grad_clip:
                nn.utils.clip_grad_value_(model.parameters(), grad_clip)

            optimizer.step()
            optimizer.zero_grad()

            # Record & update learning rate
            lrs.append(get_lr(optimizer))
            sched.step()

        # Validation phase
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        result['lrs'] = lrs
        model.epoch_end(epoch, result)
        history.append(result)
    return history


def count_classes(data_path):
    return len(next(os.walk(data_path))[1])


def train(data_path, epochs, learning_rate, val_data_size, split_dataset=True):
    num_classes = count_classes(data_path)

    if split_dataset:
        root_dir = data_path
    else:
        train_dir = "../first_quarter"
        val_dir = "../second_quarter"

    image_transforms = {
        "train": tt.Compose([
            tt.Resize((300, 300)),
            tt.ToTensor(),
            tt.Normalize([0.5, 0.5, 0.5],
                         [0.5, 0.5, 0.5])
        ]),
        "test": tt.Compose([
            tt.Resize((300, 300)),
            tt.ToTensor(),
            tt.Normalize([0.5, 0.5, 0.5],
                         [0.5, 0.5, 0.5])
        ])
    }

    if split_dataset:
        football_dataset = ImageFolder(root=root_dir, transform=image_transforms["train"])
        football_dataset.class_to_idx
        idx2class = {v: k for k, v in football_dataset.class_to_idx.items()}
        football_dataset_size = len(football_dataset)
        football_dataset_indices = list(range(football_dataset_size))
        np.random.shuffle(football_dataset_indices)
        val_split_index = int(np.floor(val_data_size * football_dataset_size))
        train_idx, val_idx = football_dataset_indices[val_split_index:], football_dataset_indices[:val_split_index]
        train_sampler = SubsetRandomSampler(train_idx)
        val_sampler = SubsetRandomSampler(val_idx)

        train_dl = DataLoader(dataset=football_dataset, batch_size=32, sampler=train_sampler)
        valid_dl = DataLoader(dataset=football_dataset, batch_size=32, sampler=val_sampler)
    else:
        # PyTorch datasets
        train_ds = ImageFolder(train_dir, image_transforms['train'])
        valid_ds = ImageFolder(val_dir, image_transforms['train'])

        batch_size = 1

        # PyTorch data loaders
        train_dl = DataLoader(train_ds, batch_size=32, shuffle=True)
        valid_dl = DataLoader(valid_ds, batch_size=32, shuffle=True)

    device = get_default_device()
    print(device)
    train_dl = DeviceDataLoader(train_dl, device)
    valid_dl = DeviceDataLoader(valid_dl, device)


    model = MyModel(num_classes)
    model.to(device)
    history = fit(epochs, learning_rate, model, train_dl, valid_dl, opt_func=torch.optim.SGD)
    return history, model

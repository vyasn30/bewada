import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch import optim

class ChessValueDataset(Dataset):
    def __init__(self):
        dat = np.load("processed/dataset100k.npz")
        self.X = dat["arr_0"][0:10]
        self.Y = dat['arr_1'][0:10]
        print("loaded", self.X.shape, self.Y.shape)

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return (self.X[idx], self.Y[idx])

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.a1 = nn.Conv2d(5,16,kernel_size=3, padding=1)
        self.a2 = nn.Conv2d(16,16,kernel_size=3, padding=1)
        self.a3 = nn.Conv2d(16,32,kernel_size=3, stride=2)

        
        self.b1 = nn.Conv2d(32,32,kernel_size=3, padding=1)
        self.b2 = nn.Conv2d(32,32,kernel_size=3, padding=1)
        self.b3 = nn.Conv2d(32,64,kernel_size=3, stride=2)


        self.c1 = nn.Conv2d(64,64,kernel_size=3, padding=1)
        self.c2 = nn.Conv2d(64,64,kernel_size=3, padding=1)
        self.c3 = nn.Conv2d(64,128,kernel_size=3, stride=2)

        self.d1 = nn.Conv2d(128,128,kernel_size=1)
        self.d2 = nn.Conv2d(128,128,kernel_size=1)
        self.d3 = nn.Conv2d(128,128,kernel_size=1)

        self.last = nn.Linear(128,1)



    def forward(self, x):
        x = F.relu(self.a1(x))
        x = F.relu(self.a2(x))
        x = F.relu(self.a3(x))

        x = F.relu(self.b1(x))
        x = F.relu(self.b2(x))
        x = F.relu(self.b3(x))

        x = F.relu(self.c1(x))
        x = F.relu(self.c2(x))
        x = F.relu(self.c3(x))

        x = F.relu(self.d1(x))
        x = F.relu(self.d2(x))
        x = F.relu(self.d3(x))

        x = x.view(-1, 128)
        x = self.last(x)

        return F.sigmoid(x)


device = "cpu"


chess_dataset = ChessValueDataset()
train_loader = torch.utils.data.DataLoader(chess_dataset, batch_size=1, shuffle = True)
model = Net()
optimizer = optim.Adam(model.parameters())
floss = nn.MSELoss()

if device == "cuda":
    model.cuda()

model.train()

for epoch in range(100):
    all_loss = 0
    num_loss = 0

    for batch_idx, (data, target) in enumerate(train_loader):
        target = target.unsqueeze(-1)
        data, target = data.to(device), target.to(device)
        data = data.float()
        target = target.float()

        optimizer.zero_grad()
        output = model(data)

        loss = floss(output, target)
        loss.backward()
        optimizer.step()

        all_loss += loss.item()
        num_loss += 1 

    print("%3d: %f" %(epoch, all_loss/num_loss))
















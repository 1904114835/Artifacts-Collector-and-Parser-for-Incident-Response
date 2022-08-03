import torch
import joblib
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
class VAE(nn.Module):
    def __init__(self, image_size=15, h_dim=10, z_dim=5):
        super(VAE, self).__init__()
        self.fc1 = nn.Linear(image_size, h_dim)
        self.fc2 = nn.Linear(h_dim, z_dim)
        self.fc3 = nn.Linear(h_dim, z_dim)
        self.fc4 = nn.Linear(z_dim, h_dim)
        self.fc5 = nn.Linear(h_dim, image_size)
        
    def encode(self, x):
        h = F.relu(self.fc1(x))
        return self.fc2(h), self.fc3(h)
    
    def reparameterize(self, mu, log_var):
        std = torch.exp(log_var/2)
        eps = torch.randn_like(std)
        return mu + eps * std 

    def decode(self, z):
        h = F.relu(self.fc4(z))
        return torch.sigmoid(self.fc5(h))
    
    def forward(self, x):
        mu, log_var = self.encode(x)
        z = self.reparameterize(mu, log_var)
        x_reconst = self.decode(z)
        return x_reconst, mu, log_var
        
def pre(d:list,vaemodel_path='vae.pth',pcamodel_path='pca.model',min_max_scaler_path='min_max_scaler.model'):
    """data: event category,timestamp,source,ID,type,data"""
    model=VAE()
    model.load_state_dict(torch.load(vaemodel_path))
    pcamodel=joblib.load(pcamodel_path)
    min_max_scaler=joblib.load(min_max_scaler_path)
    source_dict=np.load('source_dict.npy',allow_pickle=True).item()
    if d[2] in source_dict.keys():
        trow=[int(d[0]),int(d[1]),source_dict[d[2]],int(d[3]),int(d[4])]
    else:
        trow=[int(d[0]),int(d[1]),0,int(d[3]),int(d[4])]
    data_str=d[-1]
    handle=[]
    for s in data_str:
        handle.append(ord(s))
    for i in range(400-len(data_str)):
        handle.append(0)
    pca_d=pcamodel.transform([handle])
    trow.extend(pca_d[0])
    trow=min_max_scaler.transform([trow])
    
    x=torch.tensor(trow)
    x=x.to(torch.float32)
    x_reconst, mu, log_var = model(x)
    kl_div = - 0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
    return kl_div.item()

import load_eventlog
import torch
import joblib
import numpy as np
if __name__=="__main__":
    print(load_eventlog.pre([1014,'1653650672','Microsoft-WindNS-Client', 1014, 2, 'wpad\n128\n02000000C0A8580200000000000000000\n']))
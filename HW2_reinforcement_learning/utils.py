# utils.py
import torch
import torchvision.transforms as T

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = T.Compose([
    T.ToPILImage(),
    T.Resize((84, 84)),
    T.Grayscale(),
    T.ToTensor()
])

def preprocess(obs, env=None, last_obss=None):
    obs = obs.transpose((1, 2, 0)) if obs.shape[0] == 3 else obs
    obs = transform(obs).to(device)
    return obs

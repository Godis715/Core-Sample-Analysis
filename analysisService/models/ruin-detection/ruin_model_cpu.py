import os
import torch
from torchvision import transforms
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = torch.load(os.path.join(BASE_DIR, 'ruin_squeeze.pth'), map_location='cpu')

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

])

def predict(pil_img):
    inp = transform(pil_img).unsqueeze(0)
    pred = 'none' if model(inp).data.numpy().argmax() == 0 else 'high'
    return pred
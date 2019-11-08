import torch
from torchvision import transforms
model = torch.load('ruin_squeeze.pth')

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

])

def predict(pil_img):
    inp = transform(pil_img).unsqueeze(0)
    inp = inp.to(torch.device('cuda:0'))
    pred = 'не разрушен' if model(inp).cpu().data.numpy().argmax() == 0 else 'разрушен'
    return pred

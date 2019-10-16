import torch
from torchvision import transforms
model = torch.load('ruin_pred/ruin_squeeze.pth')
model.cpu()

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

])

def predict(pil_img):
    inp = transform(pil_img).unsqueeze(0)
    pred = 'не разрушен' if model(inp).data.numpy().argmax() == 0 else 'разрушен'
    return pred

from PIL import Image
import torch
from torchvision import transforms
from stego.dl_model import StegoNet

def infer_dl_stego(cover_path, secret_path, output_path='stego_dl.png'):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = StegoNet().to(device)
    model.load_state_dict(torch.load('stego/dl_model.pth', map_location=device))
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor()
    ])

    cover = transform(Image.open(cover_path).convert('RGB')).unsqueeze(0).to(device)
    secret = transform(Image.open(secret_path).convert('RGB')).unsqueeze(0).to(device)

    with torch.no_grad():
        stego = model(cover, secret)

    stego_img = stego.squeeze(0).cpu()
    stego_img = transforms.ToPILImage()(stego_img.clamp(0, 1))
    stego_img.save(output_path)
    print(f"DL stego image saved to {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python infer_dl_stego.py cover.png secret.png output.png")
    else:
        infer_dl_stego(sys.argv[1], sys.argv[2], sys.argv[3])

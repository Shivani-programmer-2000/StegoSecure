# train_dl_model.py

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from stego.dl_model import StegoNet
from stego_dataset import StegoDataset  # ✅ Make sure this file exists

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = StegoNet().to(device)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor()
    ])

    # ✅ Use your own dataset here
    train_dataset = StegoDataset(
    cover_dir='stego_dataset/train/train/clean',
    secret_dir='stego_dataset/train/train/stego',
    transform=transform
)


    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

    num_epochs = 10
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for cover, secret in train_loader:
            cover, secret = cover.to(device), secret.to(device)

            optimizer.zero_grad()

            # Encode secret into cover
            stego = model(cover, secret)

            # Losses
            loss_cover = criterion(stego, cover)
            extracted = model.extract(stego)
            loss_secret = criterion(extracted, secret)

            loss = loss_cover + loss_secret
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss / len(train_loader):.4f}")

    # Save model
    if not os.path.exists('stego'):
        os.makedirs('stego')
    torch.save(model.state_dict(), 'stego/dl_model.pth')
    print("✅ Training complete. Model saved to stego/dl_model.pth")

if __name__ == "__main__":
    train()

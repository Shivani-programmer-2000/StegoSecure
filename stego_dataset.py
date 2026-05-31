# stego_dataset.py
import os
from PIL import Image
from torch.utils.data import Dataset

class StegoDataset(Dataset):
    def __init__(self, cover_dir, secret_dir, transform=None):
        self.cover_dir = cover_dir
        self.secret_dir = secret_dir
        self.transform = transform

        self.cover_images = sorted(os.listdir(cover_dir))
        self.secret_images = sorted(os.listdir(secret_dir))

        # Map clean → stego based on index
        self.pairs = list(zip(self.cover_images, self.secret_images))

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        cover_name, secret_name = self.pairs[idx]
        cover_path = os.path.join(self.cover_dir, cover_name)
        secret_path = os.path.join(self.secret_dir, secret_name)

        cover_img = Image.open(cover_path).convert("RGB")
        secret_img = Image.open(secret_path).convert("RGB")

        if self.transform:
            cover_img = self.transform(cover_img)
            secret_img = self.transform(secret_img)

        return cover_img, secret_img


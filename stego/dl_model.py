import torch
import torch.nn as nn
import torch.nn.functional as F

class StegoNet(nn.Module):
    def __init__(self):
        super(StegoNet, self).__init__()
        
        # Encoder for cover image
        self.cover_encoder = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        
        # Encoder for secret image
        self.secret_encoder = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        
        # Fusion and decoding to stego image
        self.decoder = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 3, kernel_size=3, padding=1),
            nn.Sigmoid(),  # output in [0,1]
        )

        # Extractor network to recover secret from stego image
        self.extractor = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 3, kernel_size=3, padding=1),
            nn.Sigmoid(),
        )
    
    def forward(self, cover, secret):
        cover_feat = self.cover_encoder(cover)
        secret_feat = self.secret_encoder(secret)
        combined = torch.cat([cover_feat, secret_feat], dim=1)
        stego = self.decoder(combined)
        return stego
    
    def extract(self, stego):
        secret_rec = self.extractor(stego)
        return secret_rec


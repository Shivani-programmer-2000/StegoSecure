from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from PIL import Image
import numpy as np

def calculate_metrics(img1_path, img2_path):
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")

    # Resize both images to the same dimensions (choose img1 size here)
    img2 = img2.resize(img1.size)

    img1_np = np.array(img1)
    img2_np = np.array(img2)

    # Compute PSNR
    psnr_val = psnr(img1_np, img2_np, data_range=255)

    # Determine win_size based on image dimensions
    min_dim = min(img1_np.shape[0], img1_np.shape[1])
    win_size = min(7, min_dim)
    if win_size % 2 == 0:
        win_size -= 1

    # Compute SSIM
    ssim_val = ssim(img1_np, img2_np, win_size=win_size, channel_axis=-1, data_range=255)

    return psnr_val, ssim_val


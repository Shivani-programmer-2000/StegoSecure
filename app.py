from flask import Flask, request, render_template
from lsb import encode_image, decode_image
from crypto import encrypt, decrypt
from utils.metrics import calculate_metrics
import os
from PIL import Image
import torch
import torchvision.transforms as transforms
from stego.dl_model import StegoNet

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load DL model once at startup
model = StegoNet()
model.load_state_dict(torch.load('stego/dl_model.pth', map_location='cpu'))
model.eval()

def pil_to_tensor(img):
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor()
    ])
    return transform(img).unsqueeze(0)  # Add batch dimension

def tensor_to_pil(tensor):
    tensor = tensor.squeeze(0).clamp(0, 1)  # Remove batch dimension and clamp to [0,1]
    return transforms.ToPILImage()(tensor)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lsb/hide', methods=['POST'])
def lsb_hide():
    image = request.files['image']
    secret = request.form['secret']
    key = request.form['key']

    image_path = os.path.join(UPLOAD_FOLDER, 'input_lsb.png')
    image.save(image_path)

    encrypted = encrypt.encrypt_message(secret, key)
    output_path = os.path.join(UPLOAD_FOLDER, 'output_lsb.png')
    encode_image(image_path, output_path, encrypted)

    psnr, ssim = calculate_metrics(image_path, output_path)
    return render_template('result.html', psnr=psnr, ssim=ssim, download_link='output_lsb.png')


@app.route('/lsb/reveal', methods=['POST'])
def reveal():
    image = request.files['image']
    key = request.form['key']
    image_path = os.path.join(UPLOAD_FOLDER, 'reveal.png')
    image.save(image_path)

    encoded = decode_image(image_path)
    try:
        decrypted = decrypt.decrypt_message(encoded, key)
    except Exception:
        decrypted = "[Decryption Failed]"

    return render_template('message_result.html', message=decrypted)


@app.route('/dl/hide', methods=['POST'])
def dl_hide():
    cover_file = request.files['cover_image']
    secret_file = request.files['secret_image']

    cover_img = Image.open(cover_file).convert('RGB')
    secret_img = Image.open(secret_file).convert('RGB')

    cover_tensor = pil_to_tensor(cover_img)
    secret_tensor = pil_to_tensor(secret_img)

    with torch.no_grad():
        stego_tensor = model(cover_tensor, secret_tensor)

    stego_img = tensor_to_pil(stego_tensor)
    output_path = os.path.join(UPLOAD_FOLDER, 'output_dl.png')
    stego_img.save(output_path)

    cover_img.save(os.path.join(UPLOAD_FOLDER, 'input_dl.png'))

    psnr, ssim = calculate_metrics(os.path.join(UPLOAD_FOLDER, 'input_dl.png'), output_path)
    return render_template('result.html', psnr=psnr, ssim=ssim, download_link='output_dl.png')

if __name__ == '__main__':
    app.run(debug=True)

import streamlit as st
from stego import lsb
from crypto import encrypt, decrypt
from utils.metrics import calculate_metrics
from PIL import Image
import io

st.title("StegoSecure - Steganography with Quality Control")

uploaded_image = st.file_uploader("Upload Cover Image", type=['png', 'jpg'])
secret_text = st.text_area("Enter Secret Message")
key = st.text_input("Enter Encryption Key", type="password")

quality = st.slider("Image Quality (Compression Level)", 10, 100, 90)

if st.button("Hide Message"):
    if uploaded_image and secret_text and key:
        img = Image.open(uploaded_image).convert("RGB")
        img.save("static/input.png")

        encrypted = encrypt.encrypt_message(secret_text, key)
        lsb.encode_image("static/input.png", "static/output.png", encrypted)

        # Here you can simulate quality control by compressing the image
        output_img = Image.open("static/output.png")
        buffer = io.BytesIO()
        output_img.save(buffer, format="PNG", quality=quality)
        buffer.seek(0)

        with open("static/output.png", "wb") as f:
            f.write(buffer.read())

        psnr, ssim = calculate_metrics("static/input.png", "static/output.png")

        st.success("Message hidden successfully!")
        st.image(output_img, caption="Stego Image")
        st.write(f"PSNR: {psnr:.2f}")
        st.write(f"SSIM: {ssim:.2f}")
        
        st.download_button(
            label="Download Stego Image",
            data=open("static/output.png", "rb").read(),
            file_name="output.png",
            mime="image/png"
        )
    else:
        st.error("Please upload image, enter message, and key!")

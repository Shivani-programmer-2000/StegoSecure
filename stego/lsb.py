from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def encode_image(input_path, output_path, message):
    img = Image.open(input_path)
    binary = text_to_bin(message + "###")
    pixels = list(img.getdata())
    index = 0
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel[:3]
        if index < len(binary):
            r = r & ~1 | int(binary[index])
            index += 1
        if index < len(binary):
            g = g & ~1 | int(binary[index])
            index += 1
        if index < len(binary):
            b = b & ~1 | int(binary[index])
            index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)

def decode_image(stego_path):
    img = Image.open(stego_path)
    pixels = list(img.getdata())
    binary = ''
    for pixel in pixels:
        for value in pixel[:3]:
            binary += str(value & 1)
    text = bin_to_text(binary)
    return text.split("###")[0]

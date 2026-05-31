from PIL import Image

def encode_image(input_path, output_path, message):
    img = Image.open(input_path).convert('RGB')
    binary_msg = ''.join([format(ord(c), '08b') for c in message]) + '00000000'  # null terminator
    pixels = img.load()
    width, height = img.size

    msg_index = 0
    for y in range(height):
        for x in range(width):
            if msg_index >= len(binary_msg):
                break
            r, g, b = pixels[x, y]
            r = (r & 0xFE) | int(binary_msg[msg_index])  # LSB of red channel
            pixels[x, y] = (r, g, b)
            msg_index += 1
        if msg_index >= len(binary_msg):
            break

    img.save(output_path)

def decode_image(input_path):
    img = Image.open(input_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    bits = []
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits.append(str(r & 1))

    message = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(''.join(byte), 2))
        if char == '\x00':
            break
        message += char

    return message


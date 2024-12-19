from PIL import Image
import math

BASE_MAP = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
BIT_TO_BASE = {v: k for k, v in BASE_MAP.items()}

def base_to_bits(base: str) -> str:
    return BASE_MAP.get(base.upper(), '00')  # defaults 'A'→'00'

def kmer_to_color(kmer: str) -> tuple[int, int, int]:
    # K=12 → 24 bits
    bits = ''.join(base_to_bits(b) for b in kmer)
    r = int(bits[0:8], 2)
    g = int(bits[8:16], 2)
    b = int(bits[16:24], 2)
    return (r, g, b)

def encode_sequence_to_image(dna: str, K: int = 12, scale: int = 100000) -> Image.Image:
    remainder = len(dna) % K
    if remainder != 0:
        dna += 'A' * (K - remainder)  # pad

    pixels = []
    for i in range(0, len(dna), K):
        kmer = dna[i:i+K]
        color = kmer_to_color(kmer)
        pixels.append(color)

    num_pixels = len(pixels)
    width = int(math.sqrt(num_pixels))
    if width * width < num_pixels:
        width += 1
    height = math.ceil(num_pixels / width)

    while len(pixels) < width * height:
        pixels.append((0,0,0))

    img = Image.new('RGB', (width, height))
    img.putdata(pixels)

    if scale > 1:
        img = img.resize((width * scale, height * scale), Image.NEAREST)

    return img

def decode_pixel_to_kmer(r, g, b, K=12) -> str:
    # Reverse operation of kmer_to_color
    # Convert R,G,B to binary and then decode to bases
    r_bits = f"{r:08b}"
    g_bits = f"{g:08b}"
    b_bits = f"{b:08b}"
    full_bits = r_bits + g_bits + b_bits  # 24 bits total for K=12
    
    kmer = ''
    for i in range(K):
        base_bits = full_bits[i*2:(i*2)+2]
        kmer += BIT_TO_BASE[base_bits]
    return kmer

def decode_image_to_sequence(img: Image.Image, K: int = 12) -> str:
    pixels = list(img.getdata())
    decoded_seq = ""
    for p in pixels:
        r, g, b = p
        kmer = decode_pixel_to_kmer(r, g, b, K)
        decoded_seq += kmer
    return decoded_seq

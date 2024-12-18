from PIL import Image
import math

BASE_MAP = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}

def base_to_bits(base: str) -> str:
    return BASE_MAP.get(base.upper(), '00')  # defaults to 'A'→'00' if unknown

def kmer_to_color(kmer: str) -> tuple[int, int, int]:
    # K=12 → 12 bases * 2 bits = 24 bits total
    bits = ''.join(base_to_bits(b) for b in kmer)
    r = int(bits[0:8], 2)
    g = int(bits[8:16], 2)
    b = int(bits[16:24], 2)
    return (r, g, b)

def encode_sequence_to_image(dna: str, K: int = 12, scale: int = 1000) -> Image.Image:
    remainder = len(dna) % K
    if remainder != 0:
        dna += 'A' * (K - remainder)  # Pad with 'A's if needed

    pixels = []
    for i in range(0, len(dna), K):
        kmer = dna[i:i+K]
        color = kmer_to_color(kmer)
        pixels.append(color)

    # Create a roughly square image
    num_pixels = len(pixels)
    width = int(math.sqrt(num_pixels))
    if width * width < num_pixels:
        width += 1
    height = math.ceil(num_pixels / width)

    # If not perfectly square, fill remaining pixels with black
    while len(pixels) < width * height:
        pixels.append((0, 0, 0))

    img = Image.new('RGB', (width, height))
    img.putdata(pixels)
    return img

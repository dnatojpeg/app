from PIL import Image, PngImagePlugin
import math

BASE_MAP = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
BIT_TO_BASE = {v: k for k, v in BASE_MAP.items()}

def base_to_bits(base: str) -> str:
    return BASE_MAP.get(base.upper(), '00')

def kmer_to_color(kmer: str) -> tuple[int, int, int]:
    bits = ''.join(base_to_bits(b) for b in kmer)
    r = int(bits[0:8], 2)
    g = int(bits[8:16], 2)
    b = int(bits[16:24], 2)
    return (r, g, b)

def encode_sequence_to_image(dna: str, K: int = 12, scale: int = 1) -> (Image.Image, PngImagePlugin.PngInfo):
    remainder = len(dna) % K
    if remainder != 0:
        dna += 'A' * (K - remainder)  # Pad the end

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
        max_dim = 10000  # Just a safeguard
        scaled_width = width * scale
        scaled_height = height * scale
        if scaled_width > max_dim or scaled_height > max_dim:
            raise ValueError(f"Scale too large. Resulting image would be {scaled_width}x{scaled_height}, exceeding {max_dim}px limit.")
        img = img.resize((scaled_width, scaled_height), Image.NEAREST)

    # Add scale factor metadata
    meta = PngImagePlugin.PngInfo()
    meta.add_text("scale_factor", str(scale))
    return img, meta

def decode_pixel_to_kmer(r, g, b, K=12) -> str:
    r_bits = f"{r:08b}"
    g_bits = f"{g:08b}"
    b_bits = f"{b:08b}"
    full_bits = r_bits + g_bits + b_bits
    kmer = ''
    for i in range(K):
        base_bits = full_bits[i*2:(i*2)+2]
        kmer += BIT_TO_BASE[base_bits]
    return kmer

def decode_image_to_sequence(img: Image.Image, K: int = 12) -> str:
    scale_factor_str = img.text.get("scale_factor", "1")
    scale_factor = int(scale_factor_str)

    width, height = img.size
    if scale_factor > 1:
        original_width = width // scale_factor
        original_height = height // scale_factor

        pixel_data = list(img.getdata())
        original_pixels = []
        for y in range(original_height):
            for x in range(original_width):
                px = pixel_data[(y * scale_factor) * width + (x * scale_factor)]
                original_pixels.append(px)
    else:
        original_pixels = list(img.getdata())

    decoded_seq = ""
    for p in original_pixels:
        r, g, b = p
        kmer = decode_pixel_to_kmer(r, g, b, K)
        decoded_seq += kmer

    return decoded_seq

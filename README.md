# DNA-to-Color Encoder

This Streamlit application encodes a DNA sequence into an RGB image. It uses a K-mer approach (default K=12) to convert chunks of the DNA sequence into a unique 24-bit color (RGB) and then arranges these colors into a visual representation.

## Features

- Input a DNA sequence directly via a text area or upload a FASTA or TXT file containing a FASTA-formatted sequence.
- Convert the sequence into an image where each 12-base segment corresponds to a single pixel.
- Automatically attempts to form a square image.
- Resize the image for better visual clarity.

## Requirements

- Python 3.7 or newer
- Dependencies listed in `requirements.txt`:
  - `streamlit`
  - `pillow`

Install dependencies:
```bash
pip install -r requirements.txt

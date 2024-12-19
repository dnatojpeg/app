# DNA-to-Color Encoder/Decoder
[https://dnacolor.streamlit.app](https://dnacolor.streamlit.app)

This Streamlit application encodes DNA sequences into a color-coded PNG image and can also decode the image back into the original DNA sequence. It uses a K-mer based encoding scheme (default K=12) where each pixel represents a 12-base segment.

## Features

- **Generate Mode**:  
  Upload or paste a FASTA-formatted DNA sequence and create a PNG image that encodes the sequence.  
  You can choose a scaling factor to enlarge the image for visualization, but decoding works best if scaling is kept at 1.

- **Convert from PNG Mode**:  
  Upload a previously generated PNG image to decode and recover the original DNA sequence.  
  If the image was scaled, the app uses embedded metadata to correctly downsample and decode.

## How to Use

1. Go to: [https://dnacolor.streamlit.app](https://dnacolor.streamlit.app)
2. Select **Generate** mode to encode a sequence into PNG:
   - Paste a sequence or upload a `.fasta`/`.fa`/`.txt` file.
   - Adjust the scaling if desired (note that scaling > 1 complicates decoding).
   - Click **Submit** to view and download the resulting PNG.
3. Select **Convert from PNG** mode to decode:
   - Upload the encoded PNG.
   - Click **Decode** to see and download the recovered DNA sequence.

## Requirements

If running locally:
- Python 3.7+
- `streamlit`
- `pillow`

Install dependencies:
```bash
pip install -r requirements.txt

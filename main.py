import streamlit as st
from utils import parse_fasta
from image_encoder import encode_sequence_to_image, decode_image_to_sequence
from io import BytesIO
from PIL import Image

st.set_page_config(layout="wide")
st.sidebar.title("DNA to Color Encode/Decode (PNG)")

mode = st.sidebar.selectbox("Mode", ["Generate", "Convert from PNG"])

if mode == "Generate":
    st.sidebar.write("**Provide DNA sequence (FASTA):**")
    fasta_sequence = st.sidebar.text_area("Paste FASTA sequence:")
    fasta_file = st.sidebar.file_uploader("Or upload FASTA/TXT:", type=["fasta", "fa", "txt"])

    # Slider for scaling factor
    scale = st.sidebar.slider("Scaling factor (large values = bigger image but not directly decodable)", 
                              min_value=1, max_value=1000000, step=250, value=1)
    st.sidebar.caption("Note: If you set scale > 1, decoding directly requires correction.\nKeep scale=1 if you plan to decode later.")

    submit = st.sidebar.button("Submit")

    if submit:
        dna = ""
        if fasta_file is not None:
            file_content = fasta_file.read().decode('utf-8')
            dna = parse_fasta(file_content)
        else:
            if fasta_sequence.strip():
                dna = parse_fasta(fasta_sequence)
            else:
                st.error("Please provide a sequence either via text or file.")
                st.stop()

        if len(dna) < 12:
            st.error("Sequence too short. Need at least 12 bases.")
            st.stop()

        img, meta = encode_sequence_to_image(dna, K=12, scale=scale)

        # Save image with metadata into memory
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG", pnginfo=meta)
        img_buffer.seek(0)

        # Display image
        st.image(img, caption=f"Encoded DNA Image (PNG) [Scale: {scale}]")

        # Provide download button
        st.download_button(
            label="Download PNG",
            data=img_buffer,
            file_name="encoded_image.png",
            mime="image/png"
        )

elif mode == "Convert from PNG":
    st.sidebar.write("**Upload PNG image to decode:**")
    png_file = st.sidebar.file_uploader("Upload PNG:", type=["png"])
    submit_png = st.sidebar.button("Decode")

    if submit_png:
        if png_file is None:
            st.error("Please upload a PNG file.")
            st.stop()

        # Load image from memory
        img = Image.open(png_file)
        decoded_seq = decode_image_to_sequence(img, K=12)

        st.write("**Decoded Sequence:**")
        st.text(decoded_seq)

        # Provide a download button for the decoded FASTA
        fasta_content = f">decoded_sequence\n{decoded_seq}\n"
        st.download_button(
            label="Download Decoded FASTA",
            data=fasta_content,
            file_name="decoded_sequence.fa",
            mime="text/plain"
        )

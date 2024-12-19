import streamlit as st
from utils import parse_fasta
from image_encoder import encode_sequence_to_image, decode_image_to_sequence
from io import BytesIO

st.set_page_config(layout="wide")
st.sidebar.title("DNA to Color Encoder/Decoder")

mode = st.sidebar.selectbox("Mode", ["Generate", "Convert from PNG"])

if mode == "Generate":
    st.sidebar.write("**Provide DNA sequence (FASTA):**")
    fasta_sequence = st.sidebar.text_area("Paste FASTA sequence:")
    fasta_file = st.sidebar.file_uploader("Or upload FASTA/TXT:", type=["fasta", "fa", "txt"])
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

        img = encode_sequence_to_image(dna, K=12, scale=10)

        # Display image
        st.image(img, caption="Encoded DNA Image (PNG)")

        # Provide download button
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

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
        from PIL import Image
        img = Image.open(png_file)
        decoded_seq = decode_image_to_sequence(img, K=12)
        
        st.write("**Decoded Sequence:**")
        st.text(decoded_seq)

        # Optionally provide a way to download decoded sequence as FASTA
        fasta_content = f">decoded_sequence\n{decoded_seq}\n"
        st.download_button(
            label="Download Decoded FASTA",
            data=fasta_content,
            file_name="decoded_sequence.fa",
            mime="text/plain"
        )

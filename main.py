import streamlit as st
from utils import parse_fasta
from image_encoder import encode_sequence_to_image

st.set_page_config(layout="wide")
st.sidebar.title("DNA to Color Encoder")

fasta_sequence = st.sidebar.text_area("Paste FASTA sequence:")
fasta_file = st.sidebar.file_uploader("Or upload a FASTA file (optional):", type=["fasta","fa", 'txt'])

submit = st.sidebar.button("Submit")

if submit:
    dna = ""
    # Determine DNA source
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

    # Encode to image (using K=12 by default)
    img = encode_sequence_to_image(dna, K=12)
    st.image(img, caption="Encoded DNA Image")

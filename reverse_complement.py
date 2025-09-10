import streamlit as st
import pandas as pd
import re
import altair as alt

def run():
    
    col1, col2 = st.columns([1, 5])  # Adjust ratio as needed

    with col1:
        st.image("sanofi_2.png", width=400)  # Adjust width as needed

    st.set_page_config(
        page_title="Reverse Complement",
        page_icon="dna_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # st.markdown(
    #     """
    #     <style>
    #     body {
    #         background-color: #ACE1AF;
    #     }
    #     .stApp {
    #         background-color: #ACE1AF;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    st.title("Reverse Complement DNA/RNA")

    # Utility functions
    def clean_string(s):
        return re.sub(r'[^A-Za-z0-9]', '', s)

    def reverse_complement_dna(seq_DNA):
        seq_DNA = clean_string(seq_DNA).upper()
        complement_dna = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        comp_seq = ''.join(complement_dna.get(base, '') for base in seq_DNA)
        return comp_seq[::-1]

    def reverse_complement_rna(seq_RNA):
        seq_RNA = clean_string(seq_RNA).upper()
        complement_rna = {'A': 'U', 'U': 'A', 'C': 'G', 'G': 'C'}
        comp_seq = ''.join(complement_rna.get(base, '') for base in seq_RNA)
        return comp_seq[::-1]

    def create_nucleotide_summary(seq, title, nucleotides):
        seq = seq.upper()
        len_num = len(seq)
        if len_num > 0:
            values = [(base, (seq.count(base) / len_num) * 100) for base in nucleotides]
            df = pd.DataFrame(values, columns=['Nucleotide', 'Percent'])

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Nucleotide', sort=nucleotides),
                y='Percent',
                color='Nucleotide',
                tooltip=['Nucleotide', 'Percent']
            ).properties(
                title=title,
                width=800,
                height=300
            )
            st.altair_chart(chart, use_container_width=False)

    # UI layout
    #col1, col2 = st.columns(2)

    with st.container(border=True):
        seq_DNA = st.text_input("Enter a DNA/RNA sequence (case insensitive and spaces + special characters ignored):")
        seq_DNA = seq_DNA.upper()
        if seq_DNA:
            if 'T' in seq_DNA:
                create_nucleotide_summary(seq_DNA, "Original DNA Nucleotide Frequency", ['A', 'T', 'C', 'G'])
                result = reverse_complement_dna(seq_DNA)
                st.write("Reverse Complement DNA:", result)
                create_nucleotide_summary(result, "Reverse Complement DNA Nucleotide Frequency", ['A', 'T', 'C', 'G'])
            elif 'U' in seq_DNA:
                create_nucleotide_summary(seq_DNA, "Original RNA Nucleotide Frequency", ['A', 'U', 'C', 'G'])
                result = reverse_complement_rna(seq_DNA)
                st.write("Reverse Complement RNA:", result)
                create_nucleotide_summary(result, "Reverse Complement RNA Nucleotide Frequency", ['A', 'U', 'C', 'G'])
            else:
                create_nucleotide_summary(seq_DNA, "Original Sequence Nucleotide Frequency", ['A', 'U/T', 'C', 'G'])
                result1 = reverse_complement_dna(seq_DNA)
                result2 = reverse_complement_rna(seq_DNA)
                st.write("Reverse Complement DNA:", result1)
                create_nucleotide_summary(result1, "Reverse Complement DNA Nucleotide Frequency", ['A', 'T', 'C', 'G'])
                st.write("Reverse Complement RNA:", result2)
                create_nucleotide_summary(result2, "Reverse Complement RNA Nucleotide Frequency", ['A', 'U', 'C', 'G'])

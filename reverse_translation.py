import streamlit as st
import re
import pandas as pd
from collections import defaultdict

def run():

    st.markdown(
            """
            <style>
            body {
                background-color: #DBF3FA;
            }
            .stApp {
                background-color: #DBF3FA;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    col1, col2 = st.columns([1, 5])  # Adjust ratio as needed

    with col1:
        st.image("sanofi_2.png", width=400)  # Adjust width as needed
        
    st.set_page_config(
        page_title="Reverse Translation",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Reverse Translation")

    # Function to clean input
    def clean_string(s):
        return re.sub(r'[^A-Za-z]', '', s.upper())

    # Codon table
    codon_table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    }

    # Reverse translation function
    def reverse_translate(seq_aa):
        aa_to_codons = defaultdict(list)
        for codon, aa in codon_table.items():
            aa_to_codons[aa].append(codon)

        codon_options = [aa_to_codons[aa] for aa in seq_aa]
        example_sequence = [options[0] for options in codon_options]

        max_options = max(len(options) for options in codon_options)
        table_data_dna = []
        table_data_rna = []

        for i in range(1, max_options):  # Skip first codon (example)
            row_dna = []
            row_rna = []
            for options in codon_options:
                if len(options) > i:
                    codon_dna = options[i]
                    codon_rna = codon_dna.replace("T", "U")
                    row_dna.append(codon_dna)
                    row_rna.append(codon_rna)
                else:
                    row_dna.append("")
                    row_rna.append("")
            table_data_dna.append(row_dna)
            table_data_rna.append(row_rna)

        table_data_dna.insert(0, example_sequence)
        table_data_rna.insert(0, [codon.replace("T", "U") for codon in example_sequence])

        columns = [f"Position {i+1}" for i in range(len(example_sequence))]
        df_dna = pd.DataFrame(table_data_dna, columns=columns)
        df_rna = pd.DataFrame(table_data_rna, columns=columns)

        dna_seq = ''.join(example_sequence)
        rna_seq = dna_seq.replace("T", "U")

        return dna_seq, rna_seq, df_dna, df_rna

    # UI layout
    seq_aa = st.text_input("Enter a Protein sequence (case insensitive and spaces + special characters ignored):")
    seq_aa = clean_string(seq_aa)

    if seq_aa:
        dna_seq, rna_seq, df_dna, df_rna = reverse_translate(seq_aa)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Example DNA Sequence")
            st.code(dna_seq)

        with col2:
            st.subheader("Example RNA Sequence")
            st.code(rna_seq)

        st.subheader("DNA Codon Options at Variable Positions")
        st.dataframe(df_dna)

        st.subheader("RNA Codon Options at Variable Positions")
        st.dataframe(df_rna)

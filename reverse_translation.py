import streamlit as st
import re

def run():

    st.set_page_config(
        page_title="Reverse Translation",
        page_icon= "dna_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Streamlit UI
    st.title("Reverse Translation")
    # Streamlit UI

    # -----------------------------------------------------------------------------
    # Functions:

    def clean_string(s):
        # Remove all non-alphanumeric characters (including spaces)
        return re.sub(r'[^A-Za-z0-9]', '', s)

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

    rna_codon_table = {codon.replace('T', 'U'): aa for codon, aa in codon_table.items()}

    def protein_to_dna(seq_aa):
        protein = []
        for i in range(0, len(seq_DNA)-2, 3):
            codon = seq_DNA[i:i+3].upper()
            amino_acid= codon_table.get(codon, "X")
            protein.append(amino_acid)
        return ''.join(protein)
        
    def protein_to_rna(seq_aa):
        protein = []
        for i in range(0, len(seq_RNA)-2, 3):
            codon = seq_RNA[i:i+3].upper()
            amino_acid= rna_codon_table.get(codon, "X")
            protein.append(amino_acid)
        return ''.join(protein)

    # -----------------------------------------------------------------------------
    # Process and display result
    with st.container(border=True):
        st.write("For a DNA Sequence:")
        seq_aa_DNA = st.text_input("Enter an Amino Acid sequence:")
        seq_DNA = clean_string(seq_DNA)
        if len(seq_DNA) % 3 == 0:
            result = translate_dna_to_protein(seq_DNA)
            st.write("Protein Translation of DNA:", result)
        else:
            st.write("Please enter a string that has a length divisible by 3")

    with st.container(border=True):
        st.write("For an RNA Sequence:")
        seq_aa_RNA = st.text_input("Enter an Amino Acid Sequence:")
        seq_RNA = clean_string(seq_RNA)
        if len(seq_RNA) % 3 ==0:
            result = translate_rna_to_protein(seq_RNA)
            st.write("Protein Translation of RNA:", result)
        else:
            st.write("Please enter a string that has a length divisible by 3")




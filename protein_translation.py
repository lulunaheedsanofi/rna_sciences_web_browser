import streamlit as st
import re
import pandas as pd
import altair as alt

def run():
    st.set_page_config(
        page_title="Protein Translation",
        page_icon="dna_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Protein Translation")

    def clean_string(s):
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

    def translate_dna_to_protein(seq_DNA):
        protein = []
        for i in range(0, len(seq_DNA)-2, 3):
            codon = seq_DNA[i:i+3].upper()
            amino_acid = codon_table.get(codon, "X")
            protein.append(amino_acid)
        return ''.join(protein)

    def translate_rna_to_protein(seq_RNA):
        protein = []
        for i in range(0, len(seq_RNA)-2, 3):
            codon = seq_RNA[i:i+3].upper()
            amino_acid = rna_codon_table.get(codon, "X")
            protein.append(amino_acid)
        return ''.join(protein)

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
                width=600,
                height=400
            )
            st.altair_chart(chart, use_container_width=False)

    # UI
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            seq_DNA = st.text_input("Enter a DNA sequence:")
            seq_DNA = clean_string(seq_DNA)
            if len(seq_DNA) % 3 == 0:
                result = translate_dna_to_protein(seq_DNA)
                st.write("Protein Translation of DNA:", result)
                create_nucleotide_summary(seq_DNA, "DNA Nucleotide Frequency", ['A', 'T', 'C', 'G'])
            else:
                st.write("Please enter a string that has a length divisible by 3")

    with col2:
        with st.container(border=True):
            seq_RNA = st.text_input("Enter an RNA sequence:")
            seq_RNA = clean_string(seq_RNA)
            if len(seq_RNA) % 3 == 0:
                result = translate_rna_to_protein(seq_RNA)
                st.write("Protein Translation of RNA:", result)
                create_nucleotide_summary(seq_RNA, "RNA Nucleotide Frequency", ['A', 'U', 'C', 'G'])
            else:
                st.write("Please enter a string that has a length divisible by 3")
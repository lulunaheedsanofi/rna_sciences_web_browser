import streamlit as st
def run():
    # Wallace rule for short sequences
    def wallace_rule(seq):
        seq = seq.upper()
        A = seq.count('A')
        T = seq.count('T')
        G = seq.count('G')
        C = seq.count('C')
        return 2 * (A + T) + 4 * (G + C)

    # Nearest-neighbor method for longer sequences
    def nearest_neighbor(seq):
        seq = seq.upper()
        R = 1.987  # universal gas constant in cal/(K*mol)
        delta_H = 0
        delta_S = 0

        nn_params = {
            'AA': (-7.9, -22.2), 'TT': (-7.9, -22.2),
            'AT': (-7.2, -20.4), 'TA': (-7.2, -21.3),
            'CA': (-8.5, -22.7), 'TG': (-8.5, -22.7),
            'GT': (-8.4, -22.4), 'AC': (-8.4, -22.4),
            'CT': (-7.8, -21.0), 'AG': (-7.8, -21.0),
            'GA': (-8.2, -22.2), 'TC': (-8.2, -22.2),
            'CG': (-10.6, -27.2), 'GC': (-9.8, -24.4),
            'GG': (-8.0, -19.9), 'CC': (-8.0, -19.9)
        }

        for i in range(len(seq) - 1):
            pair = seq[i:i+2]
            if pair in nn_params:
                h, s = nn_params[pair]
                delta_H += h
                delta_S += s

        delta_H *= 1000  # convert to cal/mol
        salt = st.sidebar.slider("Salt Correction (mol/L)", 0.0001, 0.05, 0.0125)
        Tm = (delta_H / (delta_S + R * salt)) - 273.15
        return round(Tm, 2)

    # Streamlit interface
    st.set_page_config(page_title="Custom Tm Calculator", layout="centered")
    st.title("DNA Melting Temperature (Tm) Calculator")

    sequence = st.text_input("Enter DNA sequence:", "")
    if sequence:
        if len(sequence) < 14:
            tm = wallace_rule(sequence)
            st.write(f"**Tm (Wallace Rule):** {tm} °C")
        else:
            nearest_neighbor(sequence)
            st.write(f"**Tm (Nearest-Neighbor Method):** {tm} °C")
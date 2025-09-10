import streamlit as st
import umi_pipeline
import project_dashboard
import reverse_complement
import protein_translation
import production_summary
import neb_tm_calculator
import reverse_translation

# Page configuration
st.set_page_config(
    page_title="Sanofi RNA Sciences Hub",
    layout="wide",
    page_icon="dna_logo.png",
    initial_sidebar_state="expanded"
)

# Inject custom CSS


st.markdown("""
    <style>
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #4B0082;
            padding: 20px;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Main content area styling */
        [data-testid="stAppViewContainer"] > div:first-child {
            background-color: #DBF3FA;
            padding: 2em;
        }

        /* Optional: style main content text only */
        [data-testid="stAppViewContainer"] > div:first-child * {
            color: black !important;
        }

        /* Expander styling */
        div[data-testid="stExpander"] {
            background-color: #4B0082 !important;
            border: none !important;
        }

        div[data-testid="stExpander"] > details {
            background-color: #4B0082 !important;
        }

        div[data-testid="stExpander"] summary {
            background-color: #4B0082 !important;
            color: white !important;
            font-weight: bold;
        }

        div[data-testid="stExpander"] div[aria-expanded="true"] {
            background-color: #4B0082 !important;
        }

        /* Button styling */
        button {
            background-color: #6A0DAD !important;
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
            padding: 0.5em 1em !important;
            margin-top: 5px;
        }

        button:hover {
            background-color: #8A2BE2 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)



# Initialize session state
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None

# Sidebar layout with expanders and buttons
with st.sidebar:
    st.image("rna_sciences_hub_v4.png", width=400)
    st.markdown("---")
# from PIL import Image

# with st.sidebar:
#     img = Image.open("rna_sciences_hub_v1.png")
#     resized_img = img.resize((600, 100))  # width, height in pixels
#     st.image(resized_img)
#     st.markdown("---")




    with st.expander("Quick Tools", expanded=False):
        if st.button("Reverse Complement"):
            st.session_state.selected_section = "Reverse Complement"
        if st.button("Protein Translation"):
            st.session_state.selected_section = "Protein Translation"
        if st.button("Reverse Translation"):
            st.session_state.selected_section = "Reverse Translation"

    with st.expander("Applications", expanded=False):
        if st.button("UMI Pipeline Results"):
            st.session_state.selected_section = "UMI Pipeline Results"

    with st.expander("Dashboards", expanded=False):
        if st.button("Production Summary"):
            st.session_state.selected_section = "Production Summary"
        if st.button("Project Tracker"):
            st.session_state.selected_section = "Project Tracker"

# Main content area
if st.session_state.selected_section == "Reverse Complement":
    reverse_complement.run()
elif st.session_state.selected_section == "Protein Translation":
    protein_translation.run()
elif st.session_state.selected_section == "Reverse Translation":
    reverse_translation.run()
elif st.session_state.selected_section == "UMI Pipeline Results":
    umi_pipeline.run()
elif st.session_state.selected_section == "Production Summary":
    production_summary.run()
elif st.session_state.selected_section == "Project Tracker":
    project_dashboard.run()
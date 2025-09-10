
import streamlit as st
import umi_pipeline
import project_dashboard
import reverse_complement
import protein_translation
import production_summary
import neb_tm_calculator


# Page configuration
st.set_page_config(
    page_title="Sanofi RNA Sciences Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for sidebar and main content
st.markdown("""
    <style>
        /* Sanofi purple sidebar */
        [data-testid="stSidebar"] {
            background-color: #4B0082; /* Sanofi purple */
        }

        /* Lilac purple main content */
        .main {
            background-color: #E6DAF5; /* Lilac purple */
        }

        /* Optional: make sidebar text white for contrast */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] .stSelectbox label {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar layout for navigation
with st.sidebar:
    st.image("rna_sciences_logo_v1.png", width=700)
    st.markdown("---")

    section = st.selectbox("Select a category:", ["Quick Tools", "Applications", "Dashboards"])

    if section == "Quick Tools":
        tool = st.selectbox("Choose a tool:", ["Reverse Complement", "Protein Translation", "NEB Tm Calculator"])
    elif section == "Applications":
        app = st.selectbox("Choose an application:", ["UMI Pipeline Results"])
    elif section == "Dashboards":
        dashboard = st.selectbox("Choose a dashboard:", ["Production Summary", "Project Tracker"])

# Main content area

if section == "Quick Tools":
    if tool == "Reverse Complement":
        reverse_complement.run()
    elif tool == "Protein Translation":
        protein_translation.run()
    elif tool == "NEB Tm Calculator":
        neb_tm_calculator.run()

elif section == "Applications":
    if app == "UMI Pipeline Results":
        umi_pipeline.run()

elif section == "Dashboards":
    if dashboard == "Production Summary":
        production_summary.run()
    elif dashboard == "Project Tracker":
        project_dashboard.run()

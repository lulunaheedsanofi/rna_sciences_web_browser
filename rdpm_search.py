import streamlit as st
import pandas as pd

def run():
    st.set_page_config(
        page_title="RDPM Search",
        page_icon="dna_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

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


    st.title("RDPM Search Engine")


    df = pd.read_excel('pDNA_mRNAD_24-25.xlsx')
    selected_columns = ['pDNA Notebook Entry', 'pDNA Notebook Project Code', 'mRNAD Project Code']
    df_filtered = df[selected_columns]

    # Remove rows where any column contains the string "null"
    df_cleaned = df_filtered.dropna()
    df_unique = df_cleaned.drop_duplicates()
    rows, columns = df_unique.shape

    rdpm_codes = []
    descriptions = []
    mrnad_rdpm_codes = []
    mrnad_descriptions = []

    for n in range(rows):
        curr_code = df_unique.iloc[n, 1] 
        first_part = curr_code.split("_")[0]
        rdpm_codes.append(first_part)

        mrnad_curr_code = df_unique.iloc[n,2]
        m_first_part = mrnad_curr_code.split("_")[0]
        mrnad_rdpm_codes.append(m_first_part)
        
        remainder = "_".join(curr_code.split("_")[1:])
        descriptions.append(remainder) 

        m_remainder = "_".join(mrnad_curr_code.split("_")[1:])
        mrnad_descriptions.append(m_remainder) 

    cleaned_descriptions = [item.replace("_v_", "") for item in descriptions]
    mrnad_cleaned_descriptions = [item.replace("_v_", "") for item in mrnad_descriptions]

    final_df = pd.DataFrame({
        'Ticket Name': df_unique['pDNA Notebook Entry'],
        'pDNA RDPM Code': rdpm_codes,
        #'pDNA Description': cleaned_descriptions,
        'mRNAD RDPM Code' : mrnad_rdpm_codes,
        'Description' : cleaned_descriptions
    })

    final_df['Ticket Name'] = final_df['Ticket Name'].str.upper()
    final_df['pDNA RDPM Code'] = final_df['pDNA RDPM Code'].str.upper()
    #final_df['pDNA Description'] = final_df['pDNA Description'].str.upper()
    final_df['mRNAD RDPM Code'] = final_df['mRNAD RDPM Code'].str.upper()
    final_df['Description'] = final_df['Description'].str.upper()

    # Utility functions
    def display_rdpm_table(df,keyword):
        keyword_df = df[df.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]
        return keyword_df

    
    # UI layout
    #col1, col2 = st.columns(2)

    with st.container(border=True):
        keyword = st.text_input("Enter a Keyword to Search Through Ticket IDs, RDPM Codes, and Descriptions (case insensitive)")
        if keyword:
            input = keyword.upper()
            result = display_rdpm_table(final_df,input)
            st.dataframe(result)
        else:
            st.dataframe(final_df)
        
        
        
          
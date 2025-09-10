import streamlit as st
# import benchling_sdk
# from benchling_sdk.benchling import Benchling
# from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2
# import os

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
def run():

    st.set_page_config(
        page_title="Project Dashboard",
        page_icon= "dna_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
            """
            <style>
            body {
                background-color: #89CFF0;
            }
            .stApp {
                background-color: #89CFF0;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    # Streamlit UI
    st.title("Project Dashboard")


    def run_benchling_request(work_request_ID):# Or hardcode for testing
        BENCHLING_CLIENT_ID = "b8adcd17-acd1-4296-84e4-d82eb1bbdc95"
        BENCHLING_CLIENT_SECRET = "cs_q-EqKmarqkZTq9Zm9ce3ylX-d4JJvCNEx-XFIgKmgIQ"
        BENCHLING_URL = "https://sanofi.benchling.com"

        auth_method = ClientCredentialsOAuth2(
            client_id=BENCHLING_CLIENT_ID,
            client_secret=BENCHLING_CLIENT_SECRET
        )

        benchling_client = Benchling(url=BENCHLING_URL, auth_method=auth_method)


        client_id = "b8adcd17-acd1-4296-84e4-d82eb1bbdc95"
        client_secret = "cs_q-EqKmarqkZTq9Zm9ce3ylX-d4JJvCNEx-XFIgKmgIQ"
        token_url = "https://sanofi.benchling.com/api/v2/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = requests.post(token_url, data=data)
        token_data = response.json()

        access_token = token_data.get("access_token")
        print(access_token)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        ########
        response = requests.get(
            "https://sanofi.benchling.com/api/v2/dna-sequences",
            headers=headers,
            params={"name": work_request_ID}  # or use displayId
        )

        seq = response.json().get("dnaSequences", [])
        return seq
    
    with st.container(border=True):
        work_request_ID = st.text_input("Enter a Work Request ID:")

    # -----------------------------------------------------------------------------
    # Process and display result

    result = run_benchling_request(work_request_ID)

    with st.container(border=True):
        st.write("Results:", result)

   
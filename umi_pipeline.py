
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import matplotlib.pyplot as plt
import altair as alt

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
    
    st.set_page_config(
        page_title="UMI Pipeline",
        page_icon= "dna_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    col1, col2 = st.columns([1, 5])  # Adjust ratio as needed

    with col1:
        st.image("sanofi_2.png", width=400)  # Adjust width as needed
    # with col2:
    #     st.markdown("## Welcome to RNA Sciences Hub")


    # Streamlit UI
    st.title("UMI Pipeline Results")

    # -----------------------------------------------------------------------------
    # Functions:

    def read_data(uploaded_file):
        try:
            content = uploaded_file.read().decode("utf-8")
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, delimiter="\t")
            if df.empty or df.columns.size == 0:
                raise ValueError("No columns found. File may not be tab-delimited or may be empty.")
            return df
        except Exception as e:
            st.error(f"Failed to read file: {e}")
            return None

    def create_plots_for_all_samples(dataframes):
        hist_metrics = ['Score', 'Bin_size', 'Quality', 'Insertions', 'Deletions', 'Mismatches', 'Errors']
        bar_metrics = ['Perfect']
        font_size = 16

        for curr_metric in hist_metrics:
            st.subheader(f"{curr_metric}")
            cols = st.columns(len(dataframes))
            for i, (sample_name, df) in enumerate(dataframes.items()):
                chart_data = pd.DataFrame({curr_metric: df[curr_metric]})
                hist = alt.Chart(chart_data).mark_bar(color='#7A00E6').encode(
                    x=alt.X(f'{curr_metric}:Q', bin=alt.Bin(maxbins=50), title=curr_metric),
                    y=alt.Y('count()', title='Number of UMIs')
                ).properties(
                    title=f'{sample_name}',
                    width=300,
                    height=250
                )
                with cols[i]:
                    st.altair_chart(hist, use_container_width=True)

        for curr_metric in bar_metrics:
            st.subheader(f"Bar Chart: {curr_metric}")
            cols = st.columns(len(dataframes))
            for i, (sample_name, df) in enumerate(dataframes.items()):
                perfect = df[curr_metric]
                count_yes = (perfect == 'yes').sum()
                count_no = (perfect == 'no').sum()
                categories = ['Perfect', 'Not Perfect']
                values = [count_yes, count_no]
                total = sum(values)
                percents = [(v / total) * 100 if total > 0 else 0 for v in values]

                bar_data = pd.DataFrame({
                    'Sequence Type': categories,
                    'Number of UMIs': values,
                    'Percentage': [f"{p:.1f}%" for p in percents]
                })

                bar_chart = alt.Chart(bar_data).mark_bar(color='#7A00E6').encode(
                    x=alt.X('Sequence Type:N', title='Sequence Type'),
                    y=alt.Y('Number of UMIs:Q', title='Number of UMIs')
                )

                text = alt.Chart(bar_data).mark_text(
                    align='center',
                    baseline='bottom',
                    dy=-5,
                    fontSize=font_size
                ).encode(
                    x='Sequence Type:N',
                    y='Number of UMIs:Q',
                    text='Percentage:N'
                )

                final_chart = (bar_chart + text).properties(
                    title=f'{sample_name}',
                    width=300,
                    height=300
                )

                with cols[i]:
                    st.altair_chart(final_chart, use_container_width=True)

    def create_error_plot(df, sample_name):
        filtered_df_perfect = df[df['Perfect'] == 'yes']
        first_row_perfect = filtered_df_perfect.iloc[[0]]
        len_perfect = first_row_perfect['Length'].values[0]

        filtered_df_binsize = df[df['Bin_size'] >= 50]
        curr_UMIs = filtered_df_binsize.shape[0]

        filtered_df_binsize_mismatches = filtered_df_binsize[filtered_df_binsize['Mismatches'] >= 1]
        curr_mismatches = filtered_df_binsize_mismatches['Mismatches'].sum()

        error_rate = curr_mismatches / (curr_UMIs * len_perfect)

        error_df = {
            "Number of UMIs w/ Bin Size >= 50": curr_UMIs,
            "Total Number of Mismatches": curr_mismatches,
            "Total Basepairs Sequenced": curr_UMIs * len_perfect,
            "Gene Length": len_perfect,
            "Error Rate": error_rate
        }

        perfect_UMI_rows = filtered_df_perfect.iloc[[0, 1]]
        df_sorted = df.sort_values(by=['Mismatches', 'Score'], ascending=[False, False])
        confidence_reads = df_sorted.dropna(subset=['Variant_code'])
        confidence_reads = confidence_reads[confidence_reads['Errors'] == 1]
        highest_mutant_rows = confidence_reads.iloc[[0, 1]]

        with st.container(border=True):
            st.write(f"Perfect UMI - {sample_name}")
            st.dataframe(perfect_UMI_rows)
        with st.container(border=True):
            st.write(f"Mutant UMI - {sample_name}")
            st.dataframe(highest_mutant_rows)
        with st.container(border=True):
            st.table(error_df)

        chart_data = pd.DataFrame({
            'Sample': [sample_name],
            'Error Rate': [error_rate]
        })

        chart = alt.Chart(chart_data).mark_bar(color='orange').encode(
            x=alt.X('Sample:N', title='Sample ID'),
            y=alt.Y('Error Rate:Q', title='Error Rate')
        ) + alt.Chart(chart_data).mark_text(
            align='center',
            baseline='middle',
            dy=10,
            fontSize=12
        ).encode(
            x='Sample:N',
            y='Error Rate:Q',
            text=alt.Text('Error Rate:Q', format='.8f')
        )

        with st.container(border=True):
            st.altair_chart(chart, use_container_width=True)

    # --- Main App ---
    with st.container(border=True):
        uploaded_files = st.file_uploader("Upload one or more summary files", accept_multiple_files=True)

    if uploaded_files:
        dataframes = {}
        for uploaded_file in uploaded_files:
            df = read_data(uploaded_file)
            if df is not None:
                sample_name = uploaded_file.name.split("_summary")[0]
                dataframes[sample_name] = df

        if dataframes:
            create_plots_for_all_samples(dataframes)
            for sample_name, df in dataframes.items():
                create_error_plot(df, sample_name)






        

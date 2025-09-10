
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import matplotlib.pyplot as plt

def run():
    
    st.set_page_config(
        page_title="UMI Pipeline",
        page_icon= "dna_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # st.markdown(
    #         """
    #         <style>
    #         body {
    #             background-color: #C8A2C8;
    #         }
    #         .stApp {
    #             background-color: #C8A2C8;
    #         }
    #         </style>
    #         """,
    #         unsafe_allow_html=True
    #     )


    # Streamlit UI
    st.title("UMI Pipeline Results")

    # -----------------------------------------------------------------------------
    # Functions:

    def read_data(uploaded_file):
        try:
            # Read and preview raw content
            content = uploaded_file.read().decode("utf-8")
            #st.text_area("Raw File Preview", content[:1000])  # Show first 1000 characters

            # Reset file pointer so pandas can read it again
            uploaded_file.seek(0)

            # Try reading as tab-delimited
            df = pd.read_csv(uploaded_file, delimiter="\t")

            # Check if DataFrame is valid
            if df.empty or df.columns.size == 0:
                raise ValueError("No columns found. File may not be tab-delimited or may be empty.")

            return df

        except Exception as e:
            st.error(f"Failed to read file: {e}")
            return None

    def create_plots(df):
        hist_metrics = ['Score', 'Bin_size', 'Quality', 'Insertions', 'Deletions', 'Mismatches', 'Errors']
        bar_metrics = ['Perfect']

        total_plots = len(hist_metrics) + len(bar_metrics)
        cols = 4
        rows = (total_plots + cols - 1) // cols  # Calculate number of rows needed

        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), dpi=100)
        axes = axes.flatten()

        font_size = 16
        plot_index = 0
        sample_name = uploaded_file.name.split("_summary")[0]
        # Plot histograms
        for curr_metric in hist_metrics:
            ax = axes[plot_index]
            vals = df[curr_metric]
            counts, bins, patches = ax.hist(vals, bins=50, color='#7A00E6', edgecolor='white')
            ax.set_title(curr_metric + " " + sample_name, fontsize=font_size)
            ax.set_xlabel(curr_metric, fontsize=font_size)
            ax.set_ylabel('Number of UMIs', fontsize=font_size)
            ax.tick_params(axis='both', labelsize=font_size)
            ax.set_ylim(0, max(counts) + 20)
            plot_index += 1

        # Plot bar charts
        for curr_metric in bar_metrics:
            ax = axes[plot_index]
            perfect = df[curr_metric]
            count_yes = (perfect == 'yes').sum()
            count_no = (perfect == 'no').sum()
            categories = ['Perfect', 'Not Perfect']
            values = [count_yes, count_no]
            bars = ax.bar(categories, values, color='#7A00E6', edgecolor='white')
            ax.set_title(curr_metric + " " + sample_name, fontsize=font_size)
            ax.set_xlabel('Sequence Type', fontsize=font_size)
            ax.set_ylabel('Number of UMIs', fontsize=font_size)
            ax.tick_params(axis='both', labelsize=font_size)
            for b, bar in enumerate(bars):
                total = sum(values)
                perc = (values[b] / total) * 100 if total > 0 else 0
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, f"{perc:.1f}%", ha='center', fontsize=font_size)
            ax.set_ylim(0, max(values) + 20)
            plot_index += 1

        # Hide any unused subplots
        for i in range(plot_index, len(axes)):
            fig.delaxes(axes[i])

        plt.tight_layout()
        with st.container(border=True):
            st.pyplot(fig)

    def create_error_plot(df):
        # Calculate Error Rates for Samples using following criteria:
        ## Identify UMIs with bin sizes above or equal to 50
        ## Obtain number of Mismatches (only, do not pick UMIs that contain Insertions and Deletions)
        ## Add the number of Mismatches from all of the UMIs combined and divide by (# UMIs with bin size above or equal to 50 x length of MRNAD) to get Error Rate per Sample

        num_UMIs_binsize = [] # gathers number of UMIs with bin sizes >= 50 
        num_mismatches = [] # gathers number of UMIs with bin sizes >= 50 and with only mismatches
        sample_error_rates = []
        perfect_UMIs = []

        #ax = axes[0, 0]
    
        filtered_df_perfect = df[(df['Perfect'] == 'yes')] 
        first_row_perfect = filtered_df_perfect.iloc[[0]]
        len_perfect = first_row_perfect['Length'].values[0]

        filtered_df_binsize = df[(df['Bin_size'] >= 50)] # pick up only UMIs with bin sizes greater than or equal to 50
        curr_UMIs= filtered_df_binsize.shape[0]
        num_UMIs_binsize.append(curr_UMIs)
        
        filtered_df_binsize_mismatches = filtered_df_binsize[(filtered_df_binsize['Mismatches'] >= 1)] #Out of the filtered UMIs, choose only ones with mismatches
        curr_mismatches = filtered_df_binsize_mismatches['Mismatches'].sum()
        num_mismatches.append(curr_mismatches)
    
        error_rate = curr_mismatches/(curr_UMIs*len_perfect)
        sample_error_rates.append(error_rate)
        perfect_UMI = filtered_df_perfect['UMI'].iloc[[0]]
        perfect_UMIs.append(perfect_UMI)
        perfect_UMI_rows = filtered_df_perfect.iloc[[0,1]]

         ## Find highest ranking mutated UMI
        df_sorted = df.sort_values(by=['Mismatches', 'Score'], ascending=[False, False])
        confidence_reads = df_sorted.dropna(subset=['Variant_code'])
        confidence_reads = confidence_reads[(confidence_reads['Errors']==1)]
        highest_mutant_rows = confidence_reads.iloc[[0,1]]
        sample_name = uploaded_file.name.split("_summary")[0]
        # Create a figure and axis with appropriate size
        fig, ax = plt.subplots(figsize=(1, 2))

        # Plot the bar chart
        bars = ax.bar(sample_name, sample_error_rates, color='orange', edgecolor='white')
        sample_name = uploaded_file.name.split("_summary")[0]
        # Set titles and labels
        
        ax.set_title('Error Rates ' + sample_name, fontsize= 8)
        ax.set_xlabel('Sample ID', fontsize = 8)
        ax.set_ylabel('Error Rate', fontsize = 8)
        
        # Set tick label font sizes

        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)


        # Add value labels above each bar
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval * 0.5, f"{yval:.8f}", ha='center', va='bottom', fontsize=8)

        # Adjust layout and show plot
        plt.tight_layout()
        error_df = {
            "Number of UMIs w/ Bin Size >= 50" : curr_UMIs,
            "Total Number of Mismatches" : curr_mismatches,
            "Total Basepairs Sequenced" : curr_UMIs*len_perfect,
            "Gene Length" : len_perfect,
            "Error Rate" : error_rate
        }
        with st.container(border=True):
            st.write("Perfect UMI")
            st.dataframe(perfect_UMI_rows)
        with st.container(border=True):
            st.write("Mutant UMI")
            st.dataframe(highest_mutant_rows)
        with st.container(border=True):
            st.table(error_df)

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.pyplot(fig)

    # -----------------------------------------------------------------------------
    # Get user input

    # File uploader widget
    with st.container(border=True):
        uploaded_file = st.file_uploader("Please Choose a file")

    # -----------------------------------------------------------------------------
    # Process and display result

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Read the file content
        file_content = uploaded_file.read()
        st.text(f"File size: {uploaded_file.size} bytes")

        df = read_data(uploaded_file)
        plot_results = create_plots(df)
        error_results = create_error_plot(df)





    

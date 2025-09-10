import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
import altair as alt
from altair_saver import save
from io import BytesIO
import selenium
import vl_convert as vegalite_to_png



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
        page_title="Production Summary",
        page_icon= "dna_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Production Summary")

    
    def get_png_download_button(chart, filename, key):
        chart_json = chart.to_json()
        png_bytes = vegalite_to_png.vegalite_to_png(chart_json, scale=2)
        buffer = BytesIO(png_bytes)
        st.download_button(
            label=f"Download {filename}",
            data=buffer,
            file_name=filename,
            mime="image/png",
            key=key
        )

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
    
    def create_monthly_report(excel_sheet1, excel_sheet2):
        # Copy dataframes to avoid modifying originals
        df = excel_sheet1.copy()
        df = df[df['Flag'] != 0]
        df_CT = excel_sheet2.copy()

        # Convert relevant columns to datetime
        df['pDNA Created'] = pd.to_datetime(df['pDNA Created'], errors='coerce')
        df['pDNA Created.1'] = pd.to_datetime(df['pDNA Created.1'], errors='coerce')
        df['LDF Created'] = pd.to_datetime(df['LDF Created'], errors='coerce')
        df_CT['mRNA Created'] = pd.to_datetime(df_CT['mRNA Created'], errors='coerce')

        # Filter for years 2024 and 2025
        df = df[
            (df['pDNA Created'].dt.year.isin([2024, 2025])) &
            (df['pDNA Created.1'].dt.year.isin([2024, 2025])) &
            (df['LDF Created'].dt.year.isin([2024, 2025]))
        ]   
        df_CT = df_CT[df_CT['mRNA Created'].dt.year.isin([2024, 2025])]

        # Define categories with monthly counts
        categories = {
            'pDNA_Design': df['pDNA Created'].dt.to_period('M').value_counts().sort_index(),
            'pDNA_Batch': df['pDNA Created.1'].dt.to_period('M').value_counts().sort_index(),
            'LDF': df['LDF Created'].dt.to_period('M').value_counts().sort_index(),
            'CT mRNA': df_CT['mRNA Created'].dt.to_period('M').value_counts().sort_index(),
        }

        # Create a unified index of months
        all_months = sorted(set().union(*[cat.index for cat in categories.values()]))

        # Prepare data for bubble plot
        bubble_data = []
        for category, counts in categories.items():
            for month in all_months:
                count = counts.get(month, 0)
                bubble_data.append({
                    'Category': category,
                    'Month': month.to_timestamp(),
                    'Count': count
                })

        bubble_df = pd.DataFrame(bubble_data)

        # Map months to numeric values for better spacing
        month_labels = sorted(bubble_df['Month'].unique())
        month_to_y = {month: i * 1.5 for i, month in enumerate(month_labels)}
        bubble_df['Month_Y'] = bubble_df['Month'].map(month_to_y)

        # Bubble colors
        colors = {
            'pDNA_Design': '#7A1E76',
            'pDNA_Batch': '#008080',
            'LDF': '#ADD8E6',
            'CT mRNA': '#FFA500'
        }

        # Plot bubble chart
        fig = plt.figure(figsize=(30, 14), dpi=100)
        for category in categories.keys():
            subset = bubble_df[bubble_df['Category'] == category]
            plt.scatter(
                x=subset['Category'],
                y=subset['Month_Y'],
                s=subset['Count'] * 2,
                alpha=0.6,
                label=category,
                color=colors[category]
            )

        # Customize y-axis with month labels
        plt.yticks(
            ticks=list(month_to_y.values()),
            labels=[month.strftime('%b %Y') for month in month_labels],
            fontsize=35
        )
        plt.xlabel('Entity', fontsize=35)
        plt.ylabel('Month', fontsize=35)
        plt.title('Entities by Month (2024–2025)', fontsize=35)
        plt.xticks(fontsize=35)
        plt.tight_layout(pad=5.0)

        # Define example sizes
        size_legend = [100, 500, 1000, 2000]
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label=f'{size} items',
                markerfacecolor='gray', markersize=(size * 2)**0.5)
            for size in size_legend
        ]

        # Add legend outside the plot
        plt.legend(
            handles=legend_elements,
            title='Bubble Size Legend',
            loc='center left',
            bbox_to_anchor=(1.1, 0.5),
            fontsize=35,
            title_fontsize=35,
            labelspacing=4.0,
            handletextpad=2.0
        )

        plt.tight_layout()
        return fig
    


    def create_project_id_report(excel_sheet3):
        # Copy dataframe to avoid modifying original
        df = excel_sheet3.copy()

        # Drop rows with null Project IDs
        df = df.dropna(subset=['Vaccine Programs'])

        # Convert 'pDNA Created' to datetime
        df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')

        # Extract year and month
        df['Year'] = df['Created Date'].dt.year
        df['Month'] = df['Created Date'].dt.month

        # Define pastel color palette
        pastel_colors = [
            "#cbaacb", "#f1c0e8", "#b5ead7", "#ffdac1", "#ffb7b2",
            "#d5aaff", "#c7ceea", "#e2f0cb", "#f3c1c6", "#f6dfeb"
        ]
 
        def plot_altair_donut_chart(counts, title):
            # Prepare the data
            df_counts = counts.reset_index()
            df_counts.columns = ['Vaccine Programs', 'Count']
            df_counts['Percent'] = df_counts['Count'] / df_counts['Count'].sum() * 100
            df_counts['Label'] = df_counts.apply(lambda row: f"{row['Vaccine Programs']} ({row['Percent']:.1f}%)", axis=1)
            df_counts['Angle'] = df_counts['Count'] / df_counts['Count'].sum() * 2 * np.pi
            pastel_colors = ['purple', 'red', 'blue', '#AEC6CF', '#FFB347', '#B39EB5', '#77DD77', '#FF6961', '#FDFD96', '#CFCFC4', '#966FD6', '#F49AC2', '#CB99C9']
            df_counts['Color'] = pastel_colors[:len(df_counts)]

            # Donut chart with legend showing percentages
            chart = alt.Chart(df_counts).mark_arc(innerRadius=70).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Label", type="nominal", scale=alt.Scale(range=df_counts['Color'].tolist()), legend=alt.Legend(title="Vaccine Programs")),
                tooltip=["Vaccine Programs", "Count", alt.Tooltip("Percent", format=".1f")]
            ).properties(
                width=400,
                height=400,
                title=title
            )

            return chart.configure_view(stroke=None)


        # Donut chart for 2024
        df_2024 = df[df['Year'] == 2024]
        counts_2024 = df_2024['Vaccine Programs'].value_counts()
        chart1 = plot_altair_donut_chart(counts_2024, "")

        # Donut chart for 2025
        df_2025 = df[df['Year'] == 2025]
        counts_2025 = df_2025['Vaccine Programs'].value_counts()
        chart2 = plot_altair_donut_chart(counts_2025, "")

        # Donut chart for most recent month
        most_recent_date = df['Created Date'].max()
        most_recent_year = most_recent_date.year
        most_recent_month = most_recent_date.month

        df_recent = df[
            (df['Year'] == most_recent_year) &
            (df['Month'] == most_recent_month)
        ]
        counts_recent = df_recent['Vaccine Programs'].value_counts()
        chart3 = plot_altair_donut_chart(counts_recent, f"Vaccine Program Ticket Frequency - {most_recent_year}-{most_recent_month:02d}")

        return chart1, chart2, chart3

    # File uploader widget
    uploaded_file1 = "pDNA Report 2024 V2.xlsx"
    uploaded_file2 = "mRNA Report 2024 CT only With Antigen Design and pDNA.xlsx"
    uploaded_file3 = "mRNA Synthesis Export 8-4-2025 1.xlsx"

    #--------------------------------------------------------------------------------------------------------------
    excel_sheet1 = pd.read_excel(uploaded_file1, engine='openpyxl')
    excel_sheet2 = pd.read_excel(uploaded_file2, engine='openpyxl')
    excel_sheet3 = pd.read_excel(uploaded_file3, engine='openpyxl')

    chart1, chart2, chart3 = create_project_id_report(excel_sheet3)
    bubble_plot = create_monthly_report(excel_sheet1, excel_sheet2)

  
    with st.container(border=True):
        st.markdown("Total pDNAs by Project")
        # Create three columns
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("")
                st.markdown("<h4 style='font-size:18px;'>Most Recent Month</h4>", unsafe_allow_html=True)
                #st.subheader("Most Recent Month")
                st.altair_chart(chart3, use_container_width=True)
                get_png_download_button(chart3, "chart_recent.png", key= "download_chart_recent")
                st.markdown("")
                st.markdown("")
                st.markdown("")
        
            with st.container(border=True):
                st.markdown("")
                st.markdown("<h4 style='font-size:18px;'>Project ID Distribution in 2024</h4>", unsafe_allow_html=True)
                #st.subheader("Project ID Distribution in 2024")
                st.altair_chart(chart1, use_container_width=True)
                get_png_download_button(chart1, "chart_2024.png", key = "download_chart_2024")
                st.markdown("")
                st.markdown("")
                st.markdown("")


        with col2:
            with st.container(border=True):
                st.markdown("")
                st.markdown("<h4 style='font-size:18px;'>Project ID Distribution in 2025</h4>", unsafe_allow_html=True)
                #st.subheader("Project ID Distribution in 2025")
                st.altair_chart(chart2, use_container_width=True)
                get_png_download_button(chart2, "chart_2025.png", "download_chart_2025")
                st.markdown("")
                st.markdown("")
                st.markdown("")


        
        with st.container(border=True):
            st.markdown("")
            st.markdown("<h4 style='font-size:18px;'>Number of Registered Entities</h4>", unsafe_allow_html=True)
            st.pyplot(bubble_plot)
            st.markdown("")
            st.markdown("")
            st.markdown("")

        




    
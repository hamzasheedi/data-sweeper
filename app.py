import streamlit as st
import pandas as pd
from modules.uploader import upload_files
from modules.cleaner import clean_data
from modules.selector import select_columns
from modules.visualizer import visualize_data
from modules.converter import convert_and_download


def main():
    """
    Main function to run the Data Sweeper Streamlit application.
    Orchestrates the workflow: Upload -> Preview -> Clean -> Select -> Visualize -> Convert/Download
    """
    st.set_page_config(
        page_title="Data Sweeper",
        page_icon="🧹",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🧹 Data Sweeper")
    st.subheader("Clean, Process, and Transform Your Data Effortlessly")

    # Initialize session state variables
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = None
    if 'dataframes' not in st.session_state:
        st.session_state.dataframes = {}
    if 'cleaned_dataframes' not in st.session_state:
        st.session_state.cleaned_dataframes = {}
    if 'selected_columns' not in st.session_state:
        st.session_state.selected_columns = {}

    # Step 1: Upload Files
    st.header("📁 Upload Files")
    uploaded_files = upload_files()

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files

        # Process each uploaded file
        for file in uploaded_files:
            if file.name not in st.session_state.dataframes:
                # Load the dataframe
                try:
                    if file.name.endswith('.csv'):
                        df = pd.read_csv(file)
                    elif file.name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(file)
                    else:
                        st.error(f"Unsupported file type: {file.name}")
                        continue

                    st.session_state.dataframes[file.name] = df
                    st.session_state.cleaned_dataframes[file.name] = df.copy()
                except Exception as e:
                    st.error(f"Error loading file {file.name}: {str(e)}")

        # Show previews of uploaded data
        st.header("📊 Data Preview")
        for filename, df in st.session_state.dataframes.items():
            with st.expander(f"Preview: {filename}"):
                st.write(f"Shape: {df.shape}")
                st.dataframe(df.head())

        # Step 2: Clean Data
        st.header("🧽 Clean Data")
        cleaned_dataframes = clean_data(st.session_state.cleaned_dataframes)
        st.session_state.cleaned_dataframes = cleaned_dataframes

        # Step 3: Select Columns
        st.header("🔍 Select Columns")
        selected_columns = select_columns(st.session_state.cleaned_dataframes)
        st.session_state.selected_columns = selected_columns

        # Step 4: Visualize Data
        st.header("📈 Visualize Data")
        visualize_data(st.session_state.cleaned_dataframes, selected_columns)

        # Step 5: Convert and Download
        st.header("💾 Convert & Download")
        convert_and_download(st.session_state.cleaned_dataframes, selected_columns)


if __name__ == "__main__":
    main()
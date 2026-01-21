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
    # Page configuration
    st.set_page_config(
        page_title="Data Sweeper - Clean & Transform Data",
        page_icon="🧹",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject custom CSS for enhanced styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #444444;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .file-card {
        background-color: #f8f9fa;
        color: #333333;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .metric-container {
        background-color: #f0f8ff;
        color: #333333;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header Section
    st.markdown('<h1 class="main-header">🧹 Data Sweeper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Clean, Process, and Transform Your Data Effortlessly</p>', unsafe_allow_html=True)

    # Initialize session state variables
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = None
    if 'dataframes' not in st.session_state:
        st.session_state.dataframes = {}
    if 'cleaned_dataframes' not in st.session_state:
        st.session_state.cleaned_dataframes = {}
    if 'selected_columns' not in st.session_state:
        st.session_state.selected_columns = {}
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1

    # File Upload Section
    st.markdown('<h2 class="section-header">📁 Upload Files</h2>', unsafe_allow_html=True)
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

                    # Display file card
                    with st.container():
                        st.markdown(f"""
                        <div class="file-card">
                            <strong>📄 {file.name}</strong><br>
                            Size: {file.size:,} bytes<br>
                            Shape: {df.shape[0]:,} rows × {df.shape[1]:,} columns
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error loading file {file.name}: {str(e)}")

        # Data Preview Section
        st.markdown('<h2 class="section-header">📊 Data Preview</h2>', unsafe_allow_html=True)
        for filename, df in st.session_state.dataframes.items():
            with st.expander(f"🔍 Preview: {filename}", expanded=True):
                tab1, tab2 = st.tabs(["📋 Raw Data", "📈 Summary Stats"])

                with tab1:
                    st.write(f"**Shape:** {df.shape}")
                    # Convert problematic columns to string to avoid Arrow conversion issues
                    df_display = df.head(10).copy()
                    for col in df_display.columns:
                        if df_display[col].dtype == 'object':
                            # Try to convert to string, handling any problematic values
                            df_display[col] = df_display[col].apply(lambda x: str(x) if pd.notna(x) else x)
                    st.dataframe(df_display)

                with tab2:
                    st.write("**Basic Statistics:**")
                    st.dataframe(df.describe())
                    st.write("**Data Types:**")
                    st.write(df.dtypes.value_counts())

        # Data Cleaning Section
        st.markdown('<h2 class="section-header">🧽 Data Cleaning</h2>', unsafe_allow_html=True)
        cleaned_dataframes = clean_data(st.session_state.cleaned_dataframes)
        st.session_state.cleaned_dataframes = cleaned_dataframes

        # Column Selection Section
        st.markdown('<h2 class="section-header">🔍 Select Columns</h2>', unsafe_allow_html=True)
        selected_columns = select_columns(st.session_state.cleaned_dataframes)
        st.session_state.selected_columns = selected_columns

        # Visualization Section
        st.markdown('<h2 class="section-header">📈 Visualize Data</h2>', unsafe_allow_html=True)
        visualize_data(st.session_state.cleaned_dataframes, selected_columns)

        # Conversion & Download Section
        st.markdown('<h2 class="section-header">💾 Convert & Download</h2>', unsafe_allow_html=True)
        convert_and_download(st.session_state.cleaned_dataframes, selected_columns)

    # Footer Section
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #888888;">🎉 Thank you for using Data Sweeper! 🧹</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
import streamlit as st
from utils.file_utils import validate_file_type


def upload_files():
    """
    Handle file uploads for the Data Sweeper application.

    Returns:
        list: List of uploaded file objects
    """
    st.info("📤 Upload your data files (CSV, Excel formats supported)")

    uploaded_files = st.file_uploader(
        label="Choose files",
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        key="file_uploader"
    )

    if uploaded_files:
        # Validate file types
        valid_files = []
        for file in uploaded_files:
            if validate_file_type(file):
                valid_files.append(file)
            else:
                st.warning(f"⚠️ Unsupported file type: {file.name}")

        if len(valid_files) != len(uploaded_files):
            st.success(f"✅ {len(valid_files)} out of {len(uploaded_files)} files are valid.")
        else:
            st.success(f"✅ All {len(uploaded_files)} files are valid.")

        return valid_files
    else:
        st.info("ℹ️ Please upload at least one file to get started.")
        return None
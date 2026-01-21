import streamlit as st
import pandas as pd


def clean_data(dataframes):
    """
    Handle data cleaning operations for the Data Sweeper application.
    
    Args:
        dataframes (dict): Dictionary of dataframes to clean
    
    Returns:
        dict: Dictionary of cleaned dataframes
    """
    cleaned_dataframes = {}
    
    for filename, df in dataframes.items():
        st.subheader(f"Cleaning: {filename}")
        
        # Create a copy to avoid modifying the original
        df_clean = df.copy()
        
        # Option to remove duplicates
        remove_duplicates = st.checkbox(
            f"Remove duplicates in {filename}",
            value=False,
            key=f"remove_dup_{filename}"
        )
        
        if remove_duplicates:
            original_rows = len(df_clean)
            df_clean = df_clean.drop_duplicates()
            removed_rows = original_rows - len(df_clean)
            if removed_rows > 0:
                st.success(f"Removed {removed_rows} duplicate rows from {filename}")
            else:
                st.info(f"No duplicates found in {filename}")
        
        # Option to handle missing values
        col1, col2 = st.columns(2)
        
        with col1:
            handle_missing = st.selectbox(
                f"How to handle missing values in {filename}?",
                options=["Keep as is", "Drop rows", "Fill with 0", "Forward fill", "Backward fill"],
                key=f"missing_vals_{filename}"
            )
        
        if handle_missing != "Keep as is":
            if handle_missing == "Drop rows":
                original_rows = len(df_clean)
                df_clean = df_clean.dropna()
                removed_rows = original_rows - len(df_clean)
                st.success(f"Dropped {removed_rows} rows with missing values in {filename}")
                
            elif handle_missing == "Fill with 0":
                numeric_cols = df_clean.select_dtypes(include='number').columns
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
                object_cols = df_clean.select_dtypes(include=['object']).columns
                df_clean[object_cols] = df_clean[object_cols].fillna('N/A')
                st.info(f"Filled missing values with 0/N/A in {filename}")
                
            elif handle_missing == "Forward fill":
                df_clean = df_clean.fillna(method='ffill')
                st.info(f"Forward filled missing values in {filename}")
                
            elif handle_missing == "Backward fill":
                df_clean = df_clean.fillna(method='bfill')
                st.info(f"Backward filled missing values in {filename}")
        
        # Show info about the cleaned dataframe
        st.write(f"**Original shape:** {df.shape} → **Cleaned shape:** {df_clean.shape}")
        
        cleaned_dataframes[filename] = df_clean
    
    return cleaned_dataframes
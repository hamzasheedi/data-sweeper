import streamlit as st
import pandas as pd


def select_columns(dataframes):
    """
    Handle column selection for the Data Sweeper application.
    
    Args:
        dataframes (dict): Dictionary of dataframes to select columns from
    
    Returns:
        dict: Dictionary mapping filenames to selected columns
    """
    selected_columns = {}
    
    for filename, df in dataframes.items():
        st.subheader(f"Select columns for: {filename}")
        
        # Multiselect for column selection
        all_columns = df.columns.tolist()
        default_selection = all_columns  # By default, select all columns
        
        selected = st.multiselect(
            f"Columns in {filename}:",
            options=all_columns,
            default=default_selection,
            key=f"col_select_{filename}"
        )
        
        if selected:
            st.success(f"Selected {len(selected)} out of {len(all_columns)} columns for {filename}")
            selected_columns[filename] = selected
        else:
            st.warning(f"No columns selected for {filename}. Using all columns.")
            selected_columns[filename] = all_columns
    
    return selected_columns
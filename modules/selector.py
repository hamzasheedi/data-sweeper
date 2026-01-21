import streamlit as st
import pandas as pd


def select_all_callback(filename, all_columns):
    """Callback function to select all columns"""
    session_key = f"selected_cols_{filename}"
    st.session_state[session_key] = all_columns


def deselect_all_callback(filename):
    """Callback function to deselect all columns"""
    session_key = f"selected_cols_{filename}"
    st.session_state[session_key] = []


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
        with st.expander(f"📌 Select columns for: {filename}", expanded=True):
            # Multiselect for column selection
            all_columns = df.columns.tolist()

            # Initialize session state for this file's selected columns if not already set
            session_key = f"selected_cols_{filename}"
            if session_key not in st.session_state:
                st.session_state[session_key] = all_columns  # By default, select all columns

            # Create columns for better layout
            col1, col2 = st.columns([3, 1])

            with col2:
                # Add select all/deselect all buttons with callbacks
                st.button(
                    f"✅ Select All",
                    key=f"select_all_{filename}",
                    on_click=select_all_callback,
                    args=(filename, all_columns)
                )
                st.button(
                    f"❌ Deselect All",
                    key=f"deselect_all_{filename}",
                    on_click=deselect_all_callback,
                    args=(filename,)
                )

            with col1:
                selected = st.multiselect(
                    f"Columns in {filename}:",
                    options=all_columns,
                    default=st.session_state[session_key],
                    key=session_key
                )

            if selected:
                st.success(f"✅ Selected {len(selected)} out of {len(all_columns)} columns for {filename}")
                selected_columns[filename] = selected
            else:
                st.warning(f"⚠️ No columns selected for {filename}. Using all columns.")
                selected_columns[filename] = all_columns

    return selected_columns
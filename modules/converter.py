import streamlit as st
import pandas as pd
import io


def convert_and_download(dataframes, selected_columns):
    """
    Handle file conversion and download functionality for the Data Sweeper application.
    
    Args:
        dataframes (dict): Dictionary of dataframes to convert
        selected_columns (dict): Dictionary of selected columns for each dataframe
    """
    for filename, df in dataframes.items():
        st.subheader(f"Convert and download: {filename}")
        
        # Get the subset of the dataframe with selected columns only
        cols_to_use = selected_columns.get(filename, df.columns.tolist())
        df_subset = df[cols_to_use]
        
        # Choose output format
        output_format = st.radio(
            f"Select output format for {filename}:",
            options=["CSV", "Excel"],
            key=f"format_{filename}"
        )
        
        # Generate the converted file based on selected format
        if output_format == "CSV":
            csv_buffer = io.StringIO()
            df_subset.to_csv(csv_buffer, index=False)
            csv_str = csv_buffer.getvalue()
            
            st.download_button(
                label=f"Download {filename} as CSV",
                data=csv_str,
                file_name=f"cleaned_{filename.replace('.csv', '').replace('.xlsx', '').replace('.xls', '')}.csv",
                mime="text/csv",
                key=f"download_csv_{filename}"
            )
        
        elif output_format == "Excel":
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df_subset.to_excel(writer, index=False, sheet_name='Sheet1')
            excel_buffer.seek(0)
            
            st.download_button(
                label=f"Download {filename} as Excel",
                data=excel_buffer,
                file_name=f"cleaned_{filename.replace('.csv', '').replace('.xlsx', '').replace('.xls', '')}.xlsx",
                mime="application/vnd.ms-excel",
                key=f"download_excel_{filename}"
            )
        
        # Also provide option to download all as a zip
        if len(dataframes) > 1:
            st.info("Note: For multiple files, you can download them individually above.")
import streamlit as st
import pandas as pd
import plotly.express as px


def visualize_data(dataframes, selected_columns):
    """
    Handle data visualization for the Data Sweeper application.
    
    Args:
        dataframes (dict): Dictionary of dataframes to visualize
        selected_columns (dict): Dictionary of selected columns for each dataframe
    """
    for filename, df in dataframes.items():
        st.subheader(f"Visualizations for: {filename}")
        
        # Get the subset of the dataframe with selected columns only
        cols_to_use = selected_columns.get(filename, df.columns.tolist())
        df_subset = df[cols_to_use]
        
        # Identify numeric columns for plotting
        numeric_cols = df_subset.select_dtypes(include='number').columns.tolist()
        
        if not numeric_cols:
            st.info(f"No numeric columns found in {filename} for visualization.")
            continue
        
        # Create visualization options
        viz_type = st.selectbox(
            f"Select visualization type for {filename}:",
            options=["Histogram", "Box Plot", "Scatter Plot", "Line Chart"],
            key=f"viz_type_{filename}"
        )
        
        if viz_type == "Histogram":
            col_to_plot = st.selectbox(
                f"Select column for histogram in {filename}:",
                options=numeric_cols,
                key=f"hist_col_{filename}"
            )
            
            if col_to_plot:
                fig = px.histogram(df_subset, x=col_to_plot, title=f"Histogram of {col_to_plot}")
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Box Plot":
            col_to_plot = st.selectbox(
                f"Select column for box plot in {filename}:",
                options=numeric_cols,
                key=f"box_col_{filename}"
            )
            
            if col_to_plot:
                fig = px.box(df_subset, y=col_to_plot, title=f"Box Plot of {col_to_plot}")
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Scatter Plot":
            if len(numeric_cols) >= 2:
                col_x = st.selectbox(
                    f"Select X-axis column for scatter plot in {filename}:",
                    options=numeric_cols,
                    index=0,
                    key=f"scatter_x_{filename}"
                )
                
                col_y = st.selectbox(
                    f"Select Y-axis column for scatter plot in {filename}:",
                    options=numeric_cols,
                    index=min(1, len(numeric_cols)-1),
                    key=f"scatter_y_{filename}"
                )
                
                if col_x and col_y:
                    fig = px.scatter(df_subset, x=col_x, y=col_y, title=f"Scatter Plot: {col_x} vs {col_y}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"Not enough numeric columns for scatter plot in {filename}. Need at least 2.")
        
        elif viz_type == "Line Chart":
            col_to_plot = st.selectbox(
                f"Select column for line chart in {filename}:",
                options=numeric_cols,
                key=f"line_col_{filename}"
            )
            
            if col_to_plot:
                # Create an index for the line chart if there's no datetime column
                fig = px.line(df_subset, y=col_to_plot, title=f"Line Chart of {col_to_plot}")
                st.plotly_chart(fig, use_container_width=True)
        
        # Show basic statistics
        with st.expander(f"Show statistics for {filename}"):
            st.write(df_subset.describe())
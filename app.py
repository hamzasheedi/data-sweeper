import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure 
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Title / Description
st.title("🧹 Data Sweeper")
st.markdown("### Easily clean, analyze, and convert your CSV and Excel files.")

# File Uploader
uploaded_files = st.file_uploader(
    "📂 Upload your files (CSV or Excel)",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

# Process Uploaded Files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # File Info
        st.success(f"✅ **Uploaded:** {file.name} ({file.size} bytes)")
        st.write("🔍 **Preview of Data**")
        st.dataframe(df.head())

        # Cleaning Options
        st.subheader("🧹 Data Cleaning")
        if st.checkbox(f"Clean Data for **{file.name}**"):
            col1, col2 = st.columns(2)

            with col1:
                if st.checkbox("🚮 Remove Duplicates"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ **Duplicates Removed!**")

            with col2:
                if st.checkbox("🛠️ Fill Missing Values"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ **Missing values filled with column mean!**")

        # Select Columns for Conversion
        st.subheader("📌 Select Columns")
        columns = st.multiselect(
            f"Choose columns for **{file.name}**", 
            df.columns, 
            default=df.columns
        )
        df = df[columns]

        # Visualization
        st.subheader("📊 Quick Visualization")
        if st.checkbox(f"📉 Show Chart for **{file.name}**"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

        # File Conversion
        st.subheader("📂 Convert File Format")
        conversion_type = st.radio(
            f"Choose format for **{file.name}**",
            ["CSV", "Excel"],
            key=file.name
        )

        # Conversion
        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                file_name = os.path.splitext(file.name)[0] + ".csv"
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                buffer.seek(0)
                file_name = os.path.splitext(file.name)[0] + ".xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            # Download Button
            st.download_button(
                label=f"📥 Download Converted {file.name} as {conversion_type}",
                data=buffer.getvalue(),
                file_name=file_name,
                mime=mime_type
            )

st.success(f"🎉 **Thank you for using Data Sweeper!**")
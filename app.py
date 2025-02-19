import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Data Sweeper", page_icon="⚙️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #6a0dad;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
    }
    .stDownloadButton>button {
        background-color: #8a2be2;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
    }
    .stCheckbox>div>div {
        font-size: 16px;
    }
    .stRadio>div>div {
        font-size: 16px;
    }
    .stFileUploader>label {
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
    }
    .stTextArea>div>div>textarea {
        font-size: 16px;
    }
    .stSelectbox>div>div>div {
        font-size: 16px;
    }
    .stMultiselect>div>div>div {
        font-size: 16px;
    }
    .stSubheader {
        color: #6a0dad;
        font-size: 24px;
    }
    .stTitle {
        color: #6a0dad;
        font-size: 32px;
    }
    .stMarkdown {
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

#set up our app

st.title("Data Sweeper 🧹")
st.write("Transform your data with ease 🚀 from CSV and EXCEL formats with built-in data cleaning and optimization!")

uploaded_files = st.file_uploader("👨‍💻 Upload your CSV or Excel file here", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File format {file_ext} not supported")
            continue

        # Display info about the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024} KB")

        # Show 5 rows of the dataframe
        st.write("Preview the Head of the Dataframe")
        st.write(df.head())

        # Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled❗")

            # Choose Specific Columns to keep or convert
            st.subheader("Choose Specific Columns to Convert")
            columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Create Some Visualizations
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show Visualization for {file.name}"):
                numeric_df = df.select_dtypes(include='number')
                if numeric_df.shape[1] >= 4:
                    st.bar_chart(numeric_df.iloc[:, :4])
                else:
                    st.warning("Not enough numeric columns to display a bar chart. Please select more columns.")

            # Convert the File => CSV to Excel
            st.subheader("♻️ Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:", ['CSV', 'Excel'], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                # Download the button
                st.download_button(
                    label=f" ⬇️ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

st.success("Congratulations! You have successfully cleaned and optimized your data 🎉")




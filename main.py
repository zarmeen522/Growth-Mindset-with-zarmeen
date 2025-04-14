import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter & Cleaner", layout="wide")

page_bg_img = '''
<style>
.stApp {
    background-image: url("https://img.freepik.com/free-vector/watercolor-paper-with-floral-design_53876-97360.jpg?semt=ais_country_boost&w=740");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("WelCome to File Converter & Cleaner with Zarmeen Sheikh!💻")
st.subheader("Put Your Files Here and Get the Cleaned & Converted!\n\n Just with One Click!")
st.write("This will allow you to Upload your CSV and Excel Files to clean the debris and data and to Convert formats Effortlessly!")
    
files = st.file_uploader("Upload your CSV or Excel files", type=["csv","xlsx"], accept_multiple_files=(True)) 

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df =pd.read_csv(file) if ext=="csv" else pd.read_excel(file)

        st.subheader("📄 Data Cleaning Options")

        if st.checkbox(f"Clean Data for {file.name}"):

           st.subheader(f"File: {file.name} -Preview")
           st.dataframe(df,use_container_width=True)

           clean_option = st.selectbox(f"Select Cleaning Option for {file.name}",["None", "1. Remove Duplicates", "2. Remove Empty Rows", "3. Remove Empty Columns", "4. Fill Missing Values"])

           original_rows, original_cols = df.shape

           if clean_option == "1. Remove Duplicates":
              before = df.shape[0]
              df.drop_duplicates(inplace=True)
              after = df.shape[0]
              st.success(f"Removed {before - after} duplicate rows!")

           elif clean_option == "2. Remove Empty Rows":
                before = df.shape[0]
                df.dropna(how="any", inplace=True)
                after = df.shape[0]
                st.success(f" Removed {before - after} rows with empty cells!")
                if before -after>0:
                 st.success("Empty rows removed!")
                else:
                 st.warning("No empty rows found!")

           elif clean_option == "3. Remove Empty Columns":
                 before = df.shape[1]
                 df.dropna(how="any", inplace=True)
                 after = df.shape[1]
                 st.success(f" Removed {before - after} columns with empty cells!")
                 if before -after>0:
                  st.success("Empty columns removed!")
                 else:
                  st.warning("No empty columns found!")

           elif clean_option == "4. Fill Missing Values":
                total_missing = df.isnull().sum().sum()
                df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
                st.success(f"filled {total_missing} missing values with column mean!")

                selected_columns =st.multiselect("Select Columns - {file.name}", df.columns, default=df.columns)
                df=df[selected_columns]
                st.dataframe(df.head())

                st.info(f"📊 Final dataset: {df.shape[0]} rows × {df.shape[1]} columns")
# ⛏️ Check numeric columns
                st.write(f"🧪 Checking numeric columns for {file.name}...")
                numeric_data = df.select_dtypes(include="number")

# Show what numeric columns are found
                st.write("✅ Found numeric columns:")
                st.write(numeric_data.columns.tolist())

# Show some sample numeric data
                st.write("📊 Preview of numeric data:")
                st.write(numeric_data.head())

# Check if there's anything to plot
                if not numeric_data.empty:
                  if st.checkbox(f"📈 Show Chart for {file.name}"):
                     st.write("🎯 Plotting first two numeric columns:")
                     st.bar_chart(numeric_data.iloc[:, :2])
                else:
                     st.warning("⚠️ No numeric columns found. Please make sure your data includes numbers.")


        format_choice= st.radio(f"Convert {file.name} to:",["CSV","Excel"], key=file.name)
        if st.button(f"Download {file.name} as {format_choice}"):
                    output = BytesIO()
                    if format_choice =="CSV":
                        df.to_csv(output, index=False)
                        mime="text/csv"
                        new_name =file.name.replace(ext,"csv")
                    else:
                        df.to_excel(output,index=False)
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        new_name=file.name.replace(ext,"xlsx")
                    output.seek(0)
                    st.download_button(f"Download file", file_name=new_name, data=output ,mime=mime)
                    st.success("File Processed and Downloaded successfully!")       




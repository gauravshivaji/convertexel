import streamlit as st
import pandas as pd

st.title("Stock Closing Price Format Converter")

st.write(
"""
Upload a dataset with format:

Date | Ticker | Close

The app will convert it to:

Ticker | 2024-01-01 | 2024-01-02 | 2024-01-03
"""
)

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv","xlsx"])

if uploaded_file is not None:

    # read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Original Data")
    st.dataframe(df.head())

    # convert date column
    df["Date"] = pd.to_datetime(df["Date"])

    # remove decimals
    df["Close"] = df["Close"].round(0).astype("Int64")

    # pivot transformation
    pivot_df = df.pivot(index="Ticker", columns="Date", values="Close")

    # reset index
    pivot_df = pivot_df.reset_index()

    # convert date columns to string
    pivot_df.columns = [
        col.strftime("%Y-%m-%d") if isinstance(col, pd.Timestamp) else col
        for col in pivot_df.columns
    ]

    st.subheader("Converted Data")
    st.dataframe(pivot_df)

    # CSV download
    csv = pivot_df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="stocks_wide_format.csv",
        mime="text/csv"
    )

    # Excel download
    excel_file = "stocks_wide_format.xlsx"
    pivot_df.to_excel(excel_file, index=False)

    with open(excel_file, "rb") as f:
        st.download_button(
            label="Download Excel",
            data=f,
            file_name=excel_file
        )


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
from datetime import datetime

st.set_page_config(page_title="📊 Streamlit Insights Application", layout="wide")
st.title("📊 Streamlit Insights Application")
st.markdown("""
Upload a CSV file to explore your dataset, clean it, and generate interactive visual insights.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load CSV into DataFrame
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
    else:
        st.success("CSV file loaded successfully!")

        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        st.subheader("🧼 Data Cleaning")
        missing_values = df.isnull().sum()
        st.write("Missing Values Per Column:")
        st.write(missing_values[missing_values > 0])

        if missing_values.sum() > 0:
            df_cleaned = df.dropna()
            st.write(f"Dropped {df.shape[0] - df_cleaned.shape[0]} rows with missing values.")
        else:
            df_cleaned = df

        st.subheader("📊 Basic Statistics")
        st.write(df_cleaned.describe())

        st.subheader("📈 Key Insights & Visualizations")
        numeric_cols = df_cleaned.select_dtypes(include='number').columns.tolist()

        if numeric_cols:
            st.markdown("### Distribution of Numerical Features")
            selected_hist_col = st.selectbox("Select column for histogram", numeric_cols)
            fig, ax = plt.subplots()
            sns.histplot(df_cleaned[selected_hist_col], kde=True, ax=ax)
            st.pyplot(fig)

            st.markdown("### Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df_cleaned[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

            st.markdown("### Time Series Plot (optional)")
            datetime_cols = df_cleaned.select_dtypes(include=['datetime64', 'object']).columns.tolist()
            if datetime_cols:
                time_col = st.selectbox("Select datetime column", datetime_cols)
                try:
                    df_cleaned[time_col] = pd.to_datetime(df_cleaned[time_col])
                    ts_col = st.selectbox("Select numeric column to plot over time", numeric_cols)
                    fig, ax = plt.subplots()
                    df_cleaned.sort_values(time_col).set_index(time_col)[ts_col].plot(ax=ax)
                    ax.set_ylabel(ts_col)
                    st.pyplot(fig)
                except Exception as e:
                    st.warning("Couldn't parse selected column as datetime.")
        else:
            st.warning("No numeric columns found to plot.")

        # Download report
        st.subheader("⬇️ Download Cleaned Data")
        csv_download = df_cleaned.to_csv(index=False).encode('utf-8')
        st.download_button("Download Cleaned CSV", csv_download, "cleaned_data.csv", "text/csv")

else:
    st.info("Please upload a CSV file to get started.")

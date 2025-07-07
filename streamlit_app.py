
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Rainfall Trend Visualization", layout="wide")
st.title("🌧️ Rainfall Trend Visualization (Mumbai 2011–2021)")
st.markdown("### Upload the Excel file and visualize trends, seasonal patterns, and variability.")

# Step 1: Upload Excel File
st.sidebar.header("Step 1: Upload Excel File")
uploaded_file = st.sidebar.file_uploader("Upload Excel file (e.g. mumbai_rainfall_2011_2021.xlsx)", type=["xlsx"])

if uploaded_file:
    # Step 2: Read Excel file
    df = pd.read_excel(uploaded_file)

    st.subheader("Step 2: Dataset Preview")
    st.dataframe(df.head())

    # Step 3: Clean and Prepare Data
    st.subheader("Step 3: Data Cleaning & Reshaping")
    if 'Year' in df.columns:
        df_long = pd.melt(df, id_vars=['Year'], var_name='Month', value_name='Rainfall')
    else:
        st.error("The Excel file must contain a 'Year' column.")
        st.stop()

    # Step 4: Convert to datetime
    try:
# Step 4: Convert to datetime (handle full and short month names)

    try:
        df_long['Date'] = pd.to_datetime(
            df_long['Year'].astype(str) + '-' + df_long['Month'],
            format='%Y-%B'
        )
    except Exception:
        df_long['Date'] = pd.to_datetime(
            df_long['Year'].astype(str) + '-' + df_long['Month'],
            format='%Y-%b'
        )


    # Step 5: Annual Rainfall Trend
    st.subheader("Step 5: Total Annual Rainfall")
    annual = df_long.groupby('Year')['Rainfall'].sum().reset_index()
    fig1, ax1 = plt.subplots()
    sns.lineplot(data=annual, x='Year', y='Rainfall', marker='o', ax=ax1)
    ax1.set_title('Total Annual Rainfall (mm)')
    ax1.set_ylabel('Rainfall (mm)')
    st.pyplot(fig1)

    # Step 6: Average Rainfall by Month
    st.subheader("Step 6: Average Rainfall by Month")
    order = ['January','February','March','April','May','June','July','August','September','October','November','December']
    monthly_avg = df_long.groupby('Month')['Rainfall'].mean().reindex(order)
    fig2, ax2 = plt.subplots()
    monthly_avg.plot(kind='bar', ax=ax2, color='skyblue')
    ax2.set_title('Average Monthly Rainfall (2011–2021)')
    ax2.set_ylabel('Rainfall (mm)')
    st.pyplot(fig2)

    # Step 7: Monthly Boxplot
    st.subheader("Step 7: Monthly Rainfall Variation (Boxplot)")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df_long, x='Month', y='Rainfall', order=order, ax=ax3)
    ax3.set_title('Monthly Rainfall Variation Across Years')
    ax3.set_ylabel('Rainfall (mm)')
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Step 8: Summary
    st.subheader("Step 8: Summary & Interpretation")
    with st.expander("Click to view insights"):
        st.markdown("""
        - 📉 **Annual Trend:** Identify years with highest and lowest rainfall.
        - 🌦️ **Seasonal Pattern:** Observe peak rainfall months (e.g., June–September).
        - 📊 **Monthly Variability:** Boxplot reveals months with most inconsistent rainfall (wide spread or outliers).
        - 🔍 Useful for climate study, infrastructure design, and planning in Mumbai.
        """)

else:
    st.info("👈 Upload your Excel file to begin.")

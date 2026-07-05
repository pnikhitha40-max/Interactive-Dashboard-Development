import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Business Dashboard",
                   page_icon="📊",
                   layout="wide")

st.title("📊 Interactive Business Dashboard")

uploaded_file = st.file_uploader(
    "Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("sample_data.csv")

# Sidebar Filters
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

# KPI Cards
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["OrderID"].count()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", total_orders)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    sales_trend = filtered_df.groupby(
        "Month")["Sales"].sum().reset_index()

    fig = px.line(
        sales_trend,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        filtered_df,
        names="Category",
        values="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:

    region_sales = filtered_df.groupby(
        "Region")["Sales"].sum().reset_index()

    fig = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:

    fig = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Sales",
        title="Sales vs Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

st.dataframe(filtered_df)

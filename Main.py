# Streamlit!
import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
# from streamlit_navigation_bar import st_navbar

# Warning
import warnings
warnings.filterwarnings("ignore")
import time as tm

# Library Utama
import pandas as pd
import numpy as np

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 1000)

import matplotlib.pyplot as plt
import seaborn as sns

# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go

# Streamlit Web Configuration
st.set_page_config(
    page_title="My Dashboard - Logistics Supply",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto"
)

dataset = pd.read_csv("dataset/dataset-supply.csv", parse_dates=['Ship Date'])
df = dataset.ffill()

with st.container(border=False):
    st.markdown('<h1 style=text-align:center>My Supply Dashboard</h1>', unsafe_allow_html=True)
    # add_vertical_space(3)
    
st.dataframe(data=df, width=1500, use_container_width=True, hide_index=True)


col1, col2, col3, col4 = st.columns([0.05, 0.55, 0.05, 0.35], gap="small")

with col1:
    st.markdown("<br>", unsafe_allow_html=True)

    icon_click = st.button("🖥️", help="Click to interact!", key="office_button")



with col2:
    dataset['Ship Date'] = pd.to_datetime(dataset['Ship Date'], format='%Y-%m-%d')

    df_category_per_date = dataset.loc[
        (dataset['Ship Date'] >= '2014-08-01') & 
        (dataset['Ship Date'] < '2017-09-30')
    ]

    df_category_per_date.sort_values(by="Ship Date", ascending=True)

    start_of_month_dates = pd.date_range(start='2014-01-01', end='2017-12-31', freq='MS')
    df_category_per_date = df_category_per_date[df_category_per_date['Ship Date'].isin(start_of_month_dates)]

    df_category = df_category_per_date.groupby(by=["Category", "Month", "Ship Date"])["Sold"].aggregate("sum").reset_index().sort_values("Ship Date", ascending=True)

    category = "Office Supplies"
    df_category.query('Category == @category', inplace=True)

    df_category["Percent"] = (df_category["Sold"] / df_category["Sold"].sum()) * 100
    df_category = np.round(df_category, 0)

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df_category, x="Ship Date", y="Percent", marker="X")

    ax.set_title('', fontsize=15)
    ax.set_xlabel('', fontsize=12)
    ax.set_ylabel('', fontsize=12)
    ax.grid(True)

    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)

    plt.tight_layout()
    # plt.show()

    st.write("## Analisis Penjualan Office Supplies")
    st.pyplot(fig)


    col1, col2 = st.columns([0.5, 0.5], gap="small")

    with col1:
        df_area = dataset.groupby("Area")[["Sold"]].aggregate("sum").reset_index().sort_values("Sold", ascending=False)

        df_area["Percent"] = (df_area["Sold"] / df_area["Sold"].sum()) * 100

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=df_area, x="Percent", y="Area", hue="Area", palette="YlGn_r")

        ax.set_title('Highest Sales Percentage by Area', fontsize=15)
        ax.set_xlabel('', fontsize=12)
        ax.set_ylabel('', fontsize=12)
        ax.grid(True)
        # ax.legend(loc="best")

        plt.tight_layout()
        # plt.show()
        st.pyplot(fig)

    with col2:
        df_region = dataset.groupby("Region")["Sold"].aggregate("sum").reset_index().sort_values("Region", ascending=True)

        df_region["Percent"] = (df_region["Sold"] / df_region["Sold"].sum()) * 100

        labels = df_region["Region"].unique()
        sizes = df_region["Percent"]
        explode = (0, 0, 0, 0.1)

        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  

        ax1.set_title('Sales Percentage by Region', fontsize=15)
        ax1.set_xlabel('', fontsize=12)
        ax1.set_ylabel('', fontsize=12)
        ax1.grid(True)
        # ax1.legend(loc="best")

        plt.tight_layout()
        # plt.show()
        st.pyplot(fig1)


with col4:
    st.markdown("<br><br>", unsafe_allow_html=True)

    top_region = df_region.iloc[0]
    total_sales = df_region["Sold"].sum()
    top_region_sales = top_region["Sold"]
    top_region_percent = top_region["Percent"]

    a, b = st.columns(2)
    c, d = st.columns(2)

    a.metric("Top Region", top_region["Region"], f"{top_region_percent:.1f}%")
    b.metric("Total Sales", f"${total_sales:,.2f}", delta=f"${top_region_sales:,.2f}")

    c.metric("Average Sale per Region", f"${total_sales / len(df_region):,.2f}", delta="+$500")
    d.metric("Other Metric", "Value", "Change")


    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)


    df_year = dataset.groupby("Year")["Sold"].aggregate("sum").reset_index().sort_values("Year", ascending=True)
    
    df_year["Percent"] = (df_year["Sold"] / df_year["Sold"].sum()) * 100

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=df_year, x="Year", y="Percent", hue="Year", palette="YlGn")

    ax.set_title('Sales Percentage in Several Years', fontsize=15)
    ax.set_xlabel('', fontsize=12)
    ax.set_ylabel('', fontsize=12)
    ax.grid(True)
    # ax.legend(loc="best")

    plt.tight_layout()
    # plt.show()
    st.pyplot(fig)

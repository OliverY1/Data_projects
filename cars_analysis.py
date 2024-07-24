import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

@st.cache_data
def get_data():
    df = pd.read_csv(r"datasets/cars.csv", index_col=0)
    return df


def car_project():
    df = get_data()
    df = df.rename(columns={"Foreign/Local Used":"Foreign_or_local_used"})
    df["price"]=df["price"]*0.001 #convert from Naira to usd



    st.sidebar.header("Filter")
    Manufacturer = st.sidebar.multiselect(
        "select the Manufacturer:",
        options=df["manufacturer"].unique(),
        default=df["manufacturer"].unique())

    automation = st.sidebar.radio("Select the automation", options=df["Automation"].unique())

    category = st.sidebar.radio("Select the use category", options=df["Foreign_or_local_used"].unique())
    filtered_df = df.query("manufacturer== @Manufacturer & Automation== @automation & Foreign_or_local_used == @category")

    if filtered_df.empty:
        st.warning("The filters do not match any data")
        st.stop()


    st.title("Analysis of cars")

    average_price = int(filtered_df["price"].mean())
    car_count = filtered_df.shape[0]
    earliest_production_year = filtered_df["make-year"].min()

    st.divider()

    price_per_color = filtered_df.groupby(by=["color"])[["price"]].mean().sort_values(by="price")
    price_per_production = filtered_df.groupby(by=["manufacturer"])[["price"]].mean().sort_values(by="price")
    seat_material_price = filtered_df.groupby(by=["seat-make"])[["price"]].mean().sort_values(by="price")

    fig_color_price = px.bar(price_per_color,x="price",  title="Average price per color")
    production_price_fig = px.bar(price_per_production,y="price", title="Average price per manufacturer")
    seat_price_fig = px.pie(seat_material_price, values="price", title="average distribution of seat materials",names=seat_material_price.index)
    production_year_fig = px.histogram(filtered_df, x="make-year")
    production_year_fig.update_layout(bargap=0.1)


    left_col, right_col = st.columns(2)
    left_col.plotly_chart(fig_color_price, use_container_width=True)
    right_col.plotly_chart(production_price_fig, use_container_width=True)
    st.divider()

    max_price = filtered_df["price"].max()
    min_price = filtered_df["price"].min()

    left_col2, mid_col, right_col2 = st.columns(3)
    with left_col2:
        left_col2.metric(label="Price of cheapest car (usd $)", value=min_price)
    with left_col2:
        left_col2.metric(label="Price of most expensive car (usd $)", value=max_price)
    with left_col2:
        left_col2.metric(label="Average price (usd $)", value=average_price)
    with left_col2:
        left_col2.metric(label="car count", value=car_count)
    with left_col2:
        left_col2.metric(label="Earliest production year", value=earliest_production_year)


    mid_col.plotly_chart(seat_price_fig, use_container_width=True)

    right_col2.plotly_chart(production_year_fig, use_container_width=True)

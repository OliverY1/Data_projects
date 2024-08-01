import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import plotly.express as px
import streamlit as st

columns = ['TotalCases', 'TotalDeaths', 'TotalRecovered', 'ActiveCases']

# Load the data
@st.cache_data
def load_data():
    world_data = pd.read_csv(r"datasets/Covid-19/worldometer_data.csv")
    day_wise_data = pd.read_csv(r"datasets/Covid-19/day_wise.csv")
    return world_data, day_wise_data

world_data, day_wise_data = load_data()

@st.cache_data
def draw_left_figures(filtered_df, pop_test, deaths_to_confirmed):
    if len(filtered_df)>=20:
        top = 20
    else:
        top = len(filtered_df)
    top = str(top)

    
    st.plotly_chart(px.bar(filtered_df.iloc[0:20], x="Country/Region", y=pop_test[0:20], color="Country/Region", title="Population-to-COVID-19 Test Ratio by Country", template="plotly_dark", labels={'y': 'Ratio'}))
    st.plotly_chart(px.line(day_wise_data, x="Date", y=['Confirmed', 'Deaths', 'Recovered', 'Active'], title="COVID-19 cases based on date", template="plotly_dark", labels={'value': 'Amount of cases'}))
    st.plotly_chart(px.bar(filtered_df.iloc[0:20], x="Country/Region", y=["Serious,Critical", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalCases"],labels={'value': 'Amount of cases'}, title="top "+top+" Most affected countries in different cases", template="plotly_dark"))

    for i in columns[:2]:
        fig = px.treemap(filtered_df.iloc[0:20], values=i, path=["Country/Region"], title=f"Treemap representation of different countries based on their "+str(i), labels={"labels": "Country"}, template="plotly_dark")
        st.plotly_chart(fig)

    for i in columns[:2]:
        pie_chart = px.pie(filtered_df[0:15], values=i, names=filtered_df[0:15]["Country/Region"].values, hole=0.3, title=f"Top "+top+" Most Affected Countries by "+str(i))
        st.plotly_chart(pie_chart)

    st.plotly_chart(px.bar(filtered_df, x="Country/Region", y=deaths_to_confirmed, title="Death-to-Confirmed Ratio of the Most Affected Countries", labels={'y': 'Ratio'}))

@st.cache_data
def draw_right_figures(filtered_df):
    if len(filtered_df)>=20:
        top = 20
    else:
        top = len(filtered_df)
    top = str(top)


    bar_chart = px.bar(filtered_df.iloc[0:20], y='Country/Region', color="TotalCases", x='TotalCases', text='TotalCases', template="plotly_dark")
    bar_chart.update_layout(title_text="Top "+top+" countries of total confirmed cases")
    st.plotly_chart(bar_chart)

    bar_chart_deaths = px.bar(filtered_df.sort_values(by="TotalDeaths", ascending=False)[0:20], y='Country/Region', color="TotalDeaths", x='TotalDeaths', text='TotalDeaths', template="plotly_dark")
    bar_chart_deaths.update_layout(title_text="Top" +top+" countries of confirmed death cases")
    st.plotly_chart(bar_chart_deaths)

    bar_chart_active = px.bar(filtered_df.sort_values(by='ActiveCases', ascending=False)[0:20], y='Country/Region', color='ActiveCases', x='ActiveCases', text='ActiveCases', template="plotly_dark")
    bar_chart_active.update_layout(title_text="Top "+top+" countries of confirmed active cases")
    st.plotly_chart(bar_chart_active)

    for i in columns[2:]:
        fig = px.treemap(filtered_df.iloc[0:20], values=i, path=["Country/Region"], title=f"Treemap representation of different countries based on their "+str(i), labels={"labels": "Country"}, template="plotly_dark")
        st.plotly_chart(fig)

    for i in columns[2:]:
        pie_chart = px.pie(filtered_df[0:15], values=i, names=filtered_df[0:15]["Country/Region"].values, hole=0.3, title=f"Top "+top+" Most Affected Countries by "+str(i))
        st.plotly_chart(pie_chart)

    bar_chart_recovered = px.bar(filtered_df.sort_values(by='TotalRecovered', ascending=False)[0:20], y='Country/Region', color='TotalRecovered', x='TotalRecovered', text='TotalRecovered', template="plotly_dark")
    bar_chart_recovered.update_layout(title_text="Top "+top+" countries of confirmed recovered cases")
    st.plotly_chart(bar_chart_recovered)

def draw_web():
    st.header("Covid-19 analysis")
    st.write("----")

    with st.sidebar:

        st.sidebar.header("Filter")
        select_continent = st.multiselect("Select continents", options=world_data["Continent"].unique(), default=world_data["Continent"].unique())

        default_settings = world_data["Country/Region"].unique()
        if st.radio('Select countries', ['Default','Select']) == "Default":
            default_settings = world_data["Country/Region"].unique()
        else: 
            default_settings = None

        select_country = st.multiselect("",
            options=world_data["Country/Region"].unique(),
            default=default_settings)
        
    
    filtered_df = world_data.query("`Country/Region` == @select_country & `Continent` == @select_continent")

    if filtered_df.empty:
        st.warning("The filters do not match any data")
        st.stop()

    pop_test = filtered_df["Population"] / filtered_df["TotalTests"]
    deaths_to_confirmed = filtered_df["TotalDeaths"] / filtered_df["TotalCases"]

    left_col, right_col = st.columns(2)
    with left_col:
        draw_left_figures(filtered_df, pop_test, deaths_to_confirmed)
    with right_col:
        draw_right_figures(filtered_df)

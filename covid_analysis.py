import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import streamlit as st

columns = ['TotalCases', 'TotalDeaths', 'TotalRecovered', 'ActiveCases']

# Load the data
#@st.cache_data
def load_data():
    world_data = pd.read_csv(r"datasets\Covid-19\worldometer_data.csv")
    day_wise_data = pd.read_csv("datasets\Covid-19\day_wise.csv")
    pop_test = world_data["Population"] / world_data["TotalTests"]
    deaths_to_confirmed = world_data["TotalDeaths"] / world_data["TotalCases"]
    return world_data, day_wise_data, pop_test, deaths_to_confirmed

world_data, day_wise_data, pop_test, deaths_to_confirmed = load_data()

# Draw the web interface
def draw_web():
    st.sidebar.header("Filter")
    country_select = st.sidebar.multiselect(
        "Select the Countries:",
        options=world_data["Country/Region"].unique(),
        default=world_data["Country/Region"].unique()
    )

    # Declare and initialize filtered_df here
    filtered_df = world_data.query("'Country/Region' == @country_select")

    if filtered_df.empty:
        st.warning("The filters do not match any data")
        st.stop()

    # Create figures after filtered_df is defined
    fig1, day_wise_fig, fig2, fig3, bar_chart, bar_chart_deaths, bar_chart_active, bar_chart_recovered, deaths_to_confirmed_fig = create_figures(filtered_df)

    left_col, right_col = st.columns(2)
    with left_col:
        draw_left_figures(fig1, day_wise_fig, fig3, deaths_to_confirmed_fig, filtered_df)
    with right_col:
        draw_right_figures(bar_chart, bar_chart_deaths, bar_chart_active, bar_chart_recovered, filtered_df)

# Create figures
@st.cache_data
def create_figures(filtered_df):
    fig1 = px.bar(filtered_df.iloc[0:20], x="Country/Region", y=pop_test[0:20], color="Country/Region", title="Ratio of Population to COVID-19 Tests Conducted by Region", template="plotly_dark")
    fig1.update_layout(yaxis_title='Population Test Ratio')

    fig2 = px.bar(filtered_df.iloc[0:20], x="Country/Region", y=["Serious,Critical", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalCases"], title="Most affected countries in different cases", template="plotly_dark")

    bar_chart = px.bar(filtered_df.iloc[0:20], y='Country/Region', color="TotalCases", x='TotalCases', text='TotalCases', template="plotly_dark")
    bar_chart.update_layout(title_text="Top 20 countries of total confirmed cases")

    day_wise_fig = px.line(filtered_df, x="Date", y=['Confirmed', 'Deaths', 'Recovered', 'Active'], title="COVID-19 cases based on date", template="plotly_dark")
    fig3 = px.bar(filtered_df.iloc[0:20], x="Country/Region", y=["Serious,Critical", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalCases"], title="Most affected countries in different cases", template="plotly_dark")

    bar_chart_deaths = px.bar(filtered_df.sort_values(by="TotalDeaths", ascending=False)[0:20], y='Country/Region', color="TotalDeaths", x='TotalDeaths', text='TotalDeaths', template="plotly_dark")
    bar_chart_deaths.update_layout(title_text="Top 20 countries of confirmed death cases")

    bar_chart_active = px.bar(filtered_df.sort_values(by='ActiveCases', ascending=False)[0:20], y='Country/Region', color='ActiveCases', x='ActiveCases', text='ActiveCases', template="plotly_dark")
    bar_chart_active.update_layout(title_text="Top 20 countries of confirmed active cases")

    bar_chart_recovered = px.bar(filtered_df.sort_values(by='TotalRecovered', ascending=False)[0:20], y='Country/Region', color='TotalRecovered', x='TotalRecovered', text='TotalRecovered', template="plotly_dark")
    bar_chart_recovered.update_layout(title_text="Top 20 countries of confirmed recovered cases")

    deaths_to_confirmed_fig = px.bar(filtered_df, x="Country/Region", y=deaths_to_confirmed, title="Deaths to confirmed ratio of worst affected countries")

    return fig1, day_wise_fig, fig2, fig3, bar_chart, bar_chart_deaths, bar_chart_active, bar_chart_recovered, deaths_to_confirmed_fig

# Draw left figures
#@st.cache_data
def draw_left_figures(fig1, day_wise_fig, fig3, deaths_to_confirmed_fig, filtered_df):
    st.plotly_chart(fig1)
    st.plotly_chart(day_wise_fig)
    st.plotly_chart(fig3)

    for i in columns[:2]:
        fig = px.treemap(filtered_df.iloc[0:20], values=i, path=["Country/Region"], title=f"Treemap representation of different countries based on their {i}", labels={"labels": "Country"}, template="plotly_dark")
        st.plotly_chart(fig)

    for i in columns[:2]:
        pie_chart = px.pie(filtered_df[0:15], values=i, names=filtered_df[0:15]["Country/Region"].values, hole=0.3, title=f"Top 15 Most Affected Countries by {i}")
        st.plotly_chart(pie_chart)

    st.plotly_chart(deaths_to_confirmed_fig)

# Draw right figures
#@st.cache_data
def draw_right_figures(bar_chart, bar_chart_deaths, bar_chart_active, bar_chart_recovered, filtered_df):
    st.plotly_chart(bar_chart)
    st.plotly_chart(bar_chart_deaths)
    st.plotly_chart(bar_chart_active)

    for i in columns[2:]:
        fig = px.treemap(filtered_df.iloc[0:20], values=i, path=["Country/Region"], title=f"Treemap representation of different countries based on their {i}", labels={"labels": "Country"}, template="plotly_dark")
        st.plotly_chart(fig)

    for i in columns[2:]:
        pie_chart = px.pie(filtered_df[0:15], values=i, names=filtered_df[0:15]["Country/Region"].values, hole=0.3, title=f"Top 15 Most Affected Countries by {i}")
        st.plotly_chart(pie_chart)

    st.plotly_chart(bar_chart_recovered)

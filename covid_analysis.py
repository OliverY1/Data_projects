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
    world_data = pd.read_csv(r"datasets\Covid-19\worldometer_data.csv")
    day_wise_data = pd.read_csv("datasets\Covid-19\day_wise.csv")
    pop_test = world_data["Population"] / world_data["TotalTests"]
    deaths_to_confirmed = world_data["TotalDeaths"] / world_data["TotalCases"]
    return world_data, day_wise_data, pop_test, deaths_to_confirmed

world_data, day_wise_data, pop_test, deaths_to_confirmed = load_data()


@st.cache_data
def create_figures():
    fig1 = px.bar(world_data.iloc[0:20], x="Country/Region", y=pop_test[0:20], color="Country/Region", title="Ratio of Population to COVID-19 Tests Conducted by Region", template="plotly_dark")
    fig1.update_layout(yaxis_title='Population Test Ratio')

    fig2 = px.bar(world_data.iloc[0:20], x="Country/Region", y=["Serious,Critical", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalCases"], title="Most affected countries in different cases", template="plotly_dark")

    bar_chart = px.bar(world_data.iloc[0:20], y='Country/Region', color="TotalCases", x='TotalCases', text='TotalCases', template="plotly_dark")
    bar_chart.update_layout(title_text="Top 20 countries of total confirmed cases")

    day_wise_fig = px.line(day_wise_data, x="Date", y=['Confirmed', 'Deaths', 'Recovered', 'Active'], title="COVID-19 cases based on date", template="plotly_dark")
    fig3 = px.bar(world_data.iloc[0:20], x="Country/Region", y=["Serious,Critical", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalCases"], title="Most affected countries in different cases", template="plotly_dark")

    bar_chart_deaths = px.bar(world_data.sort_values(by="TotalDeaths", ascending=False)[0:20], y='Country/Region', color="TotalDeaths", x='TotalDeaths', text='TotalDeaths', template="plotly_dark")
    bar_chart_deaths.update_layout(title_text="Top 20 countries of confirmed death cases")

    bar_chart_active = px.bar(world_data.sort_values(by='ActiveCases', ascending=False)[0:20], y='Country/Region', color='ActiveCases', x='ActiveCases', text='ActiveCases', template="plotly_dark")
    bar_chart_active.update_layout(title_text="Top 20 countries of confirmed active cases")

    bar_chart_recovered = px.bar(world_data.sort_values(by='TotalRecovered', ascending=False)[0:20], y='Country/Region', color='TotalRecovered', x='TotalRecovered', text='TotalRecovered', template="plotly_dark")
    bar_chart_recovered.update_layout(title_text="Top 20 countries of confirmed recovered cases")

    deaths_to_confirmed_fig = px.bar(world_data, x="Country/Region", y=deaths_to_confirmed, title="Deaths to confirmed ratio of worst affected countries")

    return fig1, day_wise_fig, fig2, fig3, bar_chart, bar_chart_deaths, bar_chart_active, bar_chart_recovered, deaths_to_confirmed_fig

fig1, day_wise_fig, fig2, fig3, bar_chart, bar_chart_deaths, bar_chart_active, bar_chart_recovered, deaths_to_confirmed_fig = create_figures()

@st.cache_data
def draw_left_figures():
    st.plotly_chart(fig1)
    st.plotly_chart(day_wise_fig)
    st.plotly_chart(fig3)

    for i in columns[:2]:
        fig = px.treemap(world_data.iloc[0:20], values=i, path=["Country/Region"], title=f"Treemap representation of different countries based on their {i}", labels={"labels": "Country"}, template="plotly_dark")
        st.plotly_chart(fig)

    for i in columns[:2]:
        pie_chart = px.pie(world_data[0:15], values=i, names=world_data[0:15]["Country/Region"].values, hole=0.3, title=f"Top 15 Most Affected Countries by {i}")
        st.plotly_chart(pie_chart)

    st.plotly_chart(deaths_to_confirmed_fig)

@st.cache_data
def draw_right_figures():
    st.plotly_chart(bar_chart)
    st.plotly_chart(bar_chart_deaths)
    st.plotly_chart(bar_chart_active)

    for i in columns[2:]:
        fig = px.treemap(world_data.iloc[0:20], values=i, path=["Country/Region"], title=f"Treemap representation of different countries based on their {i}", labels={"labels": "Country"}, template="plotly_dark")
        st.plotly_chart(fig)

    for i in columns[2:]:
        pie_chart = px.pie(world_data[0:15], values=i, names=world_data[0:15]["Country/Region"].values, hole=0.3, title=f"Top 15 Most Affected Countries by {i}")
        st.plotly_chart(pie_chart)

    st.plotly_chart(bar_chart_recovered)


def draw_web():
    st.header("Covid-19 analysis")
    st.write("----")
    left_col, right_col = st.columns(2)
    with left_col:
        draw_left_figures()
    with right_col:
        draw_right_figures()

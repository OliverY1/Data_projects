
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_resource
def load_data():
    uber = pd.read_csv(r"datasets/uber.csv")
    pivot1 = pd.read_csv(r"datasets/pivot1.csv")
    pivot1.index.name = "Day/Hour"
    pivot1.reset_index()
    pivot1.drop("Day", axis=1, inplace=True)
    summary = pd.read_csv(r"datasets/summary.csv")
    uberfoil = pd.read_csv(r"datasets/uberfoil.csv")
    rushuber = pd.read_csv(r"datasets/rushuber.csv")
    return uber, pivot1, summary, uberfoil, rushuber

@st.cache_resource
def create_figures(summary, uberfoil, uber):
    fig = px.scatter(summary, x='Hour', y='size', color='Weekday',
                     height=500, width=750, labels={'size': 'Size', 'Hour': 'Hour of Day'},
                     category_orders={'Weekday': ['Monday', 'Tuesday', 'Wednesday', "Thursday", "Friday", "Saturday", "Sunday"]})
    fig.update_traces(mode='lines+markers')

    pivot = pd.crosstab(index=uber["Month"], columns=uber["Weekday"])
    boxfig = px.box(x="dispatching_base_number", y="active_vehicles", data_frame=uberfoil, height=500, width=750)
    return fig, boxfig, pivot

uber, pivot1, summary, uberfoil, rushuber = load_data()
fig, boxfig, pivot = create_figures(summary, uberfoil, uber)


def draw_bar_chart():
    st.header("Monthly Pickup Counts")
    st.bar_chart(pivot, width=500, height=500)
    #st.write("____")

#@st.cache_resource
def draw_map():
    st.header("Heatmap of Uber Rides")
    st.map(rushuber, latitude="Lat", longitude="Lon")

def draw():
    st.header('Hourly Ride Requests by Weekday')
    st.plotly_chart(fig)
    #st.write("____")

    st.header("Active Vehicles by Dispatching Base Number")
    st.plotly_chart(boxfig)
    #st.write("____")

@st.cache_data
def uber_project():
    st.title("Uber Data Analysis and Visualization")
    st.write("This project involves analyzing and visualizing Uber ride data to extract meaningful insights and patterns.")
    st.write("Please give the data some time to load.")
    st.markdown("[Download raw datasets](https://drive.google.com/drive/folders/1JnVPwus3H9YMN0WJhXDLA7x_dot33mUA)")
    st.write("____")

    col1, col2 = st.columns(2)

    with col1:
        draw_bar_chart()
        st.header("Hourly Ride Counts by Day")
        st.dataframe(pivot1.style.background_gradient(), height=500, width=830)
    with col2:
        draw()

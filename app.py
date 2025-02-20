
import base64
import streamlit as st
from streamlit_option_menu import option_menu as op
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Youness", page_icon="💡", layout="wide", initial_sidebar_state="auto")
import cars_analysis, uber_analysis, covid_analysis, sorting

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            header {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

selected = op(
    menu_title=None,
    options=["", "Covid analysis", "Cars analysis", "Uber analysis", "Sort algorithms"],
    icons=["house-door-fill", "virus2", "car-front-fill", "taxi-front", "sort-up"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal")

if selected == "Uber analysis":
    st.title("Uber New York Data Analysis")
    st.divider()
    if st.button("Press to see Map of uber rides"):
        uber_analysis.draw_map()

    uber_analysis.uber_project()

if selected == "Cars analysis":
    cars_analysis.car_project()

if selected =="Covid analysis":
    covid_analysis.draw_web()

if selected =="Sort algorithms":
    sorting.sort_project()


# Background setting
def set_background(png_file):
    with open(png_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    page_bg_img = f'''
    <style>
    .stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

background = r"datasets/background2.jpg"
if selected == "":
    set_background(background)
    col1,col2,col3 = st.columns([1,3,1])
    with col2:
        st.title("Oliver Youness")
        st.subheader("Computer science student in KTH, Stockholm")
        st.write("Welcome to my projects in Data Science! Have a look at some of my work and check out the source code! Learn more about me on LinkedIn.")
        st.markdown("[My Linkedin](https://www.linkedin.com/in/oliver-youness-041002302/)")
        st.markdown("[Projects source code](https://github.com/OliverY1/Data_projects/blob/main/app.py)")

        st.write("More projects are on the way!")

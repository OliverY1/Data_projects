import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd
import sort_algorithms.bubble_sort as bubble
import sort_algorithms.insertionsort as insertion
import sort_algorithms.selectionsort as selection
import sort_algorithms.mergesort as merge
import sort_algorithms.quicksort as quick

def sort_project():
    st.title("Sorting algorithms")

    col1,col2 = st.columns([1,2])

    with col1:
        sort_selected = st.selectbox("Choose sorting algorithm", options=["Merge sort",
        "Bubble sort","Insertion sort","Selection sort", "Quicksort"])

        if sort_selected is not "Quicksort":
            amount = st.slider("List length", min_value=3, max_value=500, value=100)
        else:
            amount = st.slider("List length", min_value=3, max_value=1000, value=500)

        sleep_time = st.slider("Time interval",min_value=0.0, max_value=1.0, step=0.01, value=0.0)


    lst = np.random.randint(0, 500, amount)


    with col2:
        placeholder = st.empty()
        if sort_selected=="Bubble sort":
            bubble.bubblesort(placeholder, lst,sleep_time)

        if sort_selected == "Insertion sort":
            insertion.insertionSort(placeholder,lst,sleep_time)

        if sort_selected == "Selection sort":
            selection.selectionSort(placeholder, lst, sleep_time)

        if sort_selected == "Merge sort":
            merge.mergeSort(placeholder, lst,sleep_time,0,len(lst)-1)

        if sort_selected =="Quicksort":
            quick.quickSort(placeholder, lst, sleep_time, 0,len(lst)-1)

import plotly.express as px
import streamlit as st
import time

def selectionSort(placeholder, lst, sleep_time):
    
    for index in range(len(lst)):
        min_index = index
 
        for j in range(index + 1, len(lst)):
            if lst[j] < lst[min_index]:
                min_index = j
        (lst[index], lst[min_index]) = (lst[min_index], lst[index])

        placeholder.bar_chart(lst)
        time.sleep(sleep_time)
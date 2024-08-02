import plotly.express as px
import streamlit as st
import time

def bubblesort(placeholder, lst, sleep_time):
    n= len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
            
            placeholder.bar_chart(lst)
            time.sleep(sleep_time)
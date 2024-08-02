import plotly.express as px
import streamlit as st
import time


def insertionSort(placeholder, lst, sleep_time):
    n = len(lst)  # Get the length of the array
      
    if n <= 1:
        return  # If the array has 0 or 1 element, it is already sorted, so return
 
    for i in range(1, n):  # Iterate over the array starting from the second element
        key = lst[i]  # Store the current element as the key to be inserted in the right position
        j = i-1
        while j >= 0 and key < lst[j]:  # Move elements greater than key one position ahead
            lst[j+1] = lst[j]  # Shift elements to the right
            j -= 1
        lst[j+1] = key

        placeholder.bar_chart(lst)
        time.sleep(sleep_time)
import streamlit as st
import time


def partition(lst, low, high):
    pivot = lst[high]
    i = low - 1
    for j in range(low, high):
        if lst[j] <= pivot:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    return i + 1
 

def quickSort(placeholder, lst, sleep_time, low, high):
    if low < high:

        pi = partition(lst, low, high)
 
        quickSort(placeholder, lst, sleep_time, low, pi - 1)
 
        quickSort(placeholder, lst, sleep_time, pi + 1, high)

        placeholder.bar_chart(lst)
        time.sleep(sleep_time)
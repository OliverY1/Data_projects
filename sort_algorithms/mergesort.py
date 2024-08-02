import streamlit as st
import time


def merge(lst, l, m, r):
    n1 = m - l + 1
    n2 = r - m
 

    L = [0] * (n1)
    R = [0] * (n2)
 

    for i in range(0, n1):
        L[i] = lst[l + i]
 
    for j in range(0, n2):
        R[j] = lst[m + 1 + j]
 

    i = 0    
    j = 0   
    k = l    
 
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            lst[k] = L[i]
            i += 1
        else:
            lst[k] = R[j]
            j += 1
        k += 1
 
    while i < n1:
        lst[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        lst[k] = R[j]
        j += 1
        k += 1
 
 
def mergeSort(placeholder,lst,sleep_time, l, r):
    if l < r:

        m = l+(r-l)//2
 
        mergeSort(placeholder,lst,sleep_time, l, m)
        mergeSort(placeholder,lst,sleep_time, m+1, r)
        merge(lst, l, m, r)

        placeholder.bar_chart(lst)
        time.sleep(sleep_time)
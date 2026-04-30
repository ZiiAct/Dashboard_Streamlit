import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
sns.set(style='dark')

@st.cache_data
def load_data():
    if os.path.exists("main_data.csv.gz"):
        df = pd.read_csv("main_data.csv.gz", compression="gzip")
    elif os.path.exists("main_data.zip"):
        df = pd.read_csv("main_data.zip")
    elif os.path.exists("main_data.csv"):
        df = pd.read_csv("main_data.csv")
    else:
        return None
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

all_df = load_data()

if all_df is None:
    st.error("File data tidak ditemukan! Pastikan file 'main_data.csv.gz', 'main_data.zip', atau 'main_data.csv' sudah di-upload ke GitHub.")
    st.stop() 

with st.sidebar:
    st.title("Filter Data ⚙️")
    
    min_date = all_df["datetime"].min().date()
    max_date = all_df["datetime"].max().date()
    
    date_range = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date, 
        max_value=max_date,
        value=[min_date, max_date]
    )
    if len(date_range) != 2:
        st.warning("Silakan pilih tanggal awal dan akhir.")
        st.stop()
        
    start_date,

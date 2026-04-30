import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# --- 1. LOAD DATA DENGAN PENGECEKAN ---
# Cek apakah file csv hasil cleaning sudah ada di folder
file_path = "main_data.csv"

if os.path.exists(file_path):
    all_df = pd.read_csv(file_path)
    all_df['datetime'] = pd.to_datetime(all_df['datetime'])
else:
    st.error(f"File '{file_path}' tidak ditemukan! Pastikan kamu sudah menjalankan 'air_quality_df.to_csv(\"main_data.csv\", index=False)' di Colab dan mengunduhnya.")
    st.stop() # Berhenti di sini jika data tidak ada

# --- 2. SIDEBAR FILTER ---
with st.sidebar:
    st.title("Filter Data")
    # Filter Rentang Waktu
    min_date, max_date = all_df["datetime"].min(), all_df["datetime"].max()
    
    # Handle jika date_input hanya mengembalikan 1 nilai saat user sedang memilih
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date, max_value=max_date,
        value=[min_date, max_date]
    )

# Pastikan user memilih rentang (start dan end)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.warning("Silakan pilih rentang tanggal (mulai dan selesai).")
    st.stop()

# --- 3. FILTERING DATA ---
main_df = all_df[(all_df["datetime"] >= pd.to_datetime(start_date)) & 
                 (all_df["datetime"] <= pd.to_datetime(end_date))]

# --- 4. DASHBOARD MAIN PAGE ---
st.header('Air Quality Dashboard 🌬️')

# Pastikan main_df tidak kosong sebelum menghitung metrik
if not main_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        total_obs = len(main_df)
        st.metric("Total Observasi", value=total_obs)

    with col2:
        # Gunakan fillna(0) agar tidak mengirim NoneType ke metric
        avg_pm25 = main_df['PM2.5'].mean()
        avg_pm25_val = round(avg_pm25, 2) if pd.notnull(avg_pm25) else 0.0
        st.metric("Rata-rata PM2.5", value=f"{avg_pm25_val} µg/m³")

    # Visualisasi Pertanyaan 1: PM2.5 di Dongsi & Guanyuan
    st.subheader("Rata-rata PM2.5 Jam Sibuk (Dongsi vs Guanyuan)")
    winter_rush = main_df[
        (main_df['month'].isin([12, 1, 2])) & 
        (main_df['hour'].isin([7, 8, 9, 17, 18, 19])) &
        (main_df['station'].isin(['Dongsi', 'Guanyuan']))
    ]
    
    if not winter_rush.empty:
        avg_q1 = winter_rush.groupby('station')['PM2.5'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='station', y='PM2.5', data=avg_q1, palette='muted', ax=ax)
        ax.axhline(75, color='red', linestyle='--')
        st.pyplot(fig)
    else:
        st.info("Tidak ada data untuk kriteria jam sibuk musim dingin di rentang waktu ini.")

else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

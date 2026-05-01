import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
sns.set_style('darkgrid')

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_gz = os.path.join(base_dir, "main_data.csv.gz")
    path_zip = os.path.join(base_dir, "main_data.zip")
    path_csv = os.path.join(base_dir, "main_data.csv")
    
    if os.path.exists(path_gz):
        df = pd.read_csv(path_gz, compression="gzip")
    elif os.path.exists(path_zip):
        df = pd.read_csv(path_zip)
    elif os.path.exists(path_csv):
        df = pd.read_csv(path_csv)
    else:
        return None
        
    # --- TRIK OPTIMASI MEMORI (HEMAT RAM HINGGA 60%) ---
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['station'] = df['station'].astype('category') # Ubah teks stasiun jadi kategori
    
    # Perkecil ukuran tipe data angka (Downcasting)
    float_cols = df.select_dtypes(include=['float64']).columns
    df[float_cols] = df[float_cols].astype('float32')
    
    int_cols = df.select_dtypes(include=['int64']).columns
    df[int_cols] = df[int_cols].astype('int32')
    
    return df

all_df = load_data()

if all_df is None:
    st.error("Data tidak ditemukan! Pastikan file data sudah ada di repository.")
    st.stop()

with st.sidebar:
    st.title("Filter Data ⚙️")
    min_date = all_df["datetime"].min().date()
    max_date = all_df["datetime"].max().date()
    
    date_range = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date, 
        max_value=max_date,
        value=(min_date, max_date)
    )
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    stasiun_list = all_df['station'].unique()
    selected_stations = st.multiselect(
        label="Pilih Stasiun",
        options=list(stasiun_list), # Convert category back to list for multiselect
        default=list(stasiun_list)
    )

main_df = all_df[
    (all_df["datetime"].dt.date >= start_date) & 
    (all_df["datetime"].dt.date <= end_date) &
    (all_df["station"].isin(selected_stations))
]

st.title('Air Quality Analysis Dashboard 🌬️')

if not main_df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Observasi", value=f"{len(main_df):,}")
    col2.metric("Rata-rata PM2.5", value=f"{main_df['PM2.5'].mean():.2f} µg/m³")
    col3.metric("Rata-rata PM10", value=f"{main_df['PM10'].mean():.2f} µg/m³")

    st.divider()
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("PM2.5 di Jam Sibuk Musim Dingin")
        winter_rush_df = main_df[main_df['month'].isin([12, 1, 2]) & main_df['hour'].isin([7, 8, 9, 17, 18, 19])]
        if not winter_rush_df.empty:
            avg_pm25_df = winter_rush_df.groupby('station')['PM2.5'].mean().reset_index()
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            sns.barplot(
                x='PM2.5', y='station', 
                data=avg_pm25_df.sort_values('PM2.5', ascending=False), 
                hue='station', palette='viridis', legend=False, ax=ax1
            )
            ax1.axvline(x=75, color='red', linestyle='--', label='Batas (75)')
            ax1.set_xlabel("Rata-rata PM2.5")
            ax1.set_ylabel("")
            st.pyplot(fig1)
            plt.close(fig1) # Tutup plot agar RAM tidak bocor

    with col_right:
        st.subheader("Frekuensi PM10 > 150 µg/m³ (Q4 2016)")
        danger_pm10_df = main_df[(main_df['year'] == 2016) & (main_df['month'].isin([10, 11, 12])) & (main_df['PM10'] > 150)]
        if not danger_pm10_df.empty:
            freq_df = danger_pm10_df['station'].value_counts().reset_index()
            freq_df.columns = ['station', 'total_jam']
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            sns.barplot(
                x='total_jam', y='station', 
                data=freq_df, 
                hue='station', palette='Reds_r', legend=False, ax=ax2
            )
            ax2.set_xlabel("Total Jam Kejadian")
            ax2.set_ylabel("")
            st.pyplot(fig2)
            plt.close(fig2) # Tutup plot agar RAM tidak bocor

    st.divider()
    st.subheader("Hubungan Cuaca dan Polutan")
    num_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    available_cols = [col for col in num_cols if col in main_df.columns]
    
    if available_cols:
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.heatmap(main_df[available_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
        st.pyplot(fig3)
        plt.close(fig3) # Tutup plot heatmap yang sangat berat
else:
    st.warning("Data kosong. Ubah filter stasiun/tanggal di menu samping.")

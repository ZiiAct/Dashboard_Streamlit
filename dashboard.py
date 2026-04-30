import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
sns.set(style='dark')

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
        df['datetime'] = pd.to_datetime(df['datetime'])
    return df
    
all_df = load_data()

if all_df is None:
    st.error("File data tidak ditemukan! Pastikan file 'main_data.csv.gz', 'main_data.zip', atau 'main_data.csv' sudah di-upload ke GitHub.")
    st.stop() 

with st.sidebar:
    st.title("Filter Data ⚙️")
    
    # Filter Waktu
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
        
    start_date, end_date = date_range
    
    stasiun_list = all_df['station'].unique()
    selected_stations = st.multiselect(
        label="Pilih Stasiun",
        options=stasiun_list,
        default=stasiun_list 
    )

main_df = all_df[
    (all_df["datetime"].dt.date >= start_date) & 
    (all_df["datetime"].dt.date <= end_date) &
    (all_df["station"].isin(selected_stations))
]

st.title('Air Quality Analysis Dashboard 🌬️')
st.markdown("Dashboard ini interaktif. Silakan gunakan filter di menu samping untuk mengeksplorasi data.")

if not main_df.empty:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Observasi", value=f"{len(main_df):,}")
    with col2:
        avg_pm25 = main_df['PM2.5'].mean()
        st.metric("Rata-rata PM2.5", value=f"{avg_pm25:.2f} µg/m³")
    with col3:
        avg_pm10 = main_df['PM10'].mean()
        st.metric("Rata-rata PM10", value=f"{avg_pm10:.2f} µg/m³")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("PM2.5 di Jam Sibuk Musim Dingin")
        
        winter_rush_df = main_df[
            (main_df['month'].isin([12, 1, 2])) & 
            (main_df['hour'].isin([7, 8, 9, 17, 18, 19]))
        ]
        
        if not winter_rush_df.empty:
            avg_pm25_df = winter_rush_df.groupby('station')['PM2.5'].mean().reset_index()
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            sns.barplot(x='PM2.5', y='station', data=avg_pm25_df.sort_values('PM2.5', ascending=False), palette='viridis', ax=ax1)
            ax1.axvline(x=75, color='red', linestyle='--', label='Batas Tidak Sehat (75)')
            ax1.legend()
            ax1.set_xlabel("Rata-rata PM2.5")
            ax1.set_ylabel("")
            st.pyplot(fig1)
        else:
            st.info("Tidak ada data jam sibuk musim dingin di rentang waktu/stasiun yang dipilih.")

    with col_right:
        st.subheader("Frekuensi PM10 Berbahaya (>150 µg/m³)")
        
        danger_pm10_df = main_df[
            (main_df['year'] == 2016) & 
            (main_df['month'].isin([10, 11, 12])) & 
            (main_df['PM10'] > 150)
        ]
        
        if not danger_pm10_df.empty:
            freq_df = danger_pm10_df['station'].value_counts().reset_index()
            freq_df.columns = ['station', 'total_jam']
            
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            sns.barplot(x='total_jam', y='station', data=freq_df, palette='Reds_r', ax=ax2)
            ax2.set_xlabel("Total Jam Kejadian")
            ax2.set_ylabel("")
            st.pyplot(fig2)
        else:
            st.info("Tidak ada kejadian PM10 > 150 pada Q4 2016 di rentang waktu/stasiun yang dipilih.")

    st.divider()
    
    st.subheader("Analisis Lanjutan: Hubungan Cuaca dan Polutan")
    
    num_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    available_cols = [col for col in num_cols if col in main_df.columns]
    
    corr_matrix = main_df[available_cols].corr()
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax3)
    st.pyplot(fig3)

else:
    st.warning("Data kosong. Silakan atur ulang filter di sidebar.")

st.caption("Proyek Analisis Data | Kualitas Udara")

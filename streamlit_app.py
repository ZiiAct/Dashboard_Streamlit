import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Data Dashboard", layout="wide")

# 2. Load Data (Contoh menggunakan DataFrame dummy)
@st.cache_data # Mengoptimalkan kecepatan load data
def load_data():
    df = pd.DataFrame({
        "Produk": ["A", "B", "C", "D"],
        "Penjualan": [100, 150, 80, 200],
        "Kategori": ["Elektronik", "Elektronik", "Pakaian", "Pakaian"]
    })
    return df

df = load_data()

# 3. Sidebar untuk Filter
st.sidebar.header("Filter Data")
kategori_pilihan = st.sidebar.multiselect(
    "Pilih Kategori:",
    options=df["Kategori"].unique(),
    default=df["Kategori"].unique()
)

df_filtered = df[df["Kategori"].isin(kategori_pilihan)]

# 4. Main Content (Judul dan Visualisasi)
st.title("📊 Sales Dashboard")
st.markdown("Dashboard interaktif untuk memantau performa penjualan.")

# Baris pertama: Metrik Utama
col1, col2 = st.columns(2)
col1.metric("Total Produk", len(df_filtered))
col2.metric("Total Penjualan", df_filtered["Penjualan"].sum())

# Baris kedua: Grafik
fig = px.bar(df_filtered, x="Produk", y="Penjualan", color="Kategori", title="Penjualan per Produk")
st.plotly_chart(fig, use_container_width=True)

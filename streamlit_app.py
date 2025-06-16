import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Dashboard Data Finish", layout="wide", page_icon="📊")

# Load data
df = pd.read_csv("D:/Data engineering/DATA/dataFinish.csv")

# Sidebar - Filter
st.sidebar.header("Filter Data")
columns = df.columns.tolist()

with st.sidebar:
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        col1 = st.selectbox("Pilih Kolom Numerik untuk Analisis", numeric_cols)
        show_hist = st.checkbox("Tampilkan Histogram", value=True)
        show_box = st.checkbox("Tampilkan Boxplot", value=True)

    cat_cols = df.select_dtypes(include='object').columns.tolist()
    if cat_cols:
        cat_col = st.selectbox("Pilih Kolom Kategori", cat_cols)

# Header
st.title("📊 Dashboard Visualisasi Data Finish")

# Ringkasan Data
st.subheader("📌 Ringkasan Data")
st.dataframe(df.head(), use_container_width=True)

# Statistik Deskriptif
with st.expander("🔍 Statistik Deskriptif"):
    st.write(df.describe())

# Visualisasi Histogram dan Boxplot
if numeric_cols:
    st.subheader(f"📈 Visualisasi Data Numerik: {col1}")
    col1_data = df[col1].dropna()
    if show_hist:
        fig_hist = px.histogram(df, x=col1, nbins=30, title=f"Histogram dari {col1}")
        st.plotly_chart(fig_hist, use_container_width=True)

    if show_box:
        fig_box = px.box(df, y=col1, title=f"Boxplot dari {col1}")
        st.plotly_chart(fig_box, use_container_width=True)

# Visualisasi Kategori
if cat_cols:
    st.subheader(f"📊 Visualisasi Frekuensi Kategori: {cat_col}")
    cat_counts = df[cat_col].value_counts().reset_index()
    cat_counts.columns = [cat_col, "Jumlah"]
    fig_bar = px.bar(cat_counts, x=cat_col, y="Jumlah", title=f"Jumlah per Kategori di {cat_col}")
    st.plotly_chart(fig_bar, use_container_width=True)

# Korelasi Antar Kolom Numerik
st.subheader("🔗 Korelasi Antar Kolom Numerik")
if len(numeric_cols) >= 2:
    corr = df[numeric_cols].corr()
    fig_corr, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig_corr)

# Visualisasi Kolom Numerik per Provinsi
st.subheader("📍 Visualisasi Kolom Numerik per Provinsi")

if "Provinsi" in df.columns:
    columns_to_plot = [
        "Jumlah Penduduk 2024", 
        "Timbulan Sampah Tahunan (kg)", 
        "Tidak Ada Pencemaran",
        "Sampah_per_Kapita_kg", 
        "Total_Pencemaran_Desa", 
        "Analisis_Pengelolaan", 
        "Dominasi_Pencemaran"
    ]

    for col in columns_to_plot:
        if col in df.columns:
            st.markdown(f"### 📌 {col}")
            fig = px.bar(df, x="Provinsi", y=col,
                         title=f"{col} per Provinsi",
                         labels={"Provinsi": "Provinsi", col: col})
            st.plotly_chart(fig, use_container_width=True)

    # Gabungan Pencemaran Air, Tanah, dan Udara
    pollution_cols = ["Pencemaran Air", "Pencemaran Tanah", "Pencemaran Udara"]
    available = [col for col in pollution_cols if col in df.columns]

    if len(available) == 3:
        st.markdown("### 🌍 Grafik Gabungan Pencemaran Air, Tanah, dan Udara")
        df_pollution = df[["Provinsi"] + available].melt(
            id_vars="Provinsi", 
            var_name="Jenis Pencemaran", 
            value_name="Jumlah"
        )
        fig_pollution = px.bar(
            df_pollution,
            x="Provinsi",
            y="Jumlah",
            color="Jenis Pencemaran",
            barmode="group",
            title="Pencemaran Air, Tanah, dan Udara per Provinsi"
        )
        st.plotly_chart(fig_pollution, use_container_width=True)
else:
    st.warning("Kolom 'Provinsi' tidak ditemukan. Tidak dapat menampilkan grafik per-provinsi.")

# Footer
st.markdown("---")
st.markdown("📁 Dibuat oleh Kelompok 4 - Streamlit Dashboard")

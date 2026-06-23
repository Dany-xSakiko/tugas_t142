import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ==========================================
# KONFIGURASI HALAMAN & TEMA PERSONALISASI
# ==========================================
st.set_page_config(
    page_title="Simulator Profit",
    layout="wide", # Layout lebar lebih modern
    initial_sidebar_state="expanded"
)

# Custom CSS untuk Personalisasi (Anime/Japanese aesthetic)
# Warna primer: Sakura Pink (#FFB7C5), Purple Accent (#8159E0)
# Warna latar sidebar: Gelap lembut (#262730)
st.markdown(
    """
    <style>
        /* Mengubah font global dan background utama */
        .main {
            background-color: #0E1117; /* Gelap default */
        }
        
        /* Personalisasi Judul Utama */
        h1 {
            color: #FFFFF; /* Warna Sakura Pink */
            font-family: 'Poppins', sans-serif;
            text-shadow: 2px 2px 4px rgba(255, 183, 197, 0.3);
            font-size: 3rem !important;
            padding-bottom: 0.5rem;
        }
        
        /* Personalisasi Sidebar */
        [data-testid="stSidebar"] {
            background-color: #262730; /* Sidebar background */
            border-right: 2px solid #FFFFF; /* Garis pembatas warna sakura */
        }
        [data-testid="stSidebar"] h2 {
            color: #FFFFF; /* Judul sidebar */
        }
        
        /* Personalisasi Slider */
        .stSlider [data-testid="stThumbValue"] {
            color: #FFB7C5; /* Warna teks nilai slider */
        }
        
        /* Membuat container hasil metrik membulat dan diberi bayangan */
        div[data-testid="stMetricValue"] {
            color: #FFFFF; /* Warna metrik utama */
            font-size: 3rem;
            font-weight: bold;
        }
        div[data-testid="stMetricDelta"] > div {
            color: #00FF00 !important; /* Warna delta positif hijau neon */
        }
        
        /* Styling untuk teks penjelas */
        .stMarkdown p {
            color: #FFFFF; /* Teks penjelas abu-abu lembut */
        }
        
        /* Tambahkan efek hover pada grafik */
        .vega-embed summary {
            border-color: #FFB7C5 !important;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 1. PERSIAPAN MODEL & BASELINE (Unchanged)
# ==========================================
X_train = np.array([[5, 10], [10, 20], [15, 5], [20, 25], [25, 15]])
y_train = np.array([50, 80, 110, 90, 150])
model = LinearRegression().fit(X_train, y_train)
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]


# ==========================================
# 2. STREAMLIT UI & SIDEBAR
# ==========================================

# --- HEADER PERSONALISASI ---
# Tambahkan visualisasi karakter atau ikon bertema (placeholder image)
with st.container():
    # Ane ubah rasio kolomnya sedikit biar ruang buat gambar (col_t1) lebih lega
    col_t1, col_t2 = st.columns([1.5, 3.5]) 
    
    with col_t1:
        st.image("test2.jpg", use_container_width=True)
        
    with col_t2:
        st.markdown('<h1>Simulator Profit</h1>', unsafe_allow_html=True)
        st.write("Sesuaikan strategi intervensi untuk melihat dampak langsung pada keuntungan toko kita!")


# --- LOGIKA SIMULATOR (Function) ---
def run_simulation(new_iklan, new_diskon):
    intervention_input = np.array([[new_iklan, new_diskon]])
    prediction = model.predict(intervention_input)[0]
    delta_y = prediction - baseline_pred
    return prediction, delta_y


# --- SIDEBAR: Tuas Kebijakan ---
st.sidebar.markdown('<h2 style="font-size: 1.5rem;">⚙️ Tuas Intervensi</h2>', unsafe_allow_html=True)
st.sidebar.write("Kendalikan variabel kebijakan:")

# Personalisasi slider dengan warna (menggunakan CSS di atas)
iklan_slider = st.sidebar.slider("📉 Anggaran Iklan (Juta)", 0, 50, 10, help="Ubah untuk simulasi skenario iklan")
diskon_slider = st.sidebar.slider("🏷️ Besaran Diskon (%)", 0, 50, 10, help="Ubah untuk simulasi skenario diskon")


# ==========================================
# 3. ENGINE & TAMPILAN HASIL (LAYOUT BARU)
# ==========================================

# --- JALANKAN SIMULASI ---
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)

# --- UI: LAYOUT KOLOM UNTUK HASIL ---
st.write("---") # Garis pembatas

col1, col2 = st.columns([2, 3]) # Bagian metrik lebih kecil, grafik lebih lebar

with col1:
    st.markdown("### ✨ Perkiraan Keuntungan")
    st.metric(
        label="Prediksi Keuntungan Baru",
        value=f"Rp {hasil_pred:.2f} Jt",
        delta=f"{delta:.2f} Jt (Selisih dari Baseline)",
        delta_color="normal" # CSS akan menangani pewarnaan delta
    )
    
    # Teks penjelas tambahan yang lebih ramah
    if delta > 0:
        st.info(f"Yatta! Skenario ini diprediksi menghasilkan kenaikan keuntungan sebesar Rp {delta:.2f} Juta dibandingkan kondisi baseline toko saat ini.")
    elif delta < 0:
        st.warning(f"Skenario ini diprediksi menyebabkan penurunan keuntungan sebesar Rp {abs(delta):.2f} Juta dibandingkan kondisi baseline toko. Hati-hati dalam intervensi.")
    else:
        st.write("Skenario saat ini sama dengan kondisi baseline toko. Tidak ada perubahan keuntungan.")


with col2:
    st.markdown("### 📊 Analisis Perbandingan Skenario")
    
    # Data untuk visualisasi
    data_plot = pd.DataFrame({
        'Status Skenario': ['Baseline', 'Intervensi'],
        'Keuntungan (Juta Rp)': [baseline_pred, hasil_pred]
    })
    
    # Tampilkan grafik batang (st.bar_chart) dengan warna default Streamlit
    # Catatan: st.bar_chart sulit diubah warnanya dengan CSS murni Streamlit.
    # Untuk warna sakura kustom penuh, gunakan plotly_chart (perlu library tambahan).
    # Agar tetap simple, kita pakai chart bawaan tapi berikan margin/padding CSS.
    st.bar_chart(data=data_plot, x='Status Skenario', y='Keuntungan (Juta Rp)', use_container_width=True)

# Teks kaki (opsional)
st.write("---")
st.markdown("<p style='text-align: center; color: #555;'>Created by Dany-xSakiko | Simulator v1.1 - Personalization Update</p>", unsafe_allow_html=True)

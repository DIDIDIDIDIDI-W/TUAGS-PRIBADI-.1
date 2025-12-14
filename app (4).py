import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Harga Pangan Banten", layout="wide")

# Judul Utama
st.title('📊 Dashboard Harga Komoditas Pangan Utama di Banten')
st.markdown("""
Dashboard ini menyajikan analisis perkembangan harga pangan strategis di wilayah Banten.
Data ini diambil dari laporan bulanan dan divisualisasikan untuk membantu memantau tren kenaikan atau penurunan harga.
""")

# Load data
# Menggunakan relative path untuk deployment
file_path = 'data banten ...xlsx'

try:
    df = pd.read_excel(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Process 'tahun' column
    df['tahun_date'] = pd.to_datetime(df['tahun'].astype(str).str.replace(' ', ''), format='%m/%Y', errors='coerce')

    # Sidebar untuk filter
    st.sidebar.header("Filter Tampilan")
    show_table = st.sidebar.checkbox("Tampilkan Tabel Data", value=True)

    if show_table:
        st.subheader("📋 Data Lengkap")
        # Menampilkan seluruh dataframe
        st.dataframe(df)
        st.caption(f"Menampilkan total {len(df)} baris data.")

    # Plotting Section
    st.divider()
    st.header("📈 Analisis Tren Harga")
    st.markdown("Grafik di bawah ini menunjukkan pergerakan harga komoditas pangan dari waktu ke waktu. Anda dapat mengamati pola musiman atau lonjakan harga yang tidak biasa.")

    target_komoditas = ['Beras', 'Daging Ayam', 'Daging Sapi', 'Bawang Merah',
                        'Cabai Rawit', 'Minyak Goreng', 'Gula Pasir']

    # Filter columns that exist in the dataframe
    komoditas_plot = [col for col in target_komoditas if col in df.columns]

    if komoditas_plot:
        # Opsi interaktif untuk memilih komoditas
        selected_commodities = st.multiselect(
            "Pilih Komoditas untuk Ditampilkan:",
            options=komoditas_plot,
            default=komoditas_plot
        )

        if selected_commodities:
            fig, ax = plt.subplots(figsize=(14, 7))
            for col in selected_commodities:
                sns.lineplot(data=df, x='tahun_date', y=col, label=col, ax=ax)

            ax.set_title('Dinamika Harga Komoditas Pangan', fontsize=16)
            ax.set_xlabel('Periode Waktu', fontsize=12)
            ax.set_ylabel('Harga (dalam Ribuan Rupiah)', fontsize=12)
            ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
            ax.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()

            st.pyplot(fig)

            # Penjelasan / Insight Tambahan
            st.info("""
            **💡 Insight Singkat:**
            *   **Beras & Gula Pasir**: Cenderung memiliki harga yang stabil dengan fluktuasi minim.
            *   **Cabai Rawit & Bawang Merah**: Sering mengalami volatilitas tinggi, biasanya dipengaruhi oleh faktor cuaca dan musim panen.
            *   **Daging Ayam**: Menunjukkan pola fluktuasi berkala.
            """)
        else:
            st.warning("Silakan pilih setidaknya satu komoditas untuk menampilkan grafik.")

    else:
        st.error("Komoditas yang dicari tidak ditemukan dalam data.")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.text("Pastikan file Excel berada di folder yang sama dengan app.py di repository GitHub Anda.")

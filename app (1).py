import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page title
st.title('Harga Komoditas Pangan Utama di Banten')

# Load data
# PENTING: Gunakan hanya nama file (relative path) untuk deployment GitHub
# Pastikan file Excel diletakkan di folder yang sama dengan app.py di repository GitHub
file_path = 'data banten ...xlsx'

try:
    df = pd.read_excel(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Process 'tahun' column
    df['tahun_date'] = pd.to_datetime(df['tahun'].astype(str).str.replace(' ', ''), format='%m/%Y', errors='coerce')

    st.header("Data Overview")
    st.dataframe(df.head())

    # Plotting
    st.header("Trend Harga Komoditas")
    
    target_komoditas = ['Beras', 'Daging Ayam', 'Daging Sapi', 'Bawang Merah',
                        'Cabai Rawit', 'Minyak Goreng', 'Gula Pasir']
    
    # Filter columns that exist in the dataframe
    komoditas_plot = [col for col in target_komoditas if col in df.columns]
    
    if komoditas_plot:
        fig, ax = plt.subplots(figsize=(14, 8))
        for col in komoditas_plot:
            sns.lineplot(data=df, x='tahun_date', y=col, label=col, ax=ax)
        
        ax.set_title('Perkembangan Harga Komoditas Pangan Utama di Banten')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Harga (dalam Ribuan/Satuan)')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True)
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.write("Komoditas yang dicari tidak ditemukan dalam data.")

except Exception as e:
    st.error(f"An error occurred: {e}")

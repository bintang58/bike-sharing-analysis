# Bike Sharing Analysis Dashboard 🚲

Dashboard interaktif ini dibuat menggunakan Streamlit untuk menganalisis data penyewaan sepeda berdasarkan dataset Bike Sharing Dataset. Dashboard ini memberikan wawasan tentang pola penggunaan berdasarkan musim, tren penyewaan sepeda harian, serta analisis RFM.

## 📌 Fitur Dashboard

- **Analisis Harian**: Menampilkan jumlah penyewaan sepeda oleh pengguna casual dan registered.
- **Musim dengan Penyewaan Tertinggi**: Visualisasi tren penyewaan berdasarkan musim.
- **Jam dengan Penyewaan Tertinggi & Terendah**: Mengidentifikasi jam sibuk dan sepi.
- **Analisis RFM**: Mengkategorikan pelanggan berdasarkan Recency, Frequency, dan Monetary.

## 🛠️ Instalasi dan Menjalankan Dashboard

Ikuti langkah-langkah berikut untuk menjalankan dashboard di lokal:

### 1️⃣ Clone Repository

```bash
git clone https://github.com/bintang58/bike-sharing-analysis
cd bike-sharing-analysis
```

### 2️⃣ Install Library

Pastikan sudah menginstal semua pustaka yang diperlukan dengan menjalankan perintah:

```bash
pip install -r requirements.txt
```

### 3️⃣ Jalankan Dashboard

Jalankan Streamlit untuk menampilkan dashboard:

```bash
streamlit run dashboard/dashboard.py
```

Atau Anda bisa langsung mengunjungi website berikut: [Bike Sharing Dashboard](https://bike-sharing-analysis-bintangcahyaa.streamlit.app/)

## 📂 Struktur File
```bash
📂 bike-sharing-analysis
├── 📂 dashboard
│   ├── dashboard.py
│   ├── day_clean.csv
|   ├── hour_clean.csv
|   └── logo.png
├── 📂 data
│   ├── Readme.txt
│   ├── day.csv
|   └── hour.csv
├── README.md
├── notebook.ipynb
└── requirements.txt
```

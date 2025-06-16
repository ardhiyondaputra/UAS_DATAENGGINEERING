# Data-Engineering-Kelompok-6
# Analisis Hubungan antara Timbulan Sampah, Pencemaran Lingkungan, dan Jumlah Penduduk di Indonesia
## Kontributor 
| Nama Lengkap | NIM | Peran |
| :---         |     :---:      |          :---: |
| Alridzki Innama N.R  | 234311031     | Data Analyst   |
| Ardhiyonda Wahyu P.V    | 234311032       | Data Engineer     |
| Arfan Bagus D. | 234311033     | Data Engineer   |
| Ramizah Budi C.P   | 234311049      | Project Manager     |
| Satria Bagus A.I   | 234311054       | Data Analyst     |
# Deskripsi Proyek 
Proyek ini dikembangkan untuk menganalisis 
# Manfaat Data / Use Case
- Tujuan Proyek : Proyek ini bertujuan untuk menganalisis hubungan antara jumlah penduduk, timbulan sampah, dan pencemaran lingkungan di Indonesia dengan membangun pipeline data yang mengotomatisasi proses pengumpulan, pengolahan, dan visualisasi data dari berbagai sumber.
- Manfaat : Manfaat dari proyek ini antara lain memberikan wawasan berbasis data untuk mendukung kebijakan lingkungan, menjadi referensi bagi penelitian lanjutan di bidang kependudukan dan lingkungan, meningkatkan kesadaran masyarakat terhadap dampak pertumbuhan penduduk, serta memberikan pengalaman praktis dalam penerapan teknik data engineering untuk pengolahan data lingkungan.
# Serving Analisis
Analisis pada proyek ini terdiri dari beberapa tahapan utama, yaitu pengambilan data dari sumber resmi seperti SIPSN, BPS, KLHK (extract), pembersihan dan penggabungan data berdasarkan provinsi dan tahun (transform), serta penyimpanan hasil ke dalam database PostgreSQL (aiven). Data yang telah tersimpan kemudian disajikan melalui visualisasi interaktif menggunakan tools seperti Streamlit untuk analisis tren dan korelasi. Selain itu, data juga dapat dimanfaatkan untuk keperluan machine learning seperti prediksi pengelolaan sampah, sehingga mendukung pengambilan keputusan berbasis data.
# Serving Machine Learning
Dalam proyek analisis Analisis Hubungan antara Timbulan Sampah, Pencemaran Lingkungan, dan Jumlah Penduduk di Indonesia, dimulai dari pengambilan data dari sumber resmi yaitu BPS dan SISKLHK atau yang disebut extract, pembersihan dan penggabungan data berdasarkan provinsi dan tahun atau yang disebut transform, serta penyimpanan hasil data ke dalam database PostGreSQL atau yang disebut Load. Serving Mechine adalah tahap penyajian data dan model yang telah diproses agar dapat digunakan oleh pengguna akhir. ini mencakup penyajian visualisasi interaktif melalui streamlit.
# Pipeline
## Extract (Pengambilan Data)
- Sumber Data
  - Data Timbulan Sampah - https://sipsn.menlhk.go.id/sipsn/public/data/timbulan
  - Banyaknya Jenis Pencemaran Lingkungan Hidup - https://www.bps.go.id/id/statistics-table/2/OTU5IzI=/banyaknya-desa-kelurahan-menurut-jenis-pencemaran-lingkungan-hidup.html
  - Jumlah Penduduk Menurut Provinsi di Indonesia - https://sulut.bps.go.id/id/statistics-table/2/OTU4IzI=/jumlah-penduduk-menurut-provinsi-di-indonesia.html
- Metode Pengambilan :
  - Scrapping HTML dengan Selenium untuk data BPS.
  - JSON untuk Data Timbulan Sampah.
  - Penyimpanan awal dalam format CSV atau langsung ke PostgreSQL.
# Transform (Pembersihan & Transformasi)
- Pembersihan :
  - Data yang diambil dari SIPSN, KLHK, BPS memiliki struktur yang berbeda sehingga perlu dibersihkan terlebih dahulu untuk memastikan kualitas dan konsistensinya. Langkah-langkah pembersihan meliputi:
    - Menghapus baris duplikat dan kolom tidak relevan dari masing-masing dataset.
    - Menangani nilai kosong (missing value) dengan cara menghapus atau melakukan imputasi sederhana jika memungkinkan.
    - Menstandarkan penulisan nama provinsi, misalnya menyamakan penulisan antara “JAKARTA” dan “Jakarta” agar proses penggabungan antar dataset dapat berjalan lancar.
    - Memastikan tipe data konsisten, seperti tahun dalam bentuk integer dan jumlah penduduk serta volume sampah dalam bentuk numerik.
- Transformasi :
  Setelah data bersih, dilakukan transformasi untuk menggabungkan dan menyesuaikan dataset:
  - Menggabungkan (join/merge) dataset berdasarkan atribut provinsi dan tahun agar setiap baris data mewakili kondisi suatu provinsi pada satu tahun tertentu.
  - Membuat fitur baru yang relevan dengan tujuan analisis, seperti:
  - Sampah per Kapita (kg/orang) = Total Timbulan Sampah / Jumlah Penduduk.
  - Total pencemaran = Total desa yang tercemar.
  - Konversi satuan data dari ton ke kilogram agar lebih mudah dibandingkan per individu.
# Load (Pemindahan ke Target)
- Target :
  Setelah proses transformasi selesai, dataset akhir dimuat ke dalam database PostgreSQL sebagai storage utama. PostgreSQL dipilih karena mendukung skema relasional, performa query yang baik, dan kompatibel dengan berbagai tools analitik serta machine learning pipeline.
  - Skema Database:
    Struktur tabel dibuat sederhana dan terstruktur untuk mendukung efisiensi analisis:
    - Tabel utama: data_lingkungan
    - Skema kolom: [Provinsi, Jumlah Penduduk 2024Timbulan Sampah Tahunan (kg), Pencemaran Air, Pencemaran Tanah, Pencemaran Udara]
- Proses Load :
  - Data dari hasil transformasi disimpan dalam format CSV terlebih dahulu untuk keperluan audit.
  - Proses pemindahan dilakukan menggunakan library seperti SQLAlchemy di Python.
  - Validasi dilakukan untuk memastikan tidak ada data duplikat, dan setiap baris dimasukkan berdasarkan kunci unik (provinsi + tahun).
  - Penanganan Duplikasi & Integritas Data:
  - Diterapkan primary key gabungan (provinsi, tahun) untuk mencegah entri ganda.
  - Data lama akan diupdate jika sudah ada dan terjadi perubahan nilai.
  - Pengecekan integritas dilakukan secara otomatis sebelum proses insert menggunakan validasi skema.
# Arsitektur/Workflow ETL
- Alur Modular : Workflow ini menjelaskan alur kerja yang dimulai dari pengambilan data melalui proses scraping, kemudian dilanjutkan dengan pembersihan dan transformasi data, lalu data di load ke database melalui PostGreSQL. hingga akhirnya data siap untuk dianalisis atau divisualisasikan.
- Teknologi yang Digunakan :
  - ETL: Python, Selenium, Pandas, SQLAlchemy, time,numpy
  - Machine Learning: Scikit-learn
  - Database: PostGreSQL(Aiven)
  - Visualisasi: Matplotlib, Seaborn, Streamlit
# Kode Program
- Struktur Kode :
  - Tersusun rapi per bagian: ETL, Visualisasi, Modeling
  - Terdapat 2 Notebook : satu untuk ETL dan satu untuk Machine Learning
  - Penamaan variabel deskriptif, data pipeline terotomatisasi
- Machine Learning :
  - Menggunakan model regresi linear
# Link Proyek :
- ETL Pipeline : https://github.com/ardhiyondaputra/UAS_DATAENGGINEERING/blob/main/UAS_DATA_ENGGINEER_1.ipynb
- Machine Learning : https://github.com/ardhiyondaputra/UAS_DATAENGGINEERING/blob/main/ML.ipynb
- Streamlit : https://github.com/ardhiyondaputra/UAS_DATAENGGINEERING/blob/main/streamlit_app.py

# Bank Transaction Fraud Detection: Machine Learning
Clustering-driven Classification for Transaction Security

## Deskripsi Proyek
Proyek ini bertujuan untuk membangun sistem deteksi anomali pada transaksi perbankan. Karena dataset awal tidak memiliki label (target), proyek ini menerapkan pendekatan Hybrid Machine Learning:
1. Unsupervised Learning (Clustering): Mengelompokkan transaksi menggunakan K-Means untuk menghasilkan label otomatis.
2. Supervised Learning (Classification): Membangun model Decision Tree (dan algoritma lainnya) untuk memprediksi label hasil clustering berdasarkan fitur-fitur transaksi.

## Struktur Proyek & Kriteria
Proyek ini dikerjakan dengan memenuhi kriteria sebagai berikut:

1. Exploratory Data Analysis (EDA)
    - Analisis statistik deskriptif (describe, info, head).

    - Visualisasi matriks korelasi untuk melihat hubungan antar fitur.

    - Histogram distribusi untuk fitur numerik dan kategorikal dengan label yang rapi (tidak overlap).

2. Data Preprocessing
    - Penanganan missing values dan data duplikat.

    - Handling Outliers dengan metode drop.

    - Feature Engineering: Encoding menggunakan LabelEncoder dan scaling menggunakan StandardScaler.

    - Penerapan Data Binning pada fitur numerik untuk meningkatkan performa model.

3. Clustering Model (Unsupervised)
    - Penentuan jumlah cluster optimal menggunakan Elbow Method (KElbowVisualizer).

    - Implementasi K-Means Clustering.

    - Reduksi dimensi menggunakan PCA (Principal Component Analysis) untuk visualisasi dan optimasi cluster.

    - Evaluasi menggunakan Silhouette Score.

4. Interpretasi & Integrasi Data
    - Analisis deskriptif karakteristik tiap cluster (Mean, Min, Max).

    - Inverse Transform: Mengembalikan data ke bentuk asli untuk interpretasi bisnis yang lebih mudah.

    - Export data hasil clustering ke dalam kolom Target.

5. Classification Model (Supervised)
    - Pembagian data menggunakan train_test_split.

    - Model Utama: Decision Tree Classifier.

    - Eksperimen dengan algoritma tambahan (XGBoost/Random Forest) dan Hyperparameter Tuning untuk mendapatkan akurasi, presisi, recall, dan F1-Score terbaik.
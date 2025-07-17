import pandas as pd
import mysql.connector
from mysql.connector import Error
import joblib

# Load model Logistic Regression
try:
    model = joblib.load('model_logistic_portable.pkl')
except FileNotFoundError:
    raise FileNotFoundError("Model file tidak ditemukan.")

# Buat koneksi ke database MySQL
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='gaji_karyawan_db'
        )
        return conn
    except Error as e:
        raise ConnectionError(f"Koneksi ke database gagal: {e}")

# Fungsi untuk prediksi gaji dari input pengguna
def predict_salary(data: dict):
    # Buat DataFrame dari input
    input_df = pd.DataFrame([{
        'Umur': int(data['umur']),
        'Kelas Pekerja': data['kelas_pekerja'],
        'Pendidikan': data['pendidikan'],
        'Status Perkawinan': data['status_perkawinan'],
        'Pekerjaan': data['pekerjaan'],
        'Jenis Kelamin': data['jenis_kelamin'],
        'Jam per Minggu': float(data['jam_per_minggu']),

        # Kolom tambahan yang sudah dihapus di frontend tapi diperlukan model
        'Berat Akhir': 1,
        'Jmlh Tahun Pendidikan': 10,
        'Keuntungan Kapital': 0.0,
        'Kerugian Capital': 0.0
    }])

    # Mapping nilai kategorikal (jenis kelamin)
    input_df['Jenis Kelamin'] = input_df['Jenis Kelamin'].map({'Perempuan': 0, 'Laki2': 1})

    # One-hot encoding
    input_encoded = pd.get_dummies(input_df)

    # Tambahkan kolom yang tidak muncul agar cocok dengan model
    for col in model.feature_names_in_:
        if col not in input_encoded.columns:
            input_encoded[col] = 0

    # Pastikan urutan kolom sama dengan saat training
    input_encoded = input_encoded[model.feature_names_in_]

    # ✅ Penting: hilangkan semua NaN agar tidak error
    input_encoded = input_encoded.fillna(0)

    # Prediksi
    pred = model.predict(input_encoded)[0]
    kategori = '>7jt' if pred == 1 else '<=7jt'

    return kategori, input_df

# Simpan input + hasil prediksi ke database
def save_to_database(data: dict, gaji: str):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO data_pengguna (
            umur, kelas_pekerja, pendidikan,
            status_perkawinan, pekerjaan, jenis_kelamin,
            jam_per_minggu, gaji
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['umur'],
        data['kelas_pekerja'],
        data['pendidikan'],
        data['status_perkawinan'],
        data['pekerjaan'],
        data['jenis_kelamin'],
        data['jam_per_minggu'],
        gaji
    ))

    conn.commit()
    cursor.close()
    conn.close()

# Ambil semua hasil prediksi dari database
def fetch_all_predictions():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data_pengguna ORDER BY umur DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows)

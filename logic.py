import pandas as pd
import mysql.connector
from mysql.connector import Error
import joblib

# Load model dan info
try:
    model = joblib.load('logistic_model.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    model_columns = joblib.load('model_columns.pkl')
except FileNotFoundError as e:
    raise FileNotFoundError(f"File model tidak ditemukan: {e}")

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

def predict_salary(data: dict):
    input_df = pd.DataFrame([{
        'Umur': int(data['umur']),
        'Kelas Pekerja': data['kelas_pekerja'],
        'Pendidikan': data['pendidikan'],
        'Status Perkawinan': data['status_perkawinan'],
        'Pekerjaan': data['pekerjaan'],
        'Jenis Kelamin': data['jenis_kelamin'],
        'Jam per Minggu': float(data['jam_per_minggu']),
        'Berat Akhir': 1,
        'Jmlh Tahun Pendidikan': 10,
        'Keuntungan Kapital': 0.0,
        'Kerugian Capital': 0.0
    }])

    input_df['Jenis Kelamin'] = input_df['Jenis Kelamin'].map({'Laki-laki': 1, 'Perempuan': 0})

    input_encoded = pd.get_dummies(input_df)

    for col in model_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0

    input_encoded = input_encoded[model_columns].fillna(0)

    pred_proba = model.predict_proba(input_encoded)[0][1]  # Probabilitas gaji > 7jt
    pred_label = model.predict(input_encoded)[0]
    kategori = '>7jt' if pred_label == 1 else '<=7jt'

    return kategori, pred_proba, input_df

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

def fetch_all_predictions():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data_pengguna ORDER BY umur DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows)

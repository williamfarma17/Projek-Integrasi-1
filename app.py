from logic import *
import streamlit as st

st.set_page_config(page_title="Prediksi Gaji", layout="centered")
st.title('📈 Prediksi Kategori Gaji Karyawan')
st.markdown("Masukkan data berikut untuk mengetahui apakah gaji karyawan termasuk kategori `<= 7 juta` atau `> 7 juta`.")

st.header("📝 Formulir Data Karyawan")

data = {
    'umur': st.number_input('Umur', min_value=18, max_value=70),
    'kelas_pekerja': st.text_input('Kelas Pekerja'),
    'pendidikan': st.selectbox('Pendidikan', ['SMA', 'D3','D4', 'Sarjana', 'Doktor', 'Master']),
    'status_perkawinan': st.selectbox('Status Perkawinan', ['Belum Pernah Menikah', 'Menikah', 'Cerai']),
    'pekerjaan': st.text_input('Pekerjaan'),
    'jenis_kelamin': st.radio('Jenis Kelamin', ['Laki-laki', 'Perempuan']),
    'jam_per_minggu': st.slider('Jam Kerja per Minggu', 20.0, 100.0, step=1.0)
}

if st.button("🔍 Prediksi Gaji"):
    try:
        hasil_gaji, _ = predict_salary(data)
        st.success(f"✅ Prediksi Gaji: **{hasil_gaji}**")
        save_to_database(data, hasil_gaji)
        st.info("🗃️ Data berhasil disimpan ke database.")
    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan: {e}")

st.markdown("---")
st.subheader("📋 Riwayat Data Karyawan")

if st.button("📄 Tampilkan Data Tersimpan"):
    df = fetch_all_predictions()
    if df.empty:
        st.warning("Belum ada data yang tersimpan.")
    else:
        st.dataframe(df)

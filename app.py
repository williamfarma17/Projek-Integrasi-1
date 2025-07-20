from logic import *
import streamlit as st

st.set_page_config(page_title="Prediksi Gaji Karyawan", layout="centered")
st.title('📊 Prediksi Kategori Gaji Karyawan')
st.markdown("Masukkan data karyawan berikut untuk memprediksi apakah gaji termasuk dalam kategori **`<= 7 juta`** atau **`> 7 juta`**, disertai dengan probabilitas prediksi.")

st.header("📝 Formulir Data Karyawan")

with st.form("form_prediksi"):
    col1, col2 = st.columns(2)
    with col1:
        umur = st.number_input('Umur', min_value=18, max_value=70, value=25)
        pendidikan = st.selectbox('Pendidikan', ['SMA', 'D3', 'D4', 'Sarjana', 'Master', 'Doktor'])
        status = st.selectbox('Status Perkawinan', ['Belum Pernah Menikah', 'Menikah', 'Cerai'])
    with col2:
        jenis_kelamin = st.radio('Jenis Kelamin', ['Laki-laki', 'Perempuan'])
        jam_kerja = st.slider('Jam Kerja per Minggu', 20, 100, step=1)
        kelas_pekerja = st.text_input('Kelas Pekerja')
        pekerjaan = st.text_input('Pekerjaan')

    submit = st.form_submit_button("🔍 Prediksi Sekarang")

if submit:
    try:
        data_input = {
            'umur': umur,
            'kelas_pekerja': kelas_pekerja,
            'pendidikan': pendidikan,
            'status_perkawinan': status,
            'pekerjaan': pekerjaan,
            'jenis_kelamin': jenis_kelamin,
            'jam_per_minggu': jam_kerja
        }

        hasil_kategori, prob, _ = predict_salary(data_input)

        st.success(f"✅ Prediksi Kategori Gaji: **{hasil_kategori}**")
        st.progress(int(prob * 100), text=f"Probabilitas: {prob:.2%}")
        st.caption("Semakin tinggi probabilitas, semakin yakin model dalam prediksinya.")

        save_to_database(data_input, hasil_kategori)
        st.info("🗃️ Data berhasil disimpan ke database.")
    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan: {e}")

st.markdown("---")
st.subheader("📋 Riwayat Data Prediksi")

if st.button("📄 Tampilkan Data Tersimpan"):
    df = fetch_all_predictions()
    if df.empty:
        st.warning("Belum ada data yang tersimpan.")
    else:
        st.dataframe(df, use_container_width=True)


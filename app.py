from logic import *
import streamlit as st

st.set_page_config(page_title="Prediksi Gaji Karyawan", layout="centered")

# Judul Aplikasi
st.markdown("<h1 style='text-align: center;'>📊 Prediksi Kategori Gaji Karyawan</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Masukkan data karyawan untuk memprediksi apakah gaji termasuk dalam kategori "
    "<strong style='color:#2ecc71;'>> 7 juta</strong> atau <strong style='color:#e74c3c;'>&le; 7 juta</strong>. "
    "</p>",
    unsafe_allow_html=True
)

st.header("📝 Formulir Data Karyawan")

# Form Input
with st.form("form_prediksi"):
    col1, col2 = st.columns(2)
    with col1:
        umur = st.number_input('🎂 Umur', min_value=18, max_value=70, value=25)
        pendidikan = st.selectbox('🎓 Pendidikan', ['SMA', 'D3', 'D4', 'Sarjana', 'Master', 'Doktor'])
        status = st.selectbox('💍 Status Perkawinan', ['Belum Pernah Menikah', 'Menikah', 'Cerai'])
    with col2:
        jenis_kelamin = st.radio('🧑‍🤝‍🧑 Jenis Kelamin', ['Laki-laki', 'Perempuan'])
        jam_kerja = st.slider('🕒 Jam Kerja per Minggu', 20, 100, step=1)
        kelas_pekerja = st.text_input('🏢 Kelas Pekerja')
        pekerjaan = st.text_input('💼 Pekerjaan')

    submit = st.form_submit_button("🔍 Prediksi Sekarang")

# Prediksi Gaji
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

        # Ringkasan input
        with st.expander("📌 Ringkasan Data yang Dimasukkan"):
            st.json(data_input)

        # Output hasil prediksi
        if hasil_kategori == ">7jt":
            st.success(f"🟢 Prediksi Kategori Gaji: **{hasil_kategori}**")
            st.markdown("*Karyawan diprediksi memiliki peluang besar untuk memperoleh gaji lebih dari Rp7.000.000.*")
        else:
            st.warning(f"🔴 Prediksi Kategori Gaji: **{hasil_kategori}**")
            st.markdown("*Karyawan diprediksi berada dalam kategori gaji Rp7.000.000 ke bawah.*")

        st.caption("Model yakin terhadap hasil ini berdasarkan pola data yang telah dipelajari.")

        # Simpan ke database
        save_to_database(data_input, hasil_kategori)
        st.info("🗃️ Data berhasil disimpan ke database.")

    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan: {e}")

# Riwayat Prediksi
# Riwayat Prediksi
st.markdown("---")
st.subheader("📋 Riwayat Data Prediksi")

if st.button("📄 Tampilkan Data Tersimpan"):
    df = fetch_all_predictions()
    if df.empty:
        st.warning("Belum ada data yang tersimpan.")
    else:
        # Tampilkan sebagai tabel
        st.dataframe(df, use_container_width=True)

        # Unduh sebagai CSV
        st.download_button(
            label="⬇️ Unduh Riwayat sebagai CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="riwayat_prediksi.csv",
            mime='text/csv'
        )

# Footer
st.markdown(
    "<hr style='border-top: 1px solid #bbb;'>"
    "<p style='text-align: center; font-size: 0.85em; color: gray;'>"
    "Aplikasi ini dibuat untuk tujuan pembelajaran Machine Learning & Streamlit."
    "</p>",
    unsafe_allow_html=True
)

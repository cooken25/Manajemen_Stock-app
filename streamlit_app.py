import streamlit as st
import pandas as pd

# Kelas Barang untuk menyimpan Objek barang
class Barang:
    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok

    # Fungsi untuk menambah stok barang
    def tambah_stok(self, jumlah):
        if jumlah >= 1:
            self.stok += jumlah
            return f"{jumlah} {self.nama} berhasil ditambahkan ke stok."
        else:
            return "Jumlah yang ditambahkan harus lebih besar dari 0."

    # Fungsi untuk mengurangi stok barang
    def kurangi_stok(self, jumlah):
        if jumlah > 0 and jumlah <= self.stok:
            self.stok -= jumlah
            return f"{jumlah} {self.nama} berhasil dikurangi dari stok."
        elif jumlah <= 0:
            return "Jumlah yang dikurangi harus lebih besar dari 0."
        else:
            return "Stok tidak cukup untuk transaksi ini."

    # Menampilkan informasi barang
    def __str__(self):
        return f"{self.nama} - Harga: {self.harga} - Stok: {self.stok}"

# Fungsi untuk menyimpan data ke Excel
def simpan_ke_excel():
    data = [{"Nama": barang.nama, "Harga": barang.harga, "Stok": barang.stok} for barang in st.session_state.barang_list]
    df = pd.DataFrame(data)
    df.to_excel("stok_barang.xlsx", index=False)

# Fungsi untuk membaca data dari Excel
def baca_dari_excel():
    try:
        df = pd.read_excel("stok_barang.xlsx")
        st.session_state.barang_list = [Barang(row["Nama"], row["Harga"], row["Stok"]) for _, row in df.iterrows()]
    except FileNotFoundError:
        st.session_state.barang_list = []

# Load data dari Excel saat aplikasi dijalankan
if "barang_list" not in st.session_state:
    baca_dari_excel()

# Fungsi untuk menambah barang
def tambah_barang():
    nama = st.text_input("Masukkan nama barang")
    harga = st.number_input("Masukkan harga barang", min_value=1)
    stok = st.number_input("Masukkan jumlah stok barang", min_value=1)

    if st.button("Tambah Barang"):
        if nama and harga > 0 and stok >= 0:
            barang_cek = False
            for barang in st.session_state.barang_list:
                if barang.nama == nama and barang.harga == harga:
                    barang.tambah_stok(stok)
                    barang_cek = True
                    st.success(f"Stok barang {nama} berhasil ditambahkan.")
                    break

            if not barang_cek:
                barang = Barang(nama, harga, stok)
                st.session_state.barang_list.append(barang)
                st.success(f"Barang {nama} berhasil ditambahkan.")

            simpan_ke_excel()  # Simpan perubahan ke Excel
            lihat_stok()
        else:
            st.error("Pastikan semua input valid!")

# Fungsi untuk mengurangi stok barang
def kurangi_stok():
    if st.session_state.barang_list:
        nama = st.text_input("Pilih nama barang yang akan dikurangi stoknya")
        jumlah = st.number_input("Masukkan jumlah yang akan dikurangi", min_value=1)

        if st.button("Kurangi Stok"):
            for barang in st.session_state.barang_list:
                if barang.nama == nama:
                    result = barang.kurangi_stok(jumlah)
                    st.success(result)
                    simpan_ke_excel()  # Simpan perubahan ke Excel
                    break
            else:
                st.error(f"Barang {nama} tidak ditemukan.")
    else:
        st.warning("Tidak ada barang di dalam stok.")

# Fungsi untuk melihat daftar barang
def lihat_stok():
    if len(st.session_state.barang_list) == 0:
        st.warning("Tidak ada barang di dalam stok.")
    else:
        st.write("Daftar Stok Barang:")
        for barang in st.session_state.barang_list:
            st.write(barang)

# Main
st.title("Aplikasi Manajemen Stok Barang :blue[CemilanKuFr98]")

menu = ["Tambah Barang", "Kurangi Stok Barang", "Lihat Daftar Stok"]
choice = st.sidebar.selectbox("Pilih Opsi", menu)

if choice == "Tambah Barang":
    tambah_barang()
elif choice == "Kurangi Stok Barang":
    kurangi_stok()
elif choice == "Lihat Daftar Stok":
    lihat_stok()

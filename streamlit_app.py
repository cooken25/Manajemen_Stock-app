import streamlit as st

import streamlit as st

# Kelas Barang untuk menyimpan informasi barang
class Barang:
    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok

    # Fungsi untuk menambah stok barang
    def tambah_stok(self, jumlah):
        if jumlah > 0:
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

# Menyimpan barang yang ada di stok
barang_list = []

# Fungsi untuk menambah barang
def tambah_barang():
    nama = st.text_input("Masukkan nama barang")
    harga = st.number_input("Masukkan harga barang", min_value=0.01)
    stok = st.number_input("Masukkan jumlah stok barang", min_value=0)

    if st.button("Tambah Barang"):
        if nama and harga > 0 and stok >= 0:
            barang = Barang(nama, harga, stok)
            barang_list.append(barang)
            st.success(f"Barang {nama} berhasil ditambahkan.")
        else:
            st.error("Pastikan semua input valid!")

# Fungsi untuk mengurangi stok barang
def kurangi_stok():
    nama = st.text_input("Masukkan nama barang yang akan dikurangi stoknya")
    jumlah = st.number_input("Masukkan jumlah yang akan dikurangi", min_value=1)

    if st.button("Kurangi Stok"):
        ditemukan = False
        for barang in barang_list:
            if barang.nama == nama:
                result = barang.kurangi_stok(jumlah)
                st.success(result)
                ditemukan = True
                break
        if not ditemukan:
            st.error(f"Barang {nama} tidak ditemukan.")

# Fungsi untuk menampilkan daftar barang
def lihat_stok():
    if not barang_list:
        st.warning("Tidak ada barang di dalam stok.")
    else:
        st.write("Daftar Stok Barang:")
        for barang in barang_list:
            st.write(barang)

# Layout aplikasi Streamlit
st.title("Aplikasi Manajemen Stok Barang")

menu = ["Tambah Barang", "Kurangi Stok Barang", "Lihat Daftar Stok"]
choice = st.sidebar.selectbox("Pilih Opsi", menu)

if choice == "Tambah Barang":
    tambah_barang()
elif choice == "Kurangi Stok Barang":
    kurangi_stok()
elif choice == "Lihat Daftar Stok":
    lihat_stok()

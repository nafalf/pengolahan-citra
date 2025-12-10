# 📷 Aplikasi Pengolahan Citra Digital (Algoritma Manual)

Aplikasi ini adalah implementasi teknik Pengolahan Citra Digital (Computer Vision) yang dibangun menggunakan **Python** dan **Streamlit**. 

**Poin Utama:** Aplikasi ini **tidak** menggunakan fungsi instan dari library (seperti `cv2.cvtColor` atau `cv2.GaussianBlur`) untuk memproses gambar. Sebaliknya, semua manipulasi piksel dilakukan secara **manual menggunakan looping (perulangan)** untuk mendemonstrasikan pemahaman mendalam tentang algoritma matematika di balik citra digital.

🔗 **Link Aplikasi:** https://pengolahan-citra-if-c.streamlit.app

---

## ✨ Fitur Utama

Aplikasi ini memiliki dua mode utama:

### 1. 🖼️ Mode Editor (Proses Citra)
Mode ini digunakan untuk mengunggah dan mengedit gambar.
* **11 Metode Pengolahan Manual:**
    1.  **Analisis Histogram:** Menampilkan grafik distribusi warna RGB & Grayscale.
    2.  **Grayscale:** Konversi warna ke abu-abu (Rata-rata).
    3.  **Citra Negatif:** Inversi warna (255 - pixel).
    4.  **Brightness:** Menambah/mengurangi kecerahan piksel.
    5.  **Contrast:** Mengalikan nilai piksel dengan faktor konstanta.
    6.  **Sepia:** Transformasi matriks warna untuk efek vintage.
    7.  **Blur (Manual Convolution):** Efek buram dengan kernel dinamis (bisa diatur user).
    8.  **Sharpening:** Penajaman citra menggunakan kernel Laplacian.
    9.  **Flip Horizontal:** Membalik urutan piksel per baris.
    10. **Flip Vertikal:** Membalik urutan total baris array.
    11. **Rotasi Bebas (360°):** Memutar gambar menggunakan rumus Trigonometri & Inverse Mapping.
* **Resize Otomatis:** Opsi untuk mengecilkan gambar agar pemrosesan manual berjalan lebih cepat.
* **Histogram Real-time:** Checkbox untuk melihat perubahan grafik warna setelah diedit.
* **Download Hasil:** Simpan gambar yang sudah diedit ke komputer.

### 2. 📷 Mode Kamera (Akuisisi Citra)
Mode ini digunakan untuk mengambil gambar dari Webcam secara *real-time*.
* Mengambil foto (Capture).
* Menyimpan foto ke perangkat lokal untuk kemudian diolah di Mode Editor.

---

## 🛠️ Teknologi yang Digunakan

* **Python 3.x**: Bahasa pemrograman utama.
* **Streamlit**: Framework untuk antarmuka web (UI).
* **NumPy**: Untuk manajemen array piksel (sebagai wadah data).
* **Pillow (PIL)**: Untuk membuka dan menyimpan format file gambar.
* **Matplotlib**: Untuk memvisualisasikan grafik histogram.
* **Math**: Untuk operasi trigonometri (Sin/Cos) pada fitur Rotasi.

---

## 🚀 Cara Menjalankan di Lokal (Localhost)

Jika Anda ingin menjalankan aplikasi ini di komputer sendiri:

1.  **Clone repository ini** (atau download zip):
    ```bash
    git clone [https://github.com/nafalf/pengolahan-citra.git]
    cd pengolahan-citra
    ```

2.  **Install Library yang dibutuhkan:**
    Pastikan Anda memiliki file `requirements.txt`. Jika belum, buat file tersebut dan isi dengan:
    ```text
    streamlit
    numpy
    Pillow
    matplotlib
    ```
    Lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Aplikasi:**
    ```bash
    streamlit run app.py
    ```

---

## 📝 Panduan Penggunaan

1.  **Buka Aplikasi:** Pilih mode di Sidebar sebelah kiri.
2.  **Upload Gambar:**
    * Jika punya file foto, pilih **Mode Editor** dan upload gambar.
    * Jika ingin pakai kamera, pilih **Mode Kamera**, ambil foto, download, lalu upload kembali di Mode Editor.
3.  **Resize (Opsional tapi Disarankan):**
    * Centang box *"Resize Gambar"* di sidebar. Ini akan mengubah lebar gambar menjadi 300px.
    * *Kenapa?* Karena algoritma manual memproses jutaan piksel satu per satu dengan `for-loop`, gambar resolusi tinggi (HD/4K) akan memakan waktu sangat lama (bisa menit) untuk diproses. Resize membuat proses menjadi instan (detik).
4.  **Pilih Algoritma:** Pilih metode manipulasi yang diinginkan dari *Dropdown Menu*.
5.  **Atur Parameter:** Gunakan *Slider* untuk mengatur intensitas (misal: tingkat kecerahan, sudut putar, atau level blur).
6.  **Analisis & Simpan:**
    * Centang "Tampilkan Histogram" untuk melihat grafik RGB.
    * Klik tombol "Download" untuk menyimpan hasil.

---

## ⚠️ Catatan Teknis (Untuk Laporan)

Aplikasi ini mungkin terasa lebih lambat dibandingkan aplikasi edit foto pada umumnya (seperti Photoshop atau OpenCV). Hal ini **disengaja** dan **normal** karena:

* **Pure Python Loops:** Setiap piksel (Pixel-by-pixel) diakses dan dimanipulasi menggunakan perulangan `for` bertingkat, bukan menggunakan operasi vektor C++ yang teroptimasi.
* **Kompleksitas Algoritma:** Fitur seperti *Blur* menggunakan algoritma Konvolusi dengan kompleksitas $O(N \cdot K^2)$, di mana setiap piksel harus dihitung ulang berdasarkan tetangga-tetangganya.

Tujuan utama aplikasi ini adalah **Edukasi** dan **Demonstrasi Logika**, bukan performa kecepatan.

---
**Mata Kuliah:** Pengolahan Citra

**Dibuat oleh:** 
1. Iqbal Alwy Qurrois (123220034)
2. Malik Afif (123220149)
3. Sofwan Fadhillah (123220170)
4. Muhammad Naufal Fauzi Ali (123220207)

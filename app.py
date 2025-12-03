import streamlit as st
from PIL import Image
import math
import numpy as np
import io

st.set_page_config(layout="wide", page_title="Aplikasi Pengolahan Citra Manual")

# ==========================================
# BAGIAN 1: ALGORITMA MANUAL (PURE PYTHON)
# ==========================================

def get_pixels_from_image(img):
    """Mengubah gambar menjadi Matriks 2D [Baris][Kolom][RGB]"""
    width, height = img.size
    pixels = list(img.getdata())
    matrix = []
    for y in range(height):
        start = y * width
        end = start + width
        row = []
        for p in pixels[start:end]:
            row.append(list(p))
        matrix.append(row)
    return matrix, width, height

def clamp(value):
    """Clipping nilai agar tetap 0-255"""
    return max(0, min(255, int(value)))

# --- LOGIKA KONVOLUSI (Dasar Blur & Sharpen) ---
def convolution(pixels, width, height, kernel, kernel_size, factor=1):
    new_pixels = []
    offset = kernel_size // 2
    
    # Loop Manual Pixel per Pixel
    for y in range(height):
        row = []
        for x in range(width):
            if x < offset or x >= width - offset or y < offset or y >= height - offset:
                row.append(pixels[y][x])
                continue
            
            r_acc, g_acc, b_acc = 0, 0, 0
            
            for ky in range(kernel_size):
                for kx in range(kernel_size):
                    px = pixels[y + ky - offset][x + kx - offset]
                    kval = kernel[ky][kx]
                    r_acc += px[0] * kval
                    g_acc += px[1] * kval
                    b_acc += px[2] * kval
            
            row.append([clamp(r_acc * factor), clamp(g_acc * factor), clamp(b_acc * factor)])
        new_pixels.append(row)
    return new_pixels

# --- METODE-METODE UTAMA ---

def algo_grayscale(pixels, width, height):
    new_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[y][x]
            avg = int((r + g + b) / 3)
            row.append([avg, avg, avg])
        new_pixels.append(row)
    return new_pixels

def algo_negative(pixels, width, height):
    new_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[y][x]
            row.append([255-r, 255-g, 255-b])
        new_pixels.append(row)
    return new_pixels

def algo_brightness(pixels, width, height, value):
    new_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[y][x]
            row.append([clamp(r+value), clamp(g+value), clamp(b+value)])
        new_pixels.append(row)
    return new_pixels

def algo_contrast(pixels, width, height, factor):
    new_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[y][x]
            row.append([clamp(r*factor), clamp(g*factor), clamp(b*factor)])
        new_pixels.append(row)
    return new_pixels

def algo_sepia(pixels, width, height):
    new_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[y][x]
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            row.append([clamp(tr), clamp(tg), clamp(tb)])
        new_pixels.append(row)
    return new_pixels

def algo_flip_horizontal(pixels, width, height):
    new_pixels = []
    for y in range(height):
        new_pixels.append(pixels[y][::-1])
    return new_pixels

def algo_flip_vertical(pixels, width, height):
    return pixels[::-1]

def algo_rotate_free(pixels, width, height, degree):
    theta = math.radians(degree)
    cos_val = math.cos(theta)
    sin_val = math.sin(theta)
    cx, cy = width // 2, height // 2
    
    new_pixels = [[[0,0,0] for _ in range(width)] for _ in range(height)]
        
    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            src_x = int(dx * cos_val + dy * sin_val + cx)
            src_y = int(-dx * sin_val + dy * cos_val + cy)
            
            if 0 <= src_x < width and 0 <= src_y < height:
                new_pixels[y][x] = pixels[src_y][src_x]
    return new_pixels

def algo_blur_dynamic(pixels, width, height, kernel_size):
    kernel = [[1 for _ in range(kernel_size)] for _ in range(kernel_size)]
    factor = 1 / (kernel_size * kernel_size)
    return convolution(pixels, width, height, kernel, kernel_size, factor)

def algo_sharpen(pixels, width, height):
    kernel = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
    return convolution(pixels, width, height, kernel, 3)

def manual_histogram_data(pixels, width, height):
    r_hist = [0]*256
    g_hist = [0]*256
    b_hist = [0]*256
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[y][x]
            r_hist[r] += 1
            g_hist[g] += 1
            b_hist[b] += 1
    return r_hist, g_hist, b_hist

def manual_grayscale_histogram_data(pixels, width, height):
    """Menghitung histogram grayscale manual (tanpa library)"""
    gray_hist = [0]*256
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[y][x]
            # Rumus Grayscale Rata-rata
            gray_val = int((r + g + b) / 3)
            gray_hist[gray_val] += 1
    return gray_hist

# ==========================================
# BAGIAN 2: UI STREAMLIT
# ==========================================

st.title("Aplikasi Pengolahan Citra Digital")
st.markdown("Implementasi Algoritma Manual (Looping) tanpa library instan OpenCV.")

# MODE SELECTION
mode = st.sidebar.radio("Pilih Mode:", ["📸 Mode Edit Foto", "🎥 Mode Live Kamera"])

# =========================================
# MODE 1: EDIT FOTO (Upload & Process)
# =========================================
if mode == "📸 Mode Edit Foto":
    
    st.sidebar.header("1. Upload Gambar")
    uploaded_file = st.sidebar.file_uploader("Upload JPG/PNG", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image_pil = Image.open(uploaded_file).convert('RGB')
        
        # --- FITUR RESIZE (Penting agar tidak macet) ---
        use_resize = st.sidebar.checkbox("Resize Gambar (Agar proses Blur lebih cepat)", value=True)
        if use_resize:
            base_width = 300
            w_percent = (base_width / float(image_pil.size[0]))
            h_size = int((float(image_pil.size[1]) * float(w_percent)))
            image_pil = image_pil.resize((base_width, h_size), Image.Resampling.LANCZOS)
        # -----------------------------------------------

        width, height = image_pil.size
        st.sidebar.caption(f"Resolusi Proses: {width}x{height} px")
        
        # Konversi ke Matrix (Heavy Process Preparation)
        pixels, w, h = get_pixels_from_image(image_pil)

        # MENU
        st.sidebar.header("2. Menu Metode")
        menu_options = [
            "1. Cek Histogram & Analisis", 
            "2. Grayscale",
            "3. Citra Negatif",
            "4. Brightness", 
            "5. Contrast", 
            "6. Sepia", 
            "7. Blur (Variable Intensity)", 
            "8. Sharpening", 
            "9. Flip Horizontal", 
            "10. Flip Vertikal", 
            "11. Rotasi Bebas (360°)"
        ]
        choice = st.sidebar.selectbox("Pilih Algoritma:", menu_options)

        # PARAMETER DINAMIS
        val = 0
        if "Brightness" in choice:
            val = st.sidebar.slider("Level Kecerahan", -100, 100, 50)
        elif "Contrast" in choice:
            val = st.sidebar.slider("Level Kontras", 0.0, 3.0, 1.5)
        elif "Rotasi" in choice:
            val = st.sidebar.slider("Sudut Putar", 0, 360, 45)
        elif "Blur" in choice:
            val = st.sidebar.slider("Intensitas Blur (Ukuran Kernel)", 3, 21, 5, step=2)
            st.sidebar.caption("Semakin besar angka, semakin lama prosesnya.")

        # LAYOUT 2 KOLOM
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original")
            st.image(image_pil, use_container_width=True)

        # PROSES
        res_pixels = pixels
        desc = ""

        with st.spinner('Sedang memproses algoritma pixel-by-pixel...'):
            if "Histogram" in choice:
                res_pixels = pixels 
                desc = "Mode Analisis Histogram."
            elif "Grayscale" in choice:
                res_pixels = algo_grayscale(pixels, w, h)
                desc = "Algoritma: Rata-rata (R+G+B)/3."
            elif "Negatif" in choice:
                res_pixels = algo_negative(pixels, w, h)
                desc = "Algoritma: 255 - Pixel."
            elif "Brightness" in choice:
                res_pixels = algo_brightness(pixels, w, h, val)
                desc = f"Algoritma: Penjumlahan Skalar (+{val})."
            elif "Contrast" in choice:
                res_pixels = algo_contrast(pixels, w, h, val)
                desc = f"Algoritma: Perkalian Skalar (x{val})."
            elif "Sepia" in choice:
                res_pixels = algo_sepia(pixels, w, h)
                desc = "Algoritma: Transformasi Matriks Warna."
            elif "Blur" in choice:
                res_pixels = algo_blur_dynamic(pixels, w, h, val)
                desc = f"Algoritma: Konvolusi Box Blur (Kernel {val}x{val})."
            elif "Sharpening" in choice:
                res_pixels = algo_sharpen(pixels, w, h)
                desc = "Algoritma: Konvolusi Laplacian Filter."
            elif "Flip Horizontal" in choice:
                res_pixels = algo_flip_horizontal(pixels, w, h)
                desc = "Algoritma: Reverse Array per Baris."
            elif "Flip Vertikal" in choice:
                res_pixels = algo_flip_vertical(pixels, w, h)
                desc = "Algoritma: Reverse urutan total Baris."
            elif "Rotasi" in choice:
                res_pixels = algo_rotate_free(pixels, w, h, val)
                desc = f"Algoritma: Trigonometri + Inverse Mapping ({val}°)."

        # TAMPILKAN HASIL
        with col2:
            st.subheader("Hasil Olahan")
            res_array = np.array(res_pixels, dtype=np.uint8)
            res_image_pil = Image.fromarray(res_array)
            st.image(res_image_pil, use_container_width=True)
            st.success(desc)

            # TOMBOL DOWNLOAD
            buf = io.BytesIO()
            res_image_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="💾 Download Gambar Hasil",
                data=byte_im,
                file_name="hasil_edit_manual.png",
                mime="image/png"
            )

            st.markdown("---")
            
            # --- HISTOGRAM CHECKLIST ---
            check_hist = False
            if "Histogram" in choice:
                check_hist = True
            else:
                check_hist = st.checkbox("Tampilkan Histogram Hasil (Analisis)")
            
            # --- GANTI BLOK 'if check_hist:' YANG LAMA DENGAN INI ---
            
            if check_hist:
                st.markdown("---")
                st.subheader("Data Histogram")
                
                # 1. Tampilkan RGB (Selalu tampil)
                st.write("**1. Grafik Histogram RGB:**")
                with st.spinner("Menghitung histogram RGB..."):
                    hr, hg, hb = manual_histogram_data(res_pixels, w, h)
                    
                    # Fix Rotasi (Abaikan 0)
                    if "Rotasi" in choice:
                        hr[0] = hg[0] = hb[0] = 0
                        st.caption("ℹ️ Info: Piksel background hitam (0) diabaikan.")
                    
                    st.bar_chart({"Red": hr, "Green": hg, "Blue": hb}, height=150)

                # 2. Tampilkan Grayscale (Hanya jika Menu 1 dipilih)
                if "Histogram" in choice:
                    st.write("**2. Grafik Histogram Grayscale (Derajat Keabuan):**")
                    with st.spinner("Menghitung histogram grayscale..."):
                        h_gray = manual_grayscale_histogram_data(res_pixels, w, h)
                        
                        # Fix Rotasi juga untuk Grayscale
                        if "Rotasi" in choice:
                            h_gray[0] = 0
                            
                        st.bar_chart({"Grayscale": h_gray}, height=150)
                        st.caption("Grafik ini menunjukkan distribusi intensitas cahaya (gelap-terang) dari gambar.")

    else:
        st.info("Silakan upload gambar di sidebar.")

# =========================================
# MODE 2: KAMERA (Capture Only)
# =========================================
elif mode == "🎥 Mode Live Kamera":
    st.header("Akuisisi Citra (Kamera)")
    st.write("Gunakan fitur ini untuk mengambil foto dari webcam, lalu simpan ke komputer untuk diedit di Mode Edit Foto.")
    
    picture = st.camera_input("Ambil Gambar")

    if picture:
        # Tampilkan hasil jepretan
        st.success("Gambar berhasil diambil!")
        img = Image.open(picture)
        
        # Tampilkan preview
        st.image(img, caption="Hasil Jepretan", width=400)
        
        # Instruksi
        st.markdown("### Langkah Selanjutnya:")
        st.write("1. Download gambar ini.")
        st.write("2. Pindah ke tab **'Mode Edit Foto'** di Sidebar.")
        st.write("3. Upload gambar yang baru didownload tadi.")
        
        # Tombol Download
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="⬇️ Download Gambar Kamera",
            data=buf.getvalue(),
            file_name="foto_kamera.png",
            mime="image/png"
        )
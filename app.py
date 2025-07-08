import streamlit as st
from PIL import Image, ImageEnhance
import io
import base64
import google.generativeai as genai
import traceback

# ✅ Ganti ini dengan API key milikmu dari https://makersuite.google.com/app/apikey
genai.configure(api_key="AIzaSyA2JEQ4LGTvDC_PMwPEID7E7URWlgvnyy8")  # <- GANTI di sini!

# Fungsi untuk generate caption dari gambar dan prompt menggunakan Gemini
def generate_ai_caption(image: Image.Image, user_prompt: str) -> str:
    try:
        prompt = f"""Buatkan caption marketing yang menarik untuk gambar produk ini.
Gaya caption: {user_prompt}.
Caption harus singkat, jelas, dan menggugah minat pembeli."""

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        response = model.generate_content(
            [prompt, image],  # Kirim objek PIL langsung
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 150,
            }
        )

        return response.text.strip()

    except Exception as e:
        st.error("❌ Gagal memanggil Gemini API.")
        st.text(traceback.format_exc())
        return "Gagal menghasilkan caption."

# --- Streamlit App ---
st.set_page_config(page_title="SellEase - AI Marketing untuk UMKM", layout="wide")

# Menampilkan logo dan judul
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("logo sellease crop.jpg", width=180)  # Pastikan file ada di folder yang sama
with col_title:
    st.title("SellEase - AI Marketing untuk UMKM")

# Upload Gambar
col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Gambar Produk")
    uploaded_file = st.file_uploader("Unggah gambar produk Anda", type=["jpg", "jpeg", "png", "webp"])

    image, enhanced = None, None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar Asli", use_column_width=True)

        # Enhance image (tajam + cerah)
        enhanced = ImageEnhance.Sharpness(image).enhance(2.0)
        enhanced = ImageEnhance.Brightness(enhanced).enhance(1.2)
        st.image(enhanced, caption="Gambar Setelah Ditingkatkan", use_column_width=True)

with col2:
    st.header("2. Caption & Hashtag AI")
    prompt = st.text_input("📝 Tulis gaya caption yang diinginkan (contoh: promosi, edukatif, lucu):")

    # Tombol generate caption di bawah input prompt
    if uploaded_file is not None:
        if st.button("✨ Generate Caption"):
            if prompt.strip() == "":
                st.warning("Masukkan prompt terlebih dahulu.")
            else:
                caption = generate_ai_caption(enhanced, prompt)
                st.text_area("🧠 Caption dari AI", caption, height=100)
    else:
        st.info("Silakan unggah gambar terlebih dahulu.")

# Section: Unduh Gambar
st.markdown("---")
st.header("📥 3. Unduh Gambar Hasil Edit")

if uploaded_file is not None and enhanced is not None:
    img_bytes = io.BytesIO()
    enhanced.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    b64 = base64.b64encode(img_bytes).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="gambar_enhanced.png">📥 Klik di sini untuk mengunduh gambar hasil edit</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    st.info("Upload dan proses gambar terlebih dahulu untuk dapat mengunduh.")

# --- Footer Section ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 14px; color: gray;'>"
    "SellEase adalah sebuah platform berbasis <em>AI (Artificial Intelligence)</em> "
    "yang dirancang untuk membantu <em>UMKM (Usaha Mikro, Kecil, dan Menengah)</em> "
    "dalam menjalankan strategi pemasaran digital secara otomatis dan efisien."
    "</div>",
    unsafe_allow_html=True
)

# --- Footer UI Tambahan ---
st.markdown(
    """
    <div style='text-align: center; padding-top: 10px; font-size: 13px; color: #aaa;'>
        <hr style='border: none; border-top: 1px solid #ccc; width: 60%; margin: 10px auto;' />
        <span>© 2025 SellEase | Dibuat dengan ❤️ untuk UMKM Indonesia</span><br>
        <span style='font-size: 12px;'>Created by Kelompok 2: Aninda Renadestya, Ashilla Tarawati, Farhan Arief Hudaya</span>
    </div>
    """,
    unsafe_allow_html=True
)

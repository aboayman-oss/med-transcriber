import streamlit as st
import google.generativeai as genai
import os
import tempfile

# 1. إعداد الصفحة
st.set_page_config(page_title="Medical Transcriber", page_icon="🩺")
st.title("🩺 Medical Lecture Transcriber")
st.caption("Powered by Gemini 1.5 Pro | Egy-English Hybrid")

# 2. مكان وضع مفتاح الـ API
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    # تهيئة Gemini
    genai.configure(api_key=api_key)

    # 3. رفع الملف
    uploaded_file = st.file_uploader("Upload Lecture (Audio)", type=["mp3", "wav", "m4a", "ogg"])

    if uploaded_file is not None:
        st.audio(uploaded_file)
        
        if st.button("Transcribe Now 🚀"):
            with st.spinner('Dr. Gemini is listening... Please wait...'):
                try:
                    # حفظ الملف مؤقتاً
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    # رفع الملف لـ Gemini
                    myfile = genai.upload_file(tmp_file_path)
                    
                    # اختيار الموديل
                    model = genai.GenerativeModel("gemini-1.5-pro")

                    # الأمر الطبي (البرومبت)
                    prompt = """
                    Act as a professional Medical Transcriptionist.
                    Transcribe the attached audio file verbatim (word-for-word).
                    
                    Rules:
                    1. Keep the mixed language (Egyptian Arabic + English).
                    2. Write Egyptian Arabic in Arabic script.
                    3. CRITICAL: Write ALL medical terms, diseases, and drugs in English with correct medical spelling.
                    4. Do not summarize. Do not translate medical terms to Arabic.
                    5. Format as a clean, readable script.
                    """

                    # التشغيل
                    response = model.generate_content([myfile, prompt])
                    
                    # عرض النتيجة
                    st.success("Done!")
                    st.markdown("### Transcript:")
                    st.text_area("Copy your text:", value=response.text, height=400)
                    
                    # تنظيف الملف المؤقت
                    os.unlink(tmp_file_path)

                except Exception as e:
                    st.error(f"Error: {e}")

else:
    st.warning("Please enter your API Key in the sidebar to start.")

import streamlit as st
import google.generativeai as genai
import os
import tempfile

# إعداد الصفحة
st.set_page_config(page_title="Medical Transcriber", page_icon="🩺")

st.title("🩺 Medical Lecture Transcriber")
st.caption("Egypt-English Hybrid Script | Gemini 1.5 Pro")

# --- التغيير هنا: وضعنا المفتاح في الوجه مباشرة ---
api_key = st.text_input("1. Paste your Gemini API Key here:", type="password")

# فاصل
st.markdown("---")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # رفع الملف
        uploaded_file = st.file_uploader("2. Upload Audio File", type=["mp3", "wav", "m4a", "ogg", "aac"])

        if uploaded_file is not None:
            # رسالة تأكيد أن الرفع تم
            st.success(f"File '{uploaded_file.name}' uploaded successfully! ({uploaded_file.size / 1024 / 1024:.2f} MB)")
            
            # تشغيل الصوت للتأكد
            st.audio(uploaded_file)
            
            # الزر يظهر فقط بعد الرفع
            if st.button("3. Transcribe Now (Click Once) 🚀"):
                
                # مؤشر التحميل
                progress_text = "Operation in progress. Please wait..."
                my_bar = st.progress(0, text=progress_text)

                try:
                    # 1. حفظ الملف مؤقتاً
                    with st.spinner('Preparing file...'):
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_file_path = tmp_file.name
                        my_bar.progress(20, text="File saved locally.")

                    # 2. رفع الملف لجوجل
                    with st.spinner('Sending to Dr. Gemini (This takes a few seconds)...'):
                        myfile = genai.upload_file(tmp_file_path)
                        my_bar.progress(50, text="File sent to AI.")

                    # 3. إعداد الموديل
                    model = genai.GenerativeModel("gemini-1.5-pro")
                    
                    prompt = """
                    Act as a professional Medical Transcriptionist.
                    Transcribe the attached audio file verbatim (word-for-word).
                    Rules:
                    1. Keep the mixed language (Egyptian Arabic + English).
                    2. Write Egyptian Arabic in Arabic script.
                    3. CRITICAL: Write ALL medical terms, diseases, and drugs in English with correct medical spelling.
                    4. No summarization. No translation of medical terms.
                    5. Format as a clean script.
                    """

                    # 4. التوليد
                    with st.spinner('Transcribing... This might take 1-2 minutes for long lectures...'):
                        response = model.generate_content([myfile, prompt])
                        my_bar.progress(100, text="Done!")

                    # 5. النتيجة
                    st.balloons()
                    st.markdown("### ✅ Transcript Ready:")
                    st.text_area("Copy Text:", value=response.text, height=600)

                    # تنظيف
                    os.unlink(tmp_file_path)

                except Exception as e:
                    st.error(f"Error occurred: {e}")
                    
    except Exception as e:
        st.error("Invalid API Key format.")

else:
    st.info("👈 Please enter your API Key above to start.")

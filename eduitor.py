import streamlit as st
import subprocess
import os
import math

# إعداد الصفحة
st.set_page_config(page_title="مقسم الفيديوهات الذكي", layout="wide")

st.title("🎥 بوت تقسيم الفيديوهات الطويلة")
st.markdown("---")

# رفع الملف
uploaded_file = st.file_uploader("ارفع فيديو (ساعتين أو أكثر)...", type=['mp4', 'mkv', 'mov', 'avi'])

if uploaded_file:
    # حفظ الملف مؤقتاً بصيغة ثنائية (Binary) لتوفير الذاكرة
    input_path = "input_video.mp4"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ تم رفع الفيديو بنجاح!")

    # خيارات التقسيم
    col1, col2 = st.columns(2)
    with col1:
        split_mins = st.number_input("طول كل جزء (بالدقائق):", min_value=1, value=30)
    
    # حساب عدد الأجزاء تقريبياً
    st.info(f"سيتم تقسيم الفيديو إلى أجزاء مدة كل منها {split_mins} دقيقة.")

    if st.button("🚀 ابدأ التقسيم الآن"):
        split_seconds = split_mins * 60
        
        # أمر FFmpeg للتقسيم السريع (Stream Copy)
        # هذا الأمر لا يستهلك الرام لأنه ينسخ البيانات ولا يعيد معالجتها
        output_pattern = "part_%03d.mp4"
        command = [
            "ffmpeg", "-i", input_path, 
            "-c", "copy", "-map", "0", 
            "-segment_time", str(split_seconds), 
            "-f", "segment", "-reset_timestamps", "1", 
            output_pattern
        ]

        with st.spinner("جاري التقسيم... يرجى الانتظار"):
            try:
                subprocess.run(command, check=True)
                
                # عرض الملفات الناتجة للتحميل
                st.markdown("### 📥 الأجزاء الجاهزة للتحميل:")
                files = [f for f in os.listdir('.') if f.startswith("part_") and f.endswith(".mp4")]
                files.sort()

                for file in files:
                    with open(file, "rb") as f:
                        st.download_button(label=f"تحميل {file}", data=f, file_name=file)
                
                st.balloons()
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")


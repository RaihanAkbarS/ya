import streamlit as st
from pytube import YouTube
import os
import re
from io import BytesIO

# Membuat directory untuk menyimpan video yang diunduh
directory = 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(page_title="YouTube Downloader", page_icon="🚀", layout="wide")

# Mengatur tema menjadi dark mode
def set_dark_mode():
    st.markdown(
        """
        <style>
        /* Teks */
        .css-1bxz6y {
            color: #f8f9fa !important;
        }
        /* Input teks */
        .st-eg input {
            color: #f8f9fa !important;
        }
        /* Input placeholder */
        .st-eg input::placeholder {
            color: #ced4da !important;
        }
        /* Input background */
        .st-eg input {
            background-color: #343a40 !important;
        }
        /* Selectbox */
        .st-ec select {
            color: #f8f9fa !important;
            background-color: #343a40 !important;
        }
        /* Spinner */
        .st-dk.st-el::before {
            border-color: #f8f9fa transparent transparent transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_dark_mode()

# Fungsi untuk mendapatkan informasi video
@st.cache_data
def get_info(url):
    yt = YouTube(url)
    streams = yt.streams.filter(type='video')
    details = {
        "image": yt.thumbnail_url,
        "streams": streams,
        "title": yt.title,
        "length": yt.length,
        "resolutions": [],
        "itag": [],
        "fps": [],
        "format": []
    }
    
    for i in streams:
        res = re.search(r'(\d+)p', str(i))
        typ = re.search(r'video/(\w+)', str(i))
        fps = re.search(r'(\d+)fps', str(i))
        tag = re.search(r'(\d+)', str(i))
        
        resolution = res.group() if res else "unknown"
        details["resolutions"].append(resolution)
        details["itag"].append(tag.group() if tag else "unknown")
        details["fps"].append(fps.group() if fps else "unknown")
        details["format"].append(typ.group() if typ else "unknown")
    
    return details

# Fungsi untuk mengunduh video dan mengonversinya menjadi byte
def download_video(url, itag):
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(itag)
    if stream:
        buffer = BytesIO()
        try:
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            return buffer
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    else:
        st.error("Error: Stream not found.")
        return None

# Judul aplikasi
st.title("YouTube Downloader 🚀")

# Menggunakan session state untuk menyimpan URL
if 'url' not in st.session_state:
    st.session_state.url = ""

# Input URL video
url = st.text_input("Tempel URL di sini 👇", placeholder='https://www.youtube.com/')

if st.button("Cek Link"):
    if url:
        with st.spinner("Mengambil informasi video..."):
            v_info = get_info(url)
        st.session_state.url = url  # Simpan URL saat ini
        col1, col2 = st.columns([1, 1.5], gap="small")
        with st.container():
            with col1:            
                st.image(v_info["image"])   
            with col2:
                st.subheader("Detail Video ⚙️")
                res_inp = st.selectbox('Pilih Resolusi', v_info["resolutions"])
                id = v_info["resolutions"].index(res_inp)            
                st.write(f"**Judul:** {v_info['title']}")
                st.write(f"**Durasi:** {v_info['length']} detik")
                st.write(f"**Resolusi:** {v_info['resolutions'][id]}")
                st.write(f"**Frame Rate:** {v_info['fps'][id]}")
                st.write(f"**Format:** {v_info['format'][id]}")
                file_name = st.text_input('Simpan dengan nama', placeholder=v_info['title'])
                if file_name:
                    if file_name != v_info['title']:
                        file_name += ".mp4"
                else:
                    file_name = v_info['title'] + ".mp4" 

                # Tombol unduh video
                video_bytes = download_video(url, v_info['itag'][id])
                if video_bytes:
                    st.download_button(
                        label="Unduh Video",
                        data=video_bytes,
                        file_name=file_name,
                        mime="video/mp4"
                    )
else:
    if st.session_state.url:  # Cek apakah URL sudah tersimpan di session state
        url = st.session_state.url
        with st.spinner("Mengambil informasi video..."):
            v_info = get_info(url)
        col1, col2 = st.columns([1, 1.5], gap="small")
        with st.container():
            with col1:            
                st.image(v_info["image"])   
            with col2:
                st.subheader("Detail Video ⚙️")
                res_inp = st.selectbox('Pilih Resolusi', v_info["resolutions"])
                id = v_info["resolutions"].index(res_inp)            
                st.write(f"**Judul:** {v_info['title']}")
                st.write(f"**Durasi:** {v_info['length']} detik")
                st.write(f"**Resolusi:** {v_info['resolutions'][id]}")
                st.write(f"**Frame Rate:** {v_info['fps'][id]}")
                st.write(f"**Format:** {v_info['format'][id]}")
                file_name = st.text_input('Simpan dengan nama', placeholder=v_info['title'])
                if file_name:
                    if file_name != v_info['title']:
                        file_name += ".mp4"
                else:
                    file_name = v_info['title'] + ".mp4" 

                # Tombol unduh video
                video_bytes = download_video(url, v_info['itag'][id])
                if video_bytes:
                    st.download_button(
                        label="Unduh Video",
                        data=video_bytes,
                        file_name=file_name,
                        mime="video/mp4"
                    )

import streamlit as st
from pytube import YouTube
import os
import re

# Membuat directory untuk menyimpan video yang diunduh
directory = 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(page_title="YouTube Downloader", page_icon="🚀", layout="wide")

# Mengatur background halaman menjadi hitam
st.markdown(f"""
    <style>
    .stApp {{
        background-color: black;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk mendapatkan informasi video
@st.cache_data
def get_info(url):
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, type='video')
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
        
        details["resolutions"].append(res.group() if res else "unknown")
        details["itag"].append(tag.group() if tag else "unknown")
        details["fps"].append(fps.group() if fps else "unknown")
        details["format"].append(typ.group() if typ else "unknown")
    
    return details

# Judul aplikasi
st.title("YouTube Downloader 🚀")

# Input URL video
url = st.text_input("Paste URL here 👇", placeholder='https://www.youtube.com/')
if url:
    v_info = get_info(url)
    col1, col2 = st.columns([1, 1.5], gap="small")
    with st.container():
        with col1:            
            st.image(v_info["image"])   
        with col2:
            st.subheader("Video Details ⚙️")
            res_inp = st.selectbox('__Select Resolution__', v_info["resolutions"])
            id = v_info["resolutions"].index(res_inp)            
            st.write(f"__Title:__ {v_info['title']}")
            st.write(f"__Length:__ {v_info['length']} sec")
            st.write(f"__Resolution:__ {v_info['resolutions'][id]}")
            st.write(f"__Frame Rate:__ {v_info['fps'][id]}")
            st.write(f"__Format:__ {v_info['format'][id]}")
            file_name = st.text_input('__Save as 🎯__', placeholder=v_info['title'])
            if file_name:
                if file_name != v_info['title']:
                    file_name += ".mp4"
            else:
                file_name = v_info['title'] + ".mp4" 
                
        button = st.button("Download ⚡️")
        if button:
            with st.spinner('Downloading...'):
                try:
                    ds = v_info["streams"].get_by_itag(v_info['itag'][id])
                    ds.download(filename=file_name, output_path=directory)
                    st.success('Download Complete', icon="✅")
                    st.balloons()
                except Exception as e:
                    st.error(f'Error: {str(e)}', icon="🚨")

import streamlit as st
from pytube import YouTube
import os
import base64

def clear_text():
    st.session_state["url"] = ""
    st.session_state["quality"] = ""

def download_file(stream):
    title = stream.title + '.mp4'  # Menambahkan ekstensi file
    stream.download(filename=title)
    
    with open(title, 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/mp4;base64,{b64}" download=\'{title}\'>\
            Unduh file\
        </a>'
        st.markdown(href, unsafe_allow_html=True)

    os.remove(title)

def can_access(url):
    access = False
    if len(url) > 0:
        try:
            tube = YouTube(url)
            if tube.check_availability() is None:
                access=True
        except:
            pass
    return access

st.set_page_config(page_title=" Youtube downloader", layout="wide")

with st.sidebar:
    st.title("YouTube Downloader")

    url = st.text_input("Masukkan URL di sini", key="url")

    if can_access(url):
        tube = YouTube(url)
        resolutions = set([stream.resolution for stream in tube.streams.filter(type="video")])
        resolution = st.selectbox("Pilih Resolusi", sorted(resolutions), key="resolution")

        stream = tube.streams.filter(type="video", resolution=resolution).first()

        if stream is not None:
            download = st.button("Unduh Video", key='download')
            if download:
                download_file(stream)

    st.button("Bersihkan", on_click=clear_text)

if can_access(url):
    st.video(url)

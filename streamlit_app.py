import streamlit as st
from pytube import YouTube
from io import BytesIO

def main():
    st.title("YouTube Video Downloader")

    # Input URL video dari pengguna
    video_url = st.text_input("Masukkan URL video YouTube:")

    if st.button("Download ⚡️"):
        with st.spinner('Downloading...'):
            try:
                yt = YouTube(video_url)
                stream = yt.streams.get_highest_resolution()
                video_bytes = BytesIO()
                stream.stream_to_buffer(video_bytes)
                video_bytes.seek(0)
                st.markdown(get_video_download_link(video_bytes, yt.title + ".mp4"), unsafe_allow_html=True)
                st.success('Download Selesai ✅')       
                st.balloons()
            except Exception as e:
                st.error(f'Error: {str(e)} 🚨')

def get_video_download_link(video_bytes, file_name):
    video_base64 = video_bytes.getvalue()
    download_link = f'<a href="data:video/mp4;base64,{video_base64}" download="{file_name}">Unduh Video</a>'
    return download_link

if __name__ == "__main__":
    main()

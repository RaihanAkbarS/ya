import streamlit as st
from pytube import YouTube
import os

# Fungsi untuk mendownload video
def download_video(url, resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
        if stream:
            video_path = os.path.join("downloads", "video.mp4")
            stream.download(output_path=video_path)
            thumbnail_url = yt.thumbnail_url
            return video_path, thumbnail_url
        else:
            st.error(f"Tidak ada stream yang tersedia dengan resolusi {resolution}.")
            return None, None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None

# Tampilan aplikasi menggunakan Streamlit
def main():
    st.title("YouTube Downloader")

    # Input URL video dari pengguna
    video_url = st.text_input("Masukkan URL video YouTube:")

    # Tombol untuk menampilkan thumbnail
    if video_url:
        yt = YouTube(video_url)
        thumbnail_url = yt.thumbnail_url
        st.image(thumbnail_url, caption="Thumbnail YouTube")

    # Pilihan resolusi video
    resolutions = ["144p", "240p", "360p", "480p", "720p", "1080p"]
    resolution = st.selectbox("Pilih resolusi video:", resolutions)

    # Tombol untuk memulai unduhan
    if st.button("Download"):
        if video_url:
            video_file, _ = download_video(video_url, resolution)
            if video_file:
                st.markdown(get_video_download_link(video_file), unsafe_allow_html=True)

# Fungsi untuk mendapatkan tautan unduhan video
def get_video_download_link(video_path):
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    video_base64 = base64.b64encode(video_bytes).decode()
    download_link = f'<a href="data:video/mp4;base64,{video_base64}" download="video.mp4">Download Video</a>'
    return download_link

if __name__ == "__main__":
    main()

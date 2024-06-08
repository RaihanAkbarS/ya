import streamlit as st
from pytube import YouTube
from io import BytesIO
from PIL import Image

# Fungsi untuk mendownload video
def download_video(url, resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_resolution(resolution)
        video_bytes = BytesIO()
        stream.download(video_bytes)
        thumbnail_url = yt.thumbnail_url
        return video_bytes, thumbnail_url
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None

# Tampilan aplikasi menggunakan Streamlit
def main():
    st.title("YouTube Downloader")

    # Input URL video dari pengguna
    video_url = st.text_input("Masukkan URL video YouTube:")

    # Pilihan resolusi video
    resolutions = ["144p", "240p", "360p", "480p", "720p", "1080p"]
    resolution = st.selectbox("Pilih resolusi video:", resolutions)

    # Tombol untuk memulai unduhan
    if st.button("Download"):
        if video_url:
            video_bytes, thumbnail_url = download_video(video_url, resolution)
            if video_bytes and thumbnail_url:
                st.download_button(
                    label="Download Video",
                    data=video_bytes.getvalue(),
                    file_name="video.mp4",
                    mime="video/mp4",
                )
                st.image(thumbnail_url, caption="Thumbnail YouTube")

if __name__ == "__main__":
    main()

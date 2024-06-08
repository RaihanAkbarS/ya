import streamlit as st
from pytube import YouTube
from io import BytesIO
from PIL import Image

# Fungsi untuk mendownload video
def download_video(url, resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
        if stream:
            video_bytes = BytesIO()
            stream.download(output_path=video_bytes)
            thumbnail_url = yt.thumbnail_url
            return video_bytes, thumbnail_url
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
            video_bytes, _ = download_video(video_url, resolution)
            if video_bytes:
                st.download_button(
                    label="Download Video",
                    data=video_bytes.getvalue(),
                    file_name="video.mp4",
                    mime="video/mp4",
                )

if __name__ == "__main__":
    main()

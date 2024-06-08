import streamlit as st
from pytube import YouTube
import os
import re
from io import BytesIO

directory = 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

st.set_page_config(page_title="YouTube Downloader", page_icon="🚀", layout="wide", )     
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1516557070061-c3d1653fa646?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

@st.cache(allow_output_mutation=True)
def get_info(url):
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, type='video')
    details = {}
    details["image"] = yt.thumbnail_url
    details["streams"] = streams
    details["title"] = yt.title
    details["length"] = yt.length
    itag, resolutions, vformat, frate = ([] for i in range(4))
    for i in streams:
        res = re.search(r'(\d+)p', str(i))
        typ = re.search(r'video/(\w+)', str(i))
        fps = re.search(r'(\d+)fps', str(i))
        tag = re.search(r'(\d+)',str(i))
        itag.append(str(i)[tag.start():tag.end()])
        resolutions.append(str(i)[res.start():res.end()])
        vformat.append(str(i)[typ.start():typ.end()])
        frate.append(str(i)[fps.start():fps.end()])
    details["resolutions"] = resolutions
    details["itag"] = itag
    details["fps"] = frate
    details["format"] = vformat
    return details

st.title("YouTube Downloader 🚀")
url = st.text_input("Tempel URL di sini 👇", placeholder='https://www.youtube.com/')
if url:
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
                
            button = st.button("Download ⚡️")
            if button:
                with st.spinner('Downloading...'):
                    try:
                        ds = v_info["streams"].get_by_itag(v_info['itag'][id])
                        video_bytes = BytesIO()
                        ds.stream_to_buffer(video_bytes)
                        video_bytes.seek(0)
                        st.download_button(
                            label="Unduh Video",
                            data=video_bytes,
                            file_name=file_name,
                            mime="video/mp4"
                        )
                        st.success('Download Selesai', icon="✅")       
                        st.balloons()
                    except:
                        st.error('Error: Simpan dengan nama yang berbeda!', icon="🚨")

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import os

st.set_page_config(page_title="YouTube Transcript Extractor", page_icon="🎙️")

st.title("🎙️ YouTube Video Transcript Extractor (Cookie Enabled)")
st.write("YouTube video ka link yahan dalein, cookies ki madad se transcript hasil karein!")

url = st.text_input("YouTube Video URL yahan enter karein:")

if st.button("Transcript Nikalein"):
    if url:
        try:
            with st.spinner("Transcript nikaal rahe hain..."):
                # Video ID nikalne ka tareeqa
                if "youtu.be" in url:
                    video_id = url.split("/")[-1].split("?")[0]
                elif "watch?v=" in url:
                    video_id = url.split("watch?v=")[1].split("&")[0]
                else:
                    video_id = url.split("/")[-1]

                cookie_file = "cookies.txt"
                
                # Naye tareeqay se transcript fetch karna (cookies ke sath ya baghair)
                if os.path.exists(cookie_file):
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies=cookie_file)
                else:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
                # Jo bhi pehli language mil jaye usay utha lein
                transcript = None
                for t in transcript_list:
                    transcript = t
                    break
                
                if transcript:
                    fetched_data = transcript.fetch()
                    full_text = ""
                    for entry in fetched_data:
                        full_text += entry['text'] + " "
                    
                    st.success("Transcript kamyabi se mil gaya hai!")
                    st.text_area("Result Text", full_text, height=350)
                    
                    st.download_button(
                        label="Download Transcript (.txt)",
                        data=full_text,
                        file_name=f"transcript_{video_id}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Is video ka transcript available nahi hai.")
                    
        except Exception as e:
            st.error(f"Error aa gaya hai: {e}. Baraye meharbani check karein ke cookies file theek tarike se uploaded hai.")
    else:
        st.warning("Pehle YouTube ka link darj karein!")

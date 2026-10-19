import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="YouTube Transcript Extractor", page_icon="🎙️")

st.title("🎙️ YouTube Video Transcript Extractor")
st.write("YouTube video ka link yahan dalein aur transcript hasil karein!")

url = st.text_input("YouTube Video URL yahan enter karein:")

if st.button("Transcript Nikalein"):
    if url:
        try:
            with st.spinner("Transcript nikaal rahe hain..."):
                # Video ID nikalne ka asaan tareeqa
                if "youtu.be" in url:
                    video_id = url.split("/")[-1].split("?")[0]
                elif "watch?v=" in url:
                    video_id = url.split("watch?v=")[1].split("&")[0]
                else:
                    video_id = url.split("/")[-1]

                # Safe transcript fetching using list_transcripts
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
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
            st.error(f"Error: {e}. Baraye meharbani koi doosri popular video ka link try karein.")
    else:
        st.warning("Pehle YouTube ka link darj karein!")

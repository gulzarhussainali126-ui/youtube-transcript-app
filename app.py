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
                # Video ID nikalne ka tareeqa
                if "youtu.be" in url:
                    video_id = url.split("/")[-1].split("?")[0]
                elif "watch?v=" in url:
                    video_id = url.split("watch?v=")[1].split("&")[0]
                else:
                    video_id = url.split("/")[-1]

                # Ab hum Hindi, Urdu aur English teeno languages allow kar rahe hain
                try:
                    fetched_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'ur', 'en'])
                except:
                    # Agar upar wali languages na milein, toh jo bhi auto-generated ho woh utha le
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    transcript = transcript_list.find_generated_transcript(['hi', 'en', 'ur'])
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
        except Exception as e:
            st.error(f"Koi error aa gaya hai: {e}. Baraye meharbani dosra link try karein.")
    else:
        st.warning("Pehle YouTube ka link darj karein!")

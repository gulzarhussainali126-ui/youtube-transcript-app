import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="YouTube Transcript Extractor", page_icon="🎙️")

st.title("🎙️ YouTube Video Transcript Extractor")
st.write("کسی بھی YouTube ویڈیو کا لنک یہاں درج کریں اور سیکنڈوں میں اس کا ٹرانسکرپٹ حاصل کریں!")

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            p = parse_qs(parsed_url.query)
            return p.get('v', [None])[0]
        elif parsed_url.path.startswith(('/embed/', '/v/')):
            return parsed_url.path.split('/')[2]
    return None

url = st.text_input("YouTube Video URL یہاں درج کریں:")

if st.button("Transcript نکالیں"):
    if url:
        video_id = extract_video_id(url)
        if video_id:
            try:
                with st.spinner("ٹرانسکرپٹ حاصل کیا جا رہا ہے..."):
                    # براہ راست حاصل کرنے کا بہترین طریقہ
                    fetched_data = YouTubeTranscriptApi.get_transcript(video_id)
                    
                    full_text = ""
                    for entry in fetched_data:
                        full_text += entry['text'] + " "
                    
                    st.success("ٹرانسکرپٹ کامیابی سے مل گیا ہے!")
                    st.subheader("Transcript Result:")
                    st.text_area("Result", full_text, height=350)
                    
                    st.download_button(
                        label="Transcript ڈاؤن لوڈ کریں (.txt)",
                        data=full_text,
                        file_name=f"transcript_{video_id}.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"اس ویڈیو کا ٹرانسکرپٹ دستیاب نہیں ہے یا اس پر سب ٹائٹلز آف ہیں۔ (وجہ: {e})")
        else:
            st.warning("براہ کرم ایک درست YouTube لنک درج کریں!")
    else:
        st.warning("پہلے لنک درج کریں!")

import streamlit as st
import asyncio
import edge_tts
import requests
import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

# Page Configuration for Cinematic Vibe
st.set_page_config(page_title="AI Documentary & Shorts Studio", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #0e1117; color: #ffffff;}
    .stButton>button {background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 8px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ AI Documentary & Shorts Creator Studio")
st.markdown("### Think School & Dhruv Rathee Style Automated Pipeline (100% Free - Indian Hinglish Engine)")

with st.sidebar:
    st.header("⚙️ Studio Settings")
    
    # Premium Indian Hinglish / Hindi Voices
    voice_option = st.selectbox(
        "Choose Indian AI Voice:",
        [
            "Madhur (Male - Deep Documentary Tone)", 
            "Swara (Female - Engaging & Clear)", 
            "Prabhat (Male - Professional Indian English)",
            "Neerja (Female - Warm Indian English)"
        ]
    )
    
    aspect_ratio = st.selectbox("Format:", ["9:16 (Shorts / Reels)", "16:9 (YouTube Long)"])
    st.info("☁️ Running fully on Cloud Workers. Zero PC load!")

# Voice Code Mapping Dictionary
voice_map = {
    "Madhur (Male - Deep Documentary Tone)": "hi-IN-MadhurNeural",
    "Swara (Female - Engaging & Clear)": "hi-IN-SwaraNeural",
    "Prabhat (Male - Professional Indian English)": "en-IN-PrabhatNeural",
    "Neerja (Female - Warm Indian English)": "en-IN-NeerjaNeural"
}

# Main Script Input
script_text = st.text_area(
    "📝 Paste Your Hinglish/Hindi Documentary Script Here:", 
    height=200, 
    placeholder="Example: '1991 mein jab India ki economy crash hone wali thi, tab ek aisa faisla liya gaya jisne desh ki taqdeer badal di...'"
)

async def generate_voice(text, output_file, voice_code):
    communicate = edge_tts.Communicate(text, voice_code)
    await communicate.save(output_file)

def fetch_visual(prompt, filename):
    # Using Pollinations.ai for high-end cinematic/real-style AI visuals for free
    encoded_prompt = requests.utils.quote(prompt + ", cinematic documentary lighting, 8k resolution, historical archive style, photorealistic")
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    return False

if st.button("🚀 Render Cinematic Video"):
    if not script_text.strip():
        st.warning("⚠️ Pehle script toh dalo boss!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Voiceover Generation with Indian Accent
            status_text.text("🔊 Synthesizing Studio-Quality Indian Hinglish Voiceover...")
            audio_path = "voiceover.mp3"
            selected_voice_code = voice_map[voice_option]
            asyncio.run(generate_voice(script_text, audio_path, selected_voice_code))
            progress_bar.progress(30)
            
            # Step 2: Visual Asset Generation
            status_text.text("🎨 Generating Cinematic Event Visuals...")
            image_path = "visual_scene.jpg"
            prompt_context = script_text[:120]  # First part of script for context
            fetch_visual(prompt_context, image_path)
            progress_bar.progress(70)
            
            # Step 3: Video Assembly
            status_text.text("🎞️ Compiling Final Video & Audio Sync...")
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            image_clip = ImageClip(image_path).set_duration(duration)
            video_clip = image_clip.set_audio(audio_clip)
            
            output_file = "final_output.mp4"
            video_clip.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
            progress_bar.progress(100)
            
            status_text.text("✅ Video Ready!")
            st.success("Boom! Tumhara Indian accent wala cinematic video cloud par render ho chuka hai.")
            
            # Display & Download
            st.video(output_file)
            with open(output_file, "rb") as file:
                st.download_button(
                    label="📥 Download Final Short/Video",
                    data=file,
                    file_name="ai_documentary_short.mp4",
                    mime="video/mp4"
                )
                
        except Exception as e:
            st.error(f"❌ Error aagya: {str(e)}")

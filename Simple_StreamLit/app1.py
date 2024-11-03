import streamlit as st
import sounddevice as sd
import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
from stqdm import stqdm
import time

@st.cache_resource
def load_asr_model():
    model = Wav2Vec2ForCTC.from_pretrained(r"\Model")
    processor = Wav2Vec2Processor.from_pretrained(r"\Processor")
    return model, processor

model, processor = load_asr_model()


def toggle_recording():
    if st.session_state.recording:
        st.session_state.recording = False
        sd.stop()
        st.session_state.audio_data = np.squeeze(st.session_state.myrecording)
        transcription = transcribe_audio_with_progress(st.session_state.audio_data, model, processor)
        st.write("Transcription from recorded audio:")
        st.write(transcription)
    else:
        st.session_state.recording = True
        st.session_state.myrecording = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype='float64')
        st.write("Recording... Click 'Stop Recording' to end.")


def transcribe_audio_with_progress(audio, model, processor):
    steps = 10
    for step in stqdm(range(steps), desc="Transcribing..."):
        time.sleep(0.5)
    
    input_values = processor(audio, return_tensors="pt", sampling_rate=16000).input_values
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    
    return transcription


if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None


st.title("Khmer ASR with Wav2Vec2")


btn_label = "Stop Recording" if st.session_state.recording else "Start Recording"
if st.button(btn_label):
    toggle_recording()

if st.session_state.audio_data is not None and not st.session_state.recording:
    st.audio(st.session_state.audio_data, format='audio/wav', sample_rate=16000)

uploaded_file = st.file_uploader("Upload a FLAC file", type=["flac"])
if uploaded_file is not None:
    audio_data, fs = librosa.load(uploaded_file, sr=16000)
    st.audio(uploaded_file, format="audio/flac")
    transcription = transcribe_audio_with_progress(audio_data, model, processor)
    st.write("Transcription from uploaded file:")
    st.write(transcription)

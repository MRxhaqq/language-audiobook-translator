# text_to_speech.py
"""Text-to-speech functions for the Language Audiobook Translator."""

import io
import base64
import streamlit as st
from gtts import gTTS


def text_to_speech(text, lang):
    """Convert text to speech and return audio data."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)

        # Save to BytesIO object
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")
        return None


def get_audio_download_link(audio_buffer, filename):
    """Generate download link for audio file."""
    audio_bytes = audio_buffer.getvalue()
    b64 = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Translated Audiobook</a>'
    return href
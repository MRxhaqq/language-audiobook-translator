# audio_processor.py
"""Audio processing functions for the Language Audiobook Translator."""

import io
import streamlit as st
from pydub import AudioSegment
from config import AUDIO_SETTINGS


def convert_audio_format(audio_file):
    """Convert audio file to WAV format for speech recognition with improved settings."""
    try:
        # First, try to use the file directly if it's already WAV
        if audio_file.name.lower().endswith('.wav'):
            return audio_file

        # Try using pydub with FFmpeg
        audio = AudioSegment.from_file(audio_file)

        # Improve audio for speech recognition
        # Normalize audio level
        audio = audio.normalize()

        # Ensure mono audio (speech recognition works better with mono)
        if audio.channels > 1:
            audio = audio.set_channels(AUDIO_SETTINGS["channels"])

        # Set sample rate to 16kHz (optimal for speech recognition)
        audio = audio.set_frame_rate(AUDIO_SETTINGS["sample_rate"])

        # Export to WAV with better settings
        wav_io = io.BytesIO()
        audio.export(
            wav_io,
            format="wav",
            parameters=["-ac", "1", "-ar", "16000"]  # Mono, 16kHz
        )
        wav_io.seek(0)

        return wav_io

    except FileNotFoundError as e:
        # FFmpeg not found - provide user-friendly error with solutions
        st.error("""
        🚨 **FFmpeg Not Found!**

        **Quick Fixes (choose one):**

        1️⃣ **Easiest - Use WAV files:**
           - Convert your audio to WAV format first
           - Use VLC Player: Media → Convert/Save
           - Or use online converter: convertio.co

        2️⃣ **Install FFmpeg:**
           ```
           # In Command Prompt as Administrator:
           winget install FFmpeg
           ```

        3️⃣ **Alternative install:**
           ```
           pip install imageio[ffmpeg]
           ```
        """)
        return None

    except Exception as e:
        # For other errors, try alternative approach
        st.warning(f"Audio conversion issue: {str(e)}")
        st.info("💡 **Try uploading a WAV file instead** - no conversion needed!")
        return None


def get_audio_info(wav_audio):
    """Get audio file information for display."""
    if wav_audio:
        try:
            if hasattr(wav_audio, 'seek'):
                wav_audio.seek(0)  # Reset position
                temp_audio = AudioSegment.from_wav(wav_audio)
                duration = len(temp_audio) / 1000.0  # Duration in seconds
                sample_rate = temp_audio.frame_rate
                return f"🎵 Audio Info: {duration:.1f} seconds, {sample_rate} Hz sample rate"
        except:
            pass
    return None
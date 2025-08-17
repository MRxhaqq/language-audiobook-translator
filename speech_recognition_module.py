# speech_recognition_module.py
"""Speech recognition functions for the Language Audiobook Translator."""

import speech_recognition as sr
import streamlit as st


@st.cache_resource
def init_components():
    recognizer = sr.Recognizer()
    # Don't cache the translator to avoid session issues
    return recognizer


def transcribe_audio(audio_data, source_lang):
    """Convert speech to text with improved settings."""
    recognizer = init_components()

    try:
        with sr.AudioFile(audio_data) as source:
            # Adjust for ambient noise with longer duration
            recognizer.adjust_for_ambient_noise(source, duration=1)
            # Record the entire audio file
            audio = recognizer.record(source, duration=None)  # Record everything

        # Try Google Speech Recognition with better settings
        try:
            text = recognizer.recognize_google(
                audio,
                language=source_lang,
                show_all=False  # Get best result only
            )
            return text
        except sr.UnknownValueError:
            # Try with different recognition settings
            try:
                # Try again with show_all=True to get alternatives
                results = recognizer.recognize_google(
                    audio,
                    language=source_lang,
                    show_all=True
                )
                if results and 'alternative' in results:
                    # Get the best alternative
                    best_result = results['alternative'][0]
                    if 'transcript' in best_result:
                        return best_result['transcript']
                return "Could not understand audio - try with clearer audio"
            except:
                return "Speech recognition failed - audio may be unclear"

    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        return f"Transcription error: {e}"
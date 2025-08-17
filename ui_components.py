# ui_components.py
"""UI components and layout functions for the Language Audiobook Translator."""

import streamlit as st
from config import LANGUAGES, SUPPORTED_AUDIO_FORMATS, AUDIO_SETTINGS


def render_header():
    """Render the main header and description."""
    st.title("🎧 Language Audiobook Translator")
    st.markdown("Convert audiobooks from one language to another using AI-powered speech recognition and translation.")


def render_input_section():
    """Render the input settings section and return user inputs."""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎤 Input Settings")

        # File upload
        uploaded_file = st.file_uploader(
            "Upload your audiobook file",
            type=SUPPORTED_AUDIO_FORMATS,
            help="Supported formats: " + ", ".join(f.upper() for f in SUPPORTED_AUDIO_FORMATS)
        )

        # Source language
        source_language = st.selectbox(
            "Source Language (Original audiobook language)",
            options=list(LANGUAGES.keys()),
            index=0
        )

    with col2:
        st.subheader("🎯 Output Settings")

        # Target language
        target_language = st.selectbox(
            "Target Language (Translate to)",
            options=list(LANGUAGES.keys()),
            index=1
        )

        # Processing options
        chunk_size = st.slider(
            "Audio chunk size (seconds)",
            min_value=AUDIO_SETTINGS["chunk_size_min"],
            max_value=AUDIO_SETTINGS["chunk_size_max"],
            value=AUDIO_SETTINGS["chunk_size_default"],
            help="Larger chunks may be more accurate but take longer to process"
        )

    return uploaded_file, source_language, target_language, chunk_size


def display_file_info(uploaded_file):
    """Display uploaded file information."""
    file_details = {
        "Filename": uploaded_file.name,
        "File size": f"{uploaded_file.size / (1024 * 1024):.2f} MB",
        "File type": uploaded_file.type
    }
    st.json(file_details)


def display_transcription_results(transcribed_text, audio_info=None):
    """Display transcription results with warnings for short transcriptions."""
    st.subheader("📝 Transcribed Text")

    # Show audio file info if available
    if audio_info:
        st.info(audio_info)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_area("Original text:", transcribed_text, height=100)
    with col2:
        st.metric("Characters", len(transcribed_text))

    # Check if transcription seems incomplete
    if len(transcribed_text) < 50:
        st.warning("⚠️ **Short transcription detected!** This might indicate:")
        st.write("- Audio quality issues")
        st.write("- Background noise")
        st.write("- Microphone too far from speaker")
        st.write("- Audio file corruption")

        if st.button("🔄 Try Again with Different Settings"):
            st.rerun()


def display_translation_results(translated_text):
    """Display translation results."""
    st.subheader("🔄 Translated Text")
    st.text_area("Translated text:", translated_text, height=100)


def display_final_results(audio_buffer, uploaded_file, transcribed_text, translated_text, source_language,
                          target_language):
    """Display final results with audio player and download link."""
    from text_to_speech import get_audio_download_link

    st.subheader("🎵 Results")

    # Play audio
    st.audio(audio_buffer.getvalue(), format='audio/mp3')

    # Download link
    download_filename = f"translated_{uploaded_file.name.split('.')[0]}.mp3"
    st.markdown(get_audio_download_link(audio_buffer, download_filename), unsafe_allow_html=True)

    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Original Length", f"{len(transcribed_text)} chars")
    with col2:
        st.metric("Translated Length", f"{len(translated_text)} chars")
    with col3:
        st.metric("Translation", f"{source_language} → {target_language}")


def render_sidebar():
    """Render the sidebar with information and tips."""
    with st.sidebar:
        st.header("ℹ️ How it works")
        st.markdown("""
        1. **Upload** your audiobook file
        2. **Select** source and target languages
        3. **Click** start translation
        4. **Download** the translated audiobook

        ---

        ### Supported Features:
        - 🎵 Multiple audio formats
        - 🌍 15+ languages
        - 🎧 High-quality speech synthesis
        - 📱 Mobile-friendly interface
        - 💾 Download translated files

        ---

        ### Tips for best results:
        - Use clear, high-quality audio
        - Avoid background noise
        - Choose appropriate chunk sizes
        - Ensure stable internet connection
        - Speak clearly and at normal pace
        - Use WAV format for best quality

        ### If transcription is incomplete:
        - Check audio file isn't corrupted
        - Try converting to WAV first
        - Reduce background noise
        - Ensure audio is loud enough
        """)

        st.header("🔧 Requirements")
        st.code("""
# Install required packages:
pip install streamlit
pip install SpeechRecognition
pip install googletrans==4.0.0rc1
pip install gTTS
pip install pydub

# For alternative translation (if needed):
pip install deep_translator
        """)


def render_footer():
    """Render the footer."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🎧 Language Audiobook Translator | Built with Streamlit</p>
            <p>Transform any audiobook into your preferred language!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
# app.py
"""Main application file for the Language Audiobook Translator."""

import streamlit as st
from config import PAGE_CONFIG, LANGUAGES
from ui_components import (
    render_header,
    render_input_section,
    display_file_info,
    display_transcription_results,
    display_translation_results,
    display_final_results,
    render_sidebar,
    render_footer
)
from audio_processor import convert_audio_format, get_audio_info
from speech_recognition_module import transcribe_audio
from translation_module import translate_text, translate_text_alternative
from text_to_speech import text_to_speech


def main():
    """Main application function."""
    # Configure the page
    st.set_page_config(**PAGE_CONFIG)

    # Render UI components
    render_header()

    # Get user inputs
    uploaded_file, source_language, target_language, chunk_size = render_input_section()

    # Processing section
    if uploaded_file is not None:
        st.subheader("📄 Processing")

        # Display file info
        display_file_info(uploaded_file)

        # Process button
        if st.button("🚀 Start Translation Process", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Step 1: Convert audio format
                status_text.text("Converting audio format...")
                progress_bar.progress(10)

                wav_audio = convert_audio_format(uploaded_file)
                if wav_audio is None:
                    st.error("Failed to convert audio format")
                    st.stop()

                # Step 2: Transcribe audio
                status_text.text("Converting speech to text...")
                progress_bar.progress(30)

                source_lang_code = LANGUAGES[source_language]
                transcribed_text = transcribe_audio(wav_audio, source_lang_code)

                if "error" in transcribed_text.lower() or "could not understand" in transcribed_text.lower():
                    st.error(f"Transcription failed: {transcribed_text}")
                    st.stop()

                # Display transcribed text with audio info
                audio_info = get_audio_info(wav_audio)
                display_transcription_results(transcribed_text, audio_info)

                # Step 3: Translate text
                status_text.text("Translating text...")
                progress_bar.progress(60)

                target_lang_code = LANGUAGES[target_language]
                translated_text = translate_text(transcribed_text, source_lang_code, target_lang_code)

                # If primary translation fails, try alternative method
                if "error" in translated_text.lower():
                    status_text.text("Trying alternative translation method...")
                    translated_text = translate_text_alternative(transcribed_text, source_lang_code, target_lang_code)

                if "error" in translated_text.lower() or "failed" in translated_text.lower():
                    st.error(f"Translation failed: {translated_text}")
                    st.info("💡 **Troubleshooting Tips:**")
                    st.write("- Check your internet connection")
                    st.write("- Try a shorter text sample")
                    st.write("- Install alternative translator: `pip install deep_translator`")
                    st.stop()

                # Display translated text
                display_translation_results(translated_text)

                # Step 4: Convert to speech
                status_text.text("Converting text to speech...")
                progress_bar.progress(80)

                audio_buffer = text_to_speech(translated_text, target_lang_code)
                if audio_buffer is None:
                    st.error("Failed to generate speech")
                    st.stop()

                # Step 5: Complete
                status_text.text("Translation complete!")
                progress_bar.progress(100)

                # Display results
                display_final_results(
                    audio_buffer,
                    uploaded_file,
                    transcribed_text,
                    translated_text,
                    source_language,
                    target_language
                )

            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")
                status_text.text("Processing failed")

    # Render sidebar and footer
    render_sidebar()
    render_footer()


if __name__ == "__main__":
    main()
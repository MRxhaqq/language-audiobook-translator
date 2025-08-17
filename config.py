# config.py
"""Configuration and constants for the Language Audiobook Translator."""

# Language options
LANGUAGES = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-cn',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Norwegian': 'no'
}

# Streamlit page configuration
PAGE_CONFIG = {
    "page_title": "Language Audiobook Translator",
    "page_icon": "🎧",
    "layout": "wide"
}

# Audio processing settings
AUDIO_SETTINGS = {
    "sample_rate": 16000,
    "channels": 1,
    "chunk_size_min": 10,
    "chunk_size_max": 60,
    "chunk_size_default": 30
}

# Supported file types
SUPPORTED_AUDIO_FORMATS = ['mp3', 'wav', 'ogg', 'flac', 'm4a']
# translation_module.py
"""Translation functions for the Language Audiobook Translator."""

from googletrans import Translator
import time


# Create translator instances as needed to avoid caching issues
def get_fresh_translator():
    """Get a fresh translator instance to avoid async issues."""
    return Translator()


def translate_text(text, source_lang, target_lang):
    """Translate text from source to target language."""
    try:
        # First try the alternative method (more reliable)
        return translate_text_alternative(text, source_lang, target_lang)
    except:
        # If alternative fails, try googletrans with proper handling
        try:
            time.sleep(0.5)  # Brief delay
            fresh_translator = get_fresh_translator()
            translation = fresh_translator.translate(text, src=source_lang, dest=target_lang)

            # Check if it's a coroutine (async object)
            if hasattr(translation, '__await__'):
                return "Error: Received async object - please install deep_translator"

            # Check if it has text attribute
            if hasattr(translation, 'text'):
                result = translation.text
                # Ensure it's not a coroutine string representation
                if 'coroutine' in str(result).lower():
                    return "Error: Translation returned coroutine object"
                return result
            else:
                return "Error: Translation object missing text attribute"

        except Exception as e:
            return f"Translation error: {str(e)}"


def translate_text_alternative(text, source_lang, target_lang):
    """Alternative translation using deep_translator - more reliable."""
    try:
        from deep_translator import GoogleTranslator

        # Handle language code differences
        lang_mapping = {
            'zh-cn': 'zh',
            'zh': 'zh-cn'
        }

        source_mapped = lang_mapping.get(source_lang, source_lang)
        target_mapped = lang_mapping.get(target_lang, target_lang)

        translator = GoogleTranslator(source=source_mapped, target=target_mapped)
        result = translator.translate(text)

        # Ensure we got a valid string result
        if result and isinstance(result, str) and 'coroutine' not in result.lower():
            return result
        else:
            return f"Alternative translation failed: Invalid result format"

    except ImportError:
        # Try a simple requests-based approach as final fallback
        try:
            import requests
            import urllib.parse

            # Simple Google Translate API call
            base_url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }

            response = requests.get(base_url, params=params, timeout=10)
            result = response.json()

            if result and len(result) > 0 and len(result[0]) > 0:
                return result[0][0][0]
            else:
                return "Translation failed: Invalid API response"

        except Exception as e:
            return f"All translation methods failed. Please install: pip install deep_translator"

    except Exception as e:
        return f"Alternative translation error: {str(e)}"
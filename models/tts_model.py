import os
from gtts import gTTS
from deep_translator import GoogleTranslator

def translate_to_hindi(text):
    """
    Translates English text to Hindi using deep-translator.

    Args:
        text (str): English text

    Returns:
        str: Hindi translated text
    """
    try:
        return GoogleTranslator(source='en', target='hi').translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def text_to_speech(text, filename="tts_output.mp3"):
    """
    Converts Hindi text to speech and saves as an MP3 file in the 'data/audio' folder.

    Args:
        text (str): Hindi text
        filename (str): Name of the MP3 file

    Returns:
        str: Full path to the saved MP3 file
    """
    try:
        audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "audio")
        os.makedirs(audio_dir, exist_ok=True)
        output_path = os.path.join(audio_dir, filename)

        tts = gTTS(text=text, lang='hi')
        tts.save(output_path)
        return output_path
    except Exception as e:
        print(f"TTS generation error: {e}")
        return None

# Example usage for testing
if __name__ == "__main__":
    summary = "Hello, How are you"
    translated = translate_to_hindi(summary)
    print("Translated:", translated)
    audio_file = text_to_speech(translated, filename="sample_summary.mp3")
    if audio_file:
        print("Audio saved at:", audio_file)

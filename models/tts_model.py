import os
from gtts import gTTS
from deep_translator import GoogleTranslator
import google.generativeai as genai

genai.configure(api_key="AIzaSyC8MHjTSPaiFuCE53xtHHZHsUnfBM2eXr4")
model = genai.GenerativeModel("gemini-1.5-flash")

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

def play_dashboard_summary(report_text):
    """
    Summarizes a full dashboard report using Gemini, translates it to Hindi,
    converts it to speech, and returns the English summary and audio file path.

    Args:
        report_text (str): Full text-based dashboard report

    Returns:
        tuple: (summary in English, audio path in Hindi)
    """
    try:
        prompt = f"You are an AI assistant. Summarize the following dashboard report into a concise paragraph:\n\n{report_text}"
        response = model.generate_content(prompt)
        summary = response.text.strip()

        hindi_summary = translate_to_hindi(summary)
        audio_path = text_to_speech(hindi_summary, filename="dashboard_summary.mp3")

        return summary, audio_path
    except Exception as e:
        print("Dashboard summary error:", e)
        return None, None

# Example usage for testing
if __name__ == "__main__":
    summary = "Hello, How are you"
    translated = translate_to_hindi(summary)
    print("Translated:", translated)
    audio_file = text_to_speech(translated, filename="sample_summary.mp3")
    if audio_file:
        print("Audio saved at:", audio_file)

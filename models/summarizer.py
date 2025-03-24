import json
import os
import re
import requests

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyC8MHjTSPaiFuCE53xtHHZHsUnfBM2eXr4"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

# Auto-locate data folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
INPUT_FILE = os.path.join(DATA_FOLDER, "articles_scraped.json")
OUTPUT_FILE = os.path.join(DATA_FOLDER, "articles_summary.json")

def include_first_skip_last(text):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    if len(sentences) < 2:
        return text
    return " ".join(sentences[:-1])  # keep everything except last

def truncate_to_sentence(text, max_chars=8000):
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    sentences = re.split(r'(?<=[.!?]) +', truncated)
    result = ""
    for sentence in sentences:
        if len(result) + len(sentence) <= max_chars:
            result += sentence + " "
        else:
            break
    return result.strip()

def summarize_with_gemini(text):
    if not text or text == "Content not available.":
        return "Summary not available."

    prompt = f"Summarize the following news article in 4-5 concise sentences:\n\n{text}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(
            GEMINI_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        result = response.json()
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            print(f"Unexpected response: {result}")
            return "Summary not available."
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Summary not available."

def process_articles():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"File not found at {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    updated = []
    for i, article in enumerate(articles):
        try:
            content = article.get("content", "").strip()
            trimmed = include_first_skip_last(content)
            input_text = truncate_to_sentence(trimmed, max_chars=8000)

            print(f"[{i+1}/{len(articles)}] Summarizing: {article.get('title', 'No Title')}")
            summary = summarize_with_gemini(input_text)

            article["summary"] = summary
            updated.append(article)

        except Exception as e:
            print(f"Error summarizing article {i+1}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=4, ensure_ascii=False)

    print(f"Summaries written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_articles()

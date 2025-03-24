import json
import os
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyA6Ws3pIRCPeC45N8ZFcTnIHXuhUnEF4OU"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def analyze_sentiment_gemini(text):
    if not text:
        return {"label": "Neutral", "score": 0.0}

    prompt = f"""
    Analyze the sentiment of the following news article.
    Respond strictly in this format:
    Label: [Positive/Neutral/Negative]
    Score: [a float from -1 to +1]

    Text:
    {text}
    """
    try:
        response = gemini_model.generate_content(prompt)
        if response.text:
            lines = response.text.strip().splitlines()
            label_line = next((l for l in lines if l.lower().startswith("label:")), "Label: Neutral")
            score_line = next((l for l in lines if l.lower().startswith("score:")), "Score: 0.0")
            label = label_line.split(":")[1].strip().capitalize()
            score = float(score_line.split(":")[1].strip())
            return {"label": label, "score": score}
    except Exception as e:
        print(f"❌ Gemini error: {e}")
    return {"label": "Neutral", "score": 0.0}

def process_articles():
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    file_path = os.path.join(data_folder, "articles_summary.json")

    with open(file_path, "r", encoding="utf-8") as file:
        articles = json.load(file)

    for article in articles:
        summary = article.get("summary", "")
        full_content = article.get("content", "")
        text = full_content if len(full_content) > 100 else summary
        result = analyze_sentiment_gemini(text)
        article["sentiment"] = result["label"]
        article["sentiment_score"] = result["score"]

    output_path = os.path.join(data_folder, "articles_with_sentiment.json")
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(articles, file, indent=4, ensure_ascii=False)

    print(f"✅ Sentiment analysis saved at: {output_path}")

if __name__ == "__main__":
    process_articles()

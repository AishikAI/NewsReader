from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import json

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.scraper import get_news_articles_with_content
from models.summarizer import process_articles as summarize_articles
from models.sentiment_model import process_articles as analyze_sentiment
from models.tts_model import translate_to_hindi, text_to_speech
from utils import analysis

app = FastAPI()

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FINAL_DATA_FILE = os.path.join(DATA_FOLDER, "articles_with_sentiment.json")

class CompanyRequest(BaseModel):
    company: str



@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}

@app.post("/pipeline")
def full_pipeline(req: CompanyRequest):
    try:
        get_news_articles_with_content(req.company)
        summarize_articles()
        analyze_sentiment()

        if not os.path.exists(FINAL_DATA_FILE):
            raise HTTPException(status_code=404, detail="No analysis result found")

        with open(FINAL_DATA_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)
        return {"company": req.company, "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech")
def tts_from_article_index(index: int):
    try:
        with open(FINAL_DATA_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)

        if index < 0 or index >= len(articles):
            raise HTTPException(status_code=404, detail="Article index out of range")

        summary = articles[index].get("summary", "")
        if not summary.strip():
            raise HTTPException(status_code=400, detail=f"Article {index} has no summary.")
        print("Summary:", summary)
        import asyncio
        hindi = asyncio.run(translate_to_hindi(summary))
        print("Hindi:", hindi)
        filename = f"article_{index}.mp3"
        path = text_to_speech(hindi, filename=filename)
        print("Audio Path:", path)

        audio_url = os.path.join("../data/audio", filename)

        if not path:
            raise HTTPException(status_code=500, detail="TTS generation failed")

        return {"index": index, "summary": summary, "translated": hindi, "audio_url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
def run_analysis(req: CompanyRequest):
    try:
        get_news_articles_with_content(req.company)
        summarize_articles()
        analyze_sentiment()
        result = analysis.run_analysis(req.company)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

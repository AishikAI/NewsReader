# Company News Summarization and Sentiment Analysis

A web-based tool that scrapes recent news articles about a company, summarizes them, performs sentiment analysis, generates a comparative report, and converts summaries into Hindi speech.

---

## Features

- Extracts news articles using NewsAPI
- Summarizes content via Gemini API
- Performs sentiment classification (Positive, Neutral, Negative)
- Analyzes and compares article sentiment, topics, and polarity
- Converts summaries into Hindi audio using Google Translate + gTTS
- Provides clean web interface via Streamlit
- Exposes backend via FastAPI with multiple endpoints

---

## Tech Stack

- **Language**: Python 3.10+
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **TTS**: gTTS + googletrans
- **Summarizer**: Gemini 1.5 Flash
- **Sentiment**: Gemini 1.5 Flash
- **Scraping**: NewsAPI + BeautifulSoup + LangChain Web Loader
- **Topics**: KeyBERT

---

## Workflow

1. User enters a company name.
2. App fetches top relevant news articles.
3. Summarizes each article using Gemini API.
4. Performs sentiment analysis on summaries.
5. Generates structured report with statistics and visualizations.
6. Converts the summary to Hindi speech and stores it as an MP3 file.

---

## Project Structure

```bash
news-summarization-app/
├── app/
│   ├── app.py               # Streamlit frontend
│   └── api.py               # FastAPI backend
├── models/
│   ├── summarizer.py        # Gemini summarizer
│   ├── sentiment_model.py   # Gemini sentiment model
│   └── tts_model.py         # Hindi translation + TTS
├── utils/
│   ├── scraper.py           # News fetcher + topic extraction
│   └── analysis.py          # Comparative metrics + visualizations
├── data/                    # Stores JSON and audio files
├── docs/                    # README + API + Model info
├── deployment/              # Dockerfile + HF config
├── requirements.txt         # Python dependencies

```

---

## API Endpoints

**Run these endpoints from the FastAPI server launched from project root.**

### `POST /pipeline`

Runs full pipeline: scrape, summarize, analyze sentiment.
**Request Body:**

```json
{
  "company": "Tesla"
}
```

**Response:**

```json
{
  "company": "Tesla",
  "articles": [
    { "title": "...", "summary": "...", "sentiment": "Positive" }
  ]
}
```

### `POST /text-to-speech`

Generate Hindi audio for a selected article.
**Request Body:**

```json
{
  "index": 0
}
```

**Response:**

```json
{
  "summary": "...",
  "translated": "...",
  "audio_url": "../data/audio/article_0.mp3"
}
```

### `POST /analyze`

Performs comparative sentiment analysis and returns metrics.
**Request Body:**

```json
{
  "company": "Tesla"
}
```

---

## Setup Instructions

**All commands must be run from the root directory: `news-summarization-app/`**

```bash
# Step 1: Clone the repository
$ git clone https://github.com/yourname/news-summarization-app.git
$ cd news-summarization-app

# Step 2: Create and activate virtual environment (recommended)
$ python -m venv venv
$ source venv/bin/activate   # On Windows: venv\Scripts\activate

# Step 3: Install all dependencies
$ pip install -r requirements.txt

# Step 4: Run the Streamlit app (Frontend)
$ streamlit run app/app.py

# Step 5: (Optional) Run the FastAPI server for API access
$ uvicorn app.api:app --reload

# Access FastAPI docs at:
# http://127.0.0.1:8000/docs
```

---

## Model Details

### Summarizer

- **Model**: Gemini 1.5 Flash
- **Accessed via**: Google Generative Language API (`generateContent` endpoint)
- Summarizes article text into 4-5 concise sentences using a templated prompt.

### Sentiment Analysis

- **Model**: Gemini 1.5 Flash
- Generates:
  - Sentiment Label: Positive, Negative, or Neutral
  - Sentiment Score: Floating value in the range [-1.0, 1.0]

### Text-to-Speech

- Uses `googletrans` for English to Hindi translation
- Uses `gTTS` for Hindi text-to-audio conversion
- Stores resulting `.mp3` in `data/audio/`

---

## Sample Output

```json
{
  "title": "Tesla hits Q3 sales record",
  "summary": "Tesla's latest EV sets record sales in Q3...",
  "sentiment": "Positive",
  "topics": ["EV", "Stock", "Innovation"]
}
```

---

## Credits

**Author**: Aishik Bhattacharjee  
**Email**: [aishikbhattacharjee98@gmail.com](mailto:aishikbhattacharjee98@gmail.com)  
**LinkedIn**: [linkedin.com/in/aishikcse](https://linkedin.com/in/aishikcse)

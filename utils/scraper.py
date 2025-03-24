import os
import json
from bs4 import BeautifulSoup
from keybert import KeyBERT
from newsapi import NewsApiClient
from langchain_community.document_loaders import WebBaseLoader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize models
kw_model = KeyBERT()
NEWS_API_KEY = "268527ddbbad4f28ab702ba22c877626"

def extract_full_article(url):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        html = docs[0].page_content if docs else "Content not available."
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return " ".join(text.split())
    except Exception as e:
        print(f"❌ Error fetching content from {url}: {e}")
        return "Content not available."

def extract_topics(text):
    if not text or text == "Content not available.":
        return []
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=5)
    return [kw[0] for kw in keywords]

def compute_similarity(company_name, text):
    try:
        vect = TfidfVectorizer().fit_transform([company_name, text])
        score = cosine_similarity(vect[0:1], vect[1:2])[0][0]
        return score
    except Exception:
        return 0.0

def get_news_articles_with_content(company_name, top_k=10, max_pages=5):
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    scored_articles = []
    page = 1

    while (page - 1) * 50 < 100 and page <= max_pages:
        response = newsapi.get_everything(
            q=company_name,
            language="en",
            sort_by="publishedAt",
            page_size=50,
            page=page
        )
        raw_articles = response.get("articles", [])
        if not raw_articles:
            break

        for article in raw_articles:
            url = article.get("url")
            title = article.get("title")
            description = article.get("description", "")
            if not url or not title:
                continue

            combined_text = f"{title} {description}"
            score = compute_similarity(company_name, combined_text)
            scored_articles.append((score, article))

        page += 1

    # Sort by similarity score and take top_k
    scored_articles = sorted(scored_articles, key=lambda x: x[0], reverse=True)[:top_k]
    final_articles = []

    for score, article in scored_articles:
        url = article.get("url")
        title = article.get("title")
        content = extract_full_article(url)
        if content == "Content not available.":
            continue
        topics = extract_topics(content)
        final_articles.append({
            "title": title,
            "url": url,
            "content": content,
            "topics": topics
        })

    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    os.makedirs(data_folder, exist_ok=True)
    file_path = os.path.join(data_folder, "articles_scraped.json")
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(final_articles, file, indent=4, ensure_ascii=False)

    print(f"✅ {len(final_articles)} articles saved at: {file_path}")
    return final_articles

if __name__ == "__main__":
    get_news_articles_with_content("Microsoft", top_k=10)

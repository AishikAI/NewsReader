import google.generativeai as genai

# Configure Gemini API directly
genai.configure(api_key="AIzaSyC8MHjTSPaiFuCE53xtHHZHsUnfBM2eXr4")
model = genai.GenerativeModel("gemini-1.5-flash")

def query_articles_with_gemini(articles, question):
    """
    Use Gemini to answer a question based on full article content.

    Args:
        articles (List[dict]): List of articles with full content
        question (str): User's query

    Returns:
        str: Gemini-generated answer
    """
    if not question.strip():
        return "Please enter a valid question."

    context = "\n\n".join([
        f"Title: {a['title']}\nContent: {a.get('content', a.get('summary', ''))}" for a in articles
    ])

    prompt = (
        f"You are an AI assistant. Based on the following news content, answer the question as clearly as possible.\n"
        f"News Articles:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini Query Error:", e)
        return "Failed to get an answer from Gemini. Please try again later."
    
def query_text_report_with_gemini(text_report, question):
    if not question.strip():
        return "Please enter a valid question."

    prompt = (
        f"You are an AI assistant. Based on the following analysis report, answer the user's question clearly.\n\n"
        f"Report:\n{text_report}\n\n"
        f"Question: {question}\nAnswer:"
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini Query Error:", e)
        return "Failed to get an answer from Gemini. Please try again later."


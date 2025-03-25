import streamlit as st
import os
import json
from utils import analysis
from utils.query import query_text_report_with_gemini
from models.tts_model import play_dashboard_summary

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..","data")
FINAL_DATA_FILE = os.path.join(DATA_FOLDER, "articles_with_sentiment.json")

st.set_page_config(page_title="Detailed Analysis Reporting", layout="wide")

st.title("\U0001F4CA Full News Analysis Dashboard")

if not os.path.exists(FINAL_DATA_FILE):
    st.warning("Please run article collection first from the main page.")
    st.stop()

with open(FINAL_DATA_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

company_name = articles[0].get("title", "Unknown") if articles else "Unknown"
result = analysis.run_analysis(company_name)

# Display Graphs
st.subheader("📊 Sentiment Distribution")
st.pyplot(analysis.plot_sentiment_distribution(result["sentiment_dist"]))

st.subheader("📊 Top Topics")
st.pyplot(analysis.plot_topic_frequency(result["topic_freq"]))

st.subheader("📊 Sentiment by Topic")
st.dataframe(analysis.plot_sentiment_by_topic(result["sentiment_topic"]))

# Display Full Text Summary Report
st.subheader("📝 Text-Based Report")
report = []
report.append("Sentiment Distribution:")
for sentiment, count in result["sentiment_dist"].items():
    report.append(f"- {sentiment}: {count}")

report.append("\nTop Topics:")
for topic, count in result["topic_freq"][:10]:
    report.append(f"- {topic}: {count}")

report.append("\nSentiment by Topic:")
for topic, sentiments in result["sentiment_topic"].items():
    formatted = ', '.join(f"{label}: {count}" for label, count in sentiments.items())
    report.append(f"- {topic}: {formatted}")

report.append("\nMost Polarizing Articles:")
for art in result["polarizing_articles"]:
    report.append(f"- {art['title']} ({art['sentiment']}, Score: {art['sentiment_score']})")

report.append("\nDetailed Article Summaries:")
for i, art in enumerate(articles, 1):
    report.append(f"\nArticle {i}")
    report.append(f"Title    : {art['title']}")
    report.append(f"URL      : {art['url']}")
    report.append(f"Summary  : {art.get('summary', 'N/A')}")
    report.append(f"Sentiment: {art.get('sentiment', 'N/A')} (Score: {art.get('sentiment_score', 'N/A')})")
    report.append(f"Topics   : {', '.join(art.get('topics', []))}")
    report.append("-" * 80)

full_report = "\n".join(report)
st.text_area("Combined Report", full_report, height=800)

# Display Summary and Audio (Lazy Loaded)
st.subheader("\U0001F50A Summary and Audio")
if st.button("Play Audio Summary"):
    with st.spinner("Generating audio summary..."):
        summary, audio_path = play_dashboard_summary(full_report)
        if audio_path:
            st.success("Summary generated and translated.")
            st.markdown(f"**Summary (English):** {summary}")
            st.audio(audio_path, format="audio/mp3")
        else:
            st.error("Audio generation failed. Please try again.")

# Add Gemini Query Box
st.subheader("Ask Questions About This Report")
user_query = st.text_input("Enter your question")
if user_query:
    with st.spinner("Thinking..."):
        answer = query_text_report_with_gemini(full_report, user_query)
    st.markdown(f"**Answer:** {answer}")

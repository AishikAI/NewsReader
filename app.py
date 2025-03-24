import streamlit as st
import pandas as pd
import os
import sys
import json
import asyncio
import time

from utils.scraper import get_news_articles_with_content
from models.summarizer import process_articles as summarize_articles
from models.sentiment_model import process_articles as analyze_sentiment
from models.tts_model import translate_to_hindi, text_to_speech
from utils import analysis
from utils.query import query_articles_with_gemini

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
AUDIO_FOLDER = os.path.join(DATA_FOLDER, "audio")
FINAL_DATA_FILE = os.path.join(DATA_FOLDER, "articles_with_sentiment.json")

st.set_page_config(page_title="Company News Insights", layout="wide")

st.markdown("""
    <style>
    .centered-input .stTextInput > div > div > input {
        border-radius: 2rem;
        width: 250px;
        height: 2.5rem;
        padding: 0.5rem;
        font-size: 1rem;
    }
    .centered-input {
        display: flex;
        justify-content: center;
        margin-top: 10vh;
    }
    .sidebar-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 250px;
        font-size: 0.8rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        background: #f0f0f0;
        z-index: 10;
    }
    </style>
""", unsafe_allow_html=True)

st.title("\U0001F4F0 Company News Analyzer")

st.markdown('<div class="centered-input">', unsafe_allow_html=True)
company_name = st.text_input("",placeholder="Enter company name to fetch news:")
st.markdown('</div>', unsafe_allow_html=True)

run_analysis = st.button("View Articles")

if run_analysis and company_name.strip():
    with st.spinner("Please wait while we process your request..."):
        get_news_articles_with_content(company_name)
        summarize_articles()
        analyze_sentiment()

    st.success("\u2705 News analysis complete!")

    if os.path.exists(FINAL_DATA_FILE):
        with open(FINAL_DATA_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)
        st.session_state["articles"] = articles
        st.session_state["analysis_option"] = "Show Articles"
elif "articles" in st.session_state:
    articles = st.session_state["articles"]
else:
    articles = []

if articles:
    st.sidebar.markdown("### Filter Options")
    all_topics = sorted(set(t for article in articles for t in article.get("topics", [])))
    selected_topic = st.sidebar.selectbox("Filter by Topic", ["All"] + all_topics)

    sentiment_options = ["All", "Positive", "Negative", "Neutral"]
    selected_sentiment = st.sidebar.selectbox("Filter by Sentiment", sentiment_options)

    st.sidebar.markdown("### See Analysis")
    selected_option = st.sidebar.selectbox(
        "Select Analysis View",
        ["Show Articles", "Sentiment Distribution", "Top Topics", "Sentiment by Topic", "Most Polarizing Articles", "All Analysis"],
        index=["Show Articles", "Sentiment Distribution", "Top Topics", "Sentiment by Topic", "Most Polarizing Articles", "All Analysis"].index(st.session_state.get("analysis_option", "Show Articles"))
    )

    if selected_option != st.session_state.get("analysis_option"):
        st.session_state["analysis_option"] = selected_option
        st.rerun()

    if st.session_state["analysis_option"] != "Show Articles":
        st.markdown("## \U0001F4CA Analysis")
        result = analysis.run_analysis(company_name)

        if st.session_state["analysis_option"] in ["Sentiment Distribution", "All Analysis"]:
            st.subheader("Sentiment Distribution")
            st.pyplot(analysis.plot_sentiment_distribution(result["sentiment_dist"]))

        if st.session_state["analysis_option"] in ["Top Topics", "All Analysis"]:
            st.subheader("Top Topics")
            st.pyplot(analysis.plot_topic_frequency(result["topic_freq"]))

        if st.session_state["analysis_option"] in ["Sentiment by Topic", "All Analysis"]:
            st.subheader("Sentiment by Topic")
            st.dataframe(analysis.plot_sentiment_by_topic(result["sentiment_topic"]))

        if st.session_state["analysis_option"] in ["Most Polarizing Articles", "All Analysis"]:
            st.subheader("Most Polarizing Articles")
            for art in result["polarizing_articles"]:
                st.markdown(f"**{art['title']}** — *Sentiment: {art['sentiment']}*")

    filtered_articles = articles
    if selected_topic != "All":
        filtered_articles = [a for a in filtered_articles if selected_topic in a.get("topics", [])]
    if selected_sentiment != "All":
        filtered_articles = [a for a in filtered_articles if a.get("sentiment", "Unknown").lower() == selected_sentiment.lower()]

    st.markdown("### Articles")
    for i, article in enumerate(filtered_articles):
        with st.expander(f"{i+1}. {article['title']}"):
            st.markdown(f"**Summary:** {article.get('summary', 'No summary available.')}")
            st.markdown(f"**Sentiment:** {article.get('sentiment', 'Unknown')}")
            st.markdown(f"**Topics:** {', '.join(article.get('topics', []))}")
            st.markdown(f"[\U0001F517 Read Full Article]({article['url']})", unsafe_allow_html=True)

            if st.button(f"Audio", key=f"tts_{i}"):
                with st.spinner("Generating audio..."):
                    translated = translate_to_hindi(article.get("summary", ""))
                    audio_path = text_to_speech(translated, filename=f"article_{i}.mp3")
                    if audio_path:
                        st.info("Click the play button below to hear the summary:")
                        st.audio(audio_path, format="audio/mp3")

    st.markdown("---")
    st.subheader("Write Your Query")
    user_query = st.text_input("Ask something based on the articles")
    if user_query:
        with st.spinner("Generating answer..."):
            response = query_articles_with_gemini(articles, user_query)
        st.markdown(f"**Answer:** {response}")
else:
    st.info("Enter a company name and click 'View Articles' to begin.")

st.sidebar.markdown("""
<div class="sidebar-footer">
<hr>
<small>
<strong>Created By:</strong> Aishik Bhattacharjee<br>
📧 <a href="mailto:aishikbhattacharjee98@gmail.com">aishikbhattacharjee98@gmail.com</a><br>
🔗 <a href="https://www.linkedin.com/in/aishikcse/" target="_blank">LinkedIn</a>
</small>
</div>
""", unsafe_allow_html=True)

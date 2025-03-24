import os
import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import pandas as pd


def load_articles():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "articles_with_sentiment.json")
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def sentiment_distribution(articles):
    return Counter(article.get("sentiment", "Unknown") for article in articles)


def topic_frequency(articles):
    topics = [topic for article in articles for topic in article.get("topics", [])]
    return Counter(topics).most_common()


def sentiment_by_topic(articles):
    topic_sentiment = defaultdict(lambda: Counter())
    for article in articles:
        sentiment = article.get("sentiment", "Unknown")
        for topic in article.get("topics", []):
            topic_sentiment[topic][sentiment] += 1
    return {topic: dict(sentiments) for topic, sentiments in topic_sentiment.items()}


def average_summary_length(articles):
    lengths = [len(article.get("summary", "")) for article in articles if article.get("summary")]
    return sum(lengths) / len(lengths) if lengths else 0


def most_polarizing_articles(articles, top_n=3):
    scored = [
        (article, abs(article.get("sentiment_score", 0)))
        for article in articles if "sentiment_score" in article
    ]
    sorted_by_polarity = sorted(scored, key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_by_polarity[:top_n]]


def company_mention_count(articles, company_name):
    name_lower = company_name.lower()
    return {
        article["title"]: article["content"].lower().count(name_lower)
        for article in articles if "content" in article
    }


def plot_sentiment_distribution(distribution):
    labels, values = zip(*distribution.items())
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['green', 'red', 'gray'])
    ax.set_title("Sentiment Distribution")
    return fig


def plot_topic_frequency(topic_freq, top_n=10):
    top_topics = topic_freq[:top_n]
    labels, values = zip(*top_topics)
    fig, ax = plt.subplots()
    ax.barh(labels, values)
    ax.invert_yaxis()
    ax.set_title("Top Topics by Frequency")
    return fig


def plot_sentiment_by_topic(sentiment_topic):
    df = pd.DataFrame(sentiment_topic).fillna(0).T
    return df


def run_analysis(company_name=""):
    articles = load_articles()
    analysis_results = {
        "sentiment_dist": sentiment_distribution(articles),
        "topic_freq": topic_frequency(articles),
        "sentiment_topic": sentiment_by_topic(articles),
        "avg_summary_length": average_summary_length(articles),
        "polarizing_articles": most_polarizing_articles(articles),
    }
    if company_name:
        analysis_results["company_mentions"] = company_mention_count(articles, company_name)

    return analysis_results


# Example usage
if __name__ == "__main__":
    results = run_analysis("Adani")
    print("Sentiment Distribution:", results["sentiment_dist"])
    print("Top Topics:", results["topic_freq"][:5])
    print("Average Summary Length:", results["avg_summary_length"])
    print("Most Polarizing Articles:")
    for art in results["polarizing_articles"]:
        print("-", art["title"])

    # Optional: show company mention counts
    if "company_mentions" in results:
        print("\nMentions of 'Adani':")
        for title, count in results["company_mentions"].items():
            print(f"{title}: {count}")

        # Display plots
    plot_sentiment_distribution(results["sentiment_dist"])
    plt.show()

    plot_topic_frequency(results["topic_freq"])
    plt.show()


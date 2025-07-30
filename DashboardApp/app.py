import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ----------------- Page Config -----------------
st.set_page_config(page_title="Tweet Analytics Dashboard", layout="wide")
st.title("Tweet Analytics Dashboard (Ghana)")



# ----------------- KPI Metrics -----------------
kpis = [
    {"title": "Total Tweets", "value": 538, "change": "+12.7%"},
    {"title": "Hashtag Usage", "value": 135, "change": "+8%"},
    {"title": "Engagements", "value": 266, "change": "+15%"},
    {"title": "Political Engagement Metrics", "value": 226, "change": "+5%"},
    {"title": "Reach & Impressions", "value": 324, "change": "+9%"},
    {"title": "Influencer Identification", "value": 34, "change": "+5%"},
]

with st.container():
    cols = st.columns(3)
    for i, kpi in enumerate(kpis):
        with cols[i % 3]:
            st.metric(label=kpi["title"], value=kpi["value"], delta=kpi["change"])


# ----------------- Sample Data From DB-----------------
themes = ['Mental Health', 'VAW', 'PwDs', 'LGBTQ']
sentiments = ['positive', 'neutral', 'negative']
np.random.seed(42)

# Bar chart data
bar_data = []
for theme in themes:
    pos = np.random.randint(100, 300)
    neu = np.random.randint(50, 150)
    neg = np.random.randint(80, 200)
    bar_data.extend([
        {"theme": theme, "sentiment": "positive", "count": pos},
        {"theme": theme, "sentiment": "neutral", "count": neu},
        {"theme": theme, "sentiment": "negative", "count": neg},
    ])
sentiment_counts = pd.DataFrame(bar_data)

# Line chart data
date_range = pd.date_range(start='2018-07-01', end='2020-07-30')
line_data = []

for date in date_range:
    for theme in themes:
        base = {
            "Mental Health": 0.65,
            "VAW": 0.4,
            "PwDs": 0.55,
            "LGBTQ": 0.5
        }[theme]
        score = np.clip(np.random.normal(loc=base, scale=0.1), 0, 1)
        sentiment = (
            "positive" if score > 0.6 else
            "neutral" if score >= 0.4 else
            "negative"
        )
        line_data.append({
            "date": date,
            "theme": theme,
            "score": round(score, 2),
            "sentiment": sentiment
        })
line_df = pd.DataFrame(line_data)

# ----------------- Visualizations -----------------
st.header("Sentiment Distribution by Theme")
fig1 = px.bar(
    sentiment_counts,
    x="theme",
    y="count",
    color="sentiment",
    barmode="group",
    labels={"theme": "Theme", "count": "Tweet Count", "sentiment": "Sentiment"},
    title="Sentiment Breakdown per Theme"
)
st.plotly_chart(fig1, use_container_width=True)

st.header("Sentiment Scores Over Time")
fig2 = px.line(
    line_df,
    x="date",
    y="score",
    color="theme",
    markers=True,
    labels={"score": "Sentiment Score", "theme": "Theme"},
    title="Daily Sentiment Trends by Theme"
)
st.plotly_chart(fig2, use_container_width=True)

# ----------------- Recent Tweets Table -----------------
st.header("Recent Sampled Tweets")
st.dataframe(
    line_df[['date', 'theme', 'sentiment', 'score']].sort_values('date', ascending=False).head(5),
    use_container_width=True
)

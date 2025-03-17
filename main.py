import streamlit as st
import praw
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time

# Reddit API credentials
CLIENT_ID = "your ID"
CLIENT_SECRET = "your Secret ID"
USER_AGENT = "appname/version by username"

# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

st.set_page_config(page_title="Real-Time Reddit Trends Dashboard", layout="wide")

st.title("Real-Time Reddit Trends Dashboard")

st.sidebar.header("Filters")
subreddit_name = st.sidebar.text_input("Enter Subreddit Name (e.g., Python)", "Python")


# Function to fetch trending posts
def fetch_trending_posts(subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        trending_posts = [(post.title, post.score, post.url) for post in subreddit.hot(limit=10)]
        return trending_posts
    except Exception as e:
        st.error(f"Error fetching posts: {e}")
        return []


# Function to generate a word cloud
def generate_wordcloud(titles):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(titles))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return plt

st.subheader("Live Trending Posts")
live_placeholder = st.empty()

# Simulate real-time updates
for i in range(10):  # Simulate 10 updates
    # Fetch trending posts
    trending_posts = fetch_trending_posts(subreddit_name)

    # Display live updates
    with live_placeholder.container():
        st.write(f"Update {i + 1}:")

        if trending_posts:
            # Convert to DataFrame
            df = pd.DataFrame(trending_posts, columns=["Post Title", "Upvotes", "URL"])

            # Display metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Upvotes", df["Upvotes"].sum())
            with col2:
                st.metric("Most Upvoted Post", df.loc[df["Upvotes"].idxmax()]["Post Title"])

            # Display the table
            st.write(df)

            # Display upvotes distribution chart
            st.subheader("Upvotes Distribution")
            fig, ax = plt.subplots()
            ax.bar(df["Post Title"], df["Upvotes"], color="skyblue")
            ax.set_xticklabels(df["Post Title"], rotation=45, ha="right")
            st.pyplot(fig)

            # Display word cloud
            st.subheader("Word Cloud of Post Titles")
            wordcloud_plot = generate_wordcloud(df["Post Title"])
            st.pyplot(wordcloud_plot)
        else:
            st.write("No trending posts found.")

        # Add a delay to simulate real-time updates
        time.sleep(60)  # Update every 60 seconds

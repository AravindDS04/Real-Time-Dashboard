import streamlit as st
import praw
import pandas as pd
import time

# Reddit API credentials
CLIENT_ID = "Your App ID"
CLIENT_SECRET = "Your SecretID"
USER_AGENT = "appname/version by userid"

# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Set up the Streamlit app
st.set_page_config(page_title="Real-Time Reddit Trends Dashboard", layout="wide")

# Title
st.title("Real-Time Reddit Trends Dashboard")

# Sidebar for filters
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


# Placeholder for live updates
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
            df = pd.DataFrame(trending_posts, columns=["Post Title", "Upvotes", "URL"])
            st.write(df)
        else:
            st.write("No trending posts found.")

        # Add a delay to simulate real-time updates
        time.sleep(60)  # Update every 60 seconds

# Footer
st.markdown("---")
st.markdown("Data Source: [Reddit API](https://www.reddit.com/dev/api/)")

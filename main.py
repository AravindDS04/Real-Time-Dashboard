import streamlit as st
import pandas as pd
import plotly.express as px
import time


st.set_page_config(page_title="Real -Time Dashboard", layout="wide")

# Title
st.title("Real-Time Dashboard")


# Load the dataset
@st.cache_data  # Cache the data to improve performance
def load_data():
    data = pd.read_csv("covid_19_clean_complete.csv", parse_dates=["Date"])
    return data


data = load_data()

# Sidebar for filters
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Select Country", data["Country/Region"].unique())

# Filter data by selected country
filtered_data = data[data["Country/Region"] == country]

# Display raw data
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(filtered_data)

# Placeholder for live updates
st.subheader("Live COVID-19 Updates")
live_placeholder = st.empty()

# Simulate real-time updates
for i in range(10):  # Simulate 10 updates
    new_data = filtered_data.sample(5)  # Randomly sample 5 rows for simulation

    # Display live updates
    with live_placeholder.container():
        st.write(f"Update {i + 1}:")
        st.write(new_data)

        # Plot live data
        fig = px.line(filtered_data, x="Date", y="Confirmed", title=f"Confirmed Cases in {country}")

        # Add a unique key to the plotly_chart element
        st.plotly_chart(fig, use_container_width=True, key=f"plotly_chart_{i}")

        # Add a delay to simulate real-time updates
        time.sleep(5)  # Update every 5 seconds

# Footer
st.markdown("---")
st.markdown("Data Source: [Kaggle COVID-19 Dataset](https://www.kaggle.com/datasets/imdevskp/corona-virus-report)")
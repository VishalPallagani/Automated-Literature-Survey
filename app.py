import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud

# Set the page configuration first
st.set_page_config(page_title="Survey", layout="wide")


# Function to load data
@st.cache_data
def load_data():
    return pd.read_csv("arxiv_papers.csv")


# Load data
df = load_data()

# Streamlit app layout
st.title("LLMs and Planning Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_year = st.sidebar.multiselect(
    "Year", options=df["Published Date"].apply(lambda x: x.split("-")[0]).unique()
)
selected_author = st.sidebar.multiselect(
    "Author", options=df["Authors"].str.split(", ").explode().unique()
)

# Filter data based on selection
if selected_year:
    df = df[df["Published Date"].apply(lambda x: x.split("-")[0]).isin(selected_year)]
if selected_author:
    df = df[df["Authors"].str.contains("|".join(selected_author))]

# Plot 1: Bar chart of the number of papers per year
df["Published Date"] = pd.to_datetime(df["Published Date"])
df["Year"] = df["Published Date"].dt.year
year_counts = df["Year"].value_counts().sort_index()
fig1 = px.bar(
    year_counts,
    x=year_counts.index,
    y=year_counts.values,
    labels={"x": "Year", "y": "Number of Papers"},
    title="Number of Papers per Year",
)
fig1.update_layout(barmode="group", xaxis_tickangle=-45)

# Plot 2: Wordcloud of paper titles
text = " ".join(df["Title"])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
fig2 = px.imshow(wordcloud.to_array(), title="Wordcloud of Paper Titles")
fig2.update_layout(
    xaxis={"visible": False}, yaxis={"visible": False}, margin=dict(l=0, r=0, t=30, b=0)
)

# Plot 3: Timeline of papers
df_sorted = df.sort_values("Published Date")
fig3 = px.scatter(
    df_sorted,
    x="Published Date",
    y="Title",
    hover_data=["Authors"],
    title="Timeline of Papers",
)
fig3.update_layout(margin=dict(l=0, r=0, t=30, b=0))

# Plot 4: Authors' contributions
authors_df = (
    df["Authors"].str.split(", ", expand=True).stack().reset_index(level=1, drop=True)
)
authors_counts = authors_df.value_counts().head(20)
fig4 = px.bar(
    authors_counts,
    x=authors_counts.values,
    y=authors_counts.index,
    orientation="h",
    labels={"x": "Number of Papers", "index": "Author"},
    title="Top 20 Authors",
)
fig4.update_layout(margin=dict(l=0, r=0, t=30, b=0))

# Display plots in a layout
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)

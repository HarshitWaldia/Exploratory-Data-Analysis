import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set page config for Streamlit
st.set_page_config(page_title="Amazon EDA Dashboard", layout="wide")

st.title("📊 Amazon Products EDA Dashboard")
st.write("Explore the insights of Amazon products with the dataset below.")

# -------------------------------
# Load the Dataset (locally stored)
# -------------------------------
dataset_path = 'amazon.csv'  # Path to the dataset within the project folder

# Check if the file exists in the folder
if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path)
else:
    st.error("Dataset file not found. Please make sure it's uploaded correctly.")
    st.stop()

# -------------------------------
# Data Cleaning Functions
# -------------------------------
def clean_price(x):
    try:
        return float(str(x).replace("₹", "").replace(",", "").strip())
    except:
        return None

def clean_percentage(x):
    try:
        return int(str(x).replace("%", "").strip())
    except:
        return None

def clean_rating(x):
    try:
        return float(str(x).strip())
    except:
        return None

def clean_rating_count(x):
    try:
        return int(str(x).replace(",", "").strip())
    except:
        return None

# Apply cleaning functions
if "discounted_price" in df.columns:
    df["discounted_price"] = df["discounted_price"].apply(clean_price)
if "actual_price" in df.columns:
    df["actual_price"] = df["actual_price"].apply(clean_price)
if "discount_percentage" in df.columns:
    df["discount_percentage"] = df["discount_percentage"].apply(clean_percentage)
if "rating" in df.columns:
    df["rating"] = df["rating"].apply(clean_rating)
if "rating_count" in df.columns:
    df["rating_count"] = df["rating_count"].apply(clean_rating_count)

st.success("✅ Dataset cleaned successfully!")
st.write("### Preview of Data")
st.dataframe(df.head())

# -------------------------------
# Split the 'category' column into 'top_category' and 'bottom_category'
# -------------------------------
df['top_category'] = df['category'].str.split('|').str[0]
df['bottom_category'] = df['category'].str.split('|').str[-1]

# -------------------------------
# Sidebar filter for selecting category level
# -------------------------------
st.sidebar.header("Filter Options")
filter_level = st.sidebar.selectbox("Select Category Level", ["High-Level", "Detailed"])

# High-level or Detailed category selection
if filter_level == "High-Level":
    top_category_filter = st.sidebar.multiselect("Select Top Categories", df["top_category"].dropna().unique())
    # Filter dataframe based on top category selection
    if top_category_filter:
        df = df[df["top_category"].isin(top_category_filter)]
elif filter_level == "Detailed":
    bottom_category_filter = st.sidebar.multiselect("Select Bottom Categories", df["bottom_category"].dropna().unique())
    # Filter dataframe based on bottom category selection
    if bottom_category_filter:
        df = df[df["bottom_category"].isin(bottom_category_filter)]

# Basic stats
# -------------------------------
st.subheader("📌 Basic Statistics")
st.write(df.describe())

# -------------------------------
# Product Categories Distribution (High-level vs Detailed)
# -------------------------------
if filter_level == "Detailed" and "bottom_category" in df.columns:
    st.subheader("📊 Product Categories Distribution (Detailed)")
    category_counts = df["bottom_category"].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(y=category_counts.index[:10], x=category_counts.values[:10], palette="viridis", ax=ax, ci=None)
    ax.set_title("Top 10 Detailed Categories by Product Count")
    st.pyplot(fig)

if filter_level == "High-Level" and "top_category" in df.columns:
    st.subheader("📊 Product Categories Distribution (High-Level)")
    top_category_counts = df["top_category"].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(y=top_category_counts.index[:10], x=top_category_counts.values[:10], palette="viridis", ax=ax, ci=None)
    ax.set_title("Top 10 High-Level Categories by Product Count")
    st.pyplot(fig)

# -------------------------------
# Scatter Plot: Actual vs Discounted Price
# -------------------------------
if "actual_price" in df.columns and "discounted_price" in df.columns:
    st.subheader("🔍 Scatter Plot: Actual Price vs Discounted Price")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x="actual_price", y="discounted_price", data=df, color="blue", alpha=0.6)
    plt.title("Scatter Plot: Actual Price vs Discounted Price")
    st.pyplot(fig)

# -------------------------------
# Box Plot: Rating Distribution
# -------------------------------
if "rating" in df.columns:
    st.subheader("📦 Box Plot: Rating Distribution by Category")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="top_category", y="rating", data=df, palette="coolwarm", ax=ax)
    ax.set_title("Box Plot: Rating Distribution by Category")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -------------------------------
# Histogram: Discount Percentage Distribution
# -------------------------------
if "discount_percentage" in df.columns:
    st.subheader("📊 Histogram: Discount Percentage Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["discount_percentage"].dropna(), kde=True, color="green", ax=ax)
    ax.set_title("Histogram: Discount Percentage Distribution")
    st.pyplot(fig)

# -------------------------------
# Violin Plot: Price Distribution by Category
# -------------------------------
if "actual_price" in df.columns and "top_category" in df.columns:
    st.subheader("🎻 Violin Plot: Actual Price Distribution by High-Level Category")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(x="top_category", y="actual_price", data=df, palette="muted", ax=ax)
    ax.set_title("Violin Plot: Price Distribution by High-Level Category")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -------------------------------
# Discounted Price vs Rating (Scatter plot)
# -------------------------------
if "discounted_price" in df.columns and "rating" in df.columns:
    st.subheader("💸 Discounted Price vs Rating (Scatter Plot)")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x="discounted_price", y="rating", data=df, color="red", alpha=0.6)
    plt.title("Discounted Price vs Rating")
    st.pyplot(fig)

# -------------------------------
# Average Prices and Ratings
# -------------------------------
if "actual_price" in df.columns and "discounted_price" in df.columns:
    st.subheader("💰 Average Actual vs Discounted Price (per category)")
    price_comparison = df.groupby("top_category")[["actual_price", "discounted_price"]].mean().sort_values("actual_price", ascending=False)
    st.dataframe(price_comparison.head(10))

    fig, ax = plt.subplots(figsize=(10, 5))
    price_comparison.head(10).plot(kind="bar", ax=ax)
    plt.title("Average Prices by Category")
    st.pyplot(fig)

if "rating" in df.columns:
    st.subheader("⭐ Average Rating by Category")
    avg_rating_top_category = df.groupby("top_category")["rating"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    avg_rating_top_category.head(10).plot(kind="bar", color="orange", ax=ax)
    plt.title("Top 10 Categories by Average Rating")
    st.pyplot(fig)

# -------------------------------
# Correlation Heatmap (for numerical columns)
# -------------------------------
st.subheader("📈 Correlation Heatmap")
numeric_cols = ["actual_price", "discounted_price", "discount_percentage", "rating", "rating_count"]
numeric_cols = [col for col in numeric_cols if col in df.columns]
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
plt.title("Correlation Heatmap")
st.pyplot(fig)

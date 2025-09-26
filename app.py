import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Amazon EDA Dashboard", layout="wide")

st.title("📊 Amazon Products EDA Dashboard")
st.write("Upload the dataset to explore Amazon product insights interactively.")

# -------------------------------
# Upload CSV
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # -------------------------------
    # Data Cleaning
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

    # Apply cleaning
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
    # Sidebar filters
    # -------------------------------
    st.sidebar.header("Filter Options")
    df['top_category'] = df['category'].str.split('|').str[0]
    df['bottom_category'] = df['category'].str.split('|').str[-1]
    if "top_category" in df.columns:
        category_filter = st.sidebar.multiselect("Select Categories", df["bottom_category"].dropna().unique())
        if category_filter:
            df = df[df["bottom_category"].isin(category_filter)]

    # -------------------------------
    # Basic stats
    # -------------------------------
    st.subheader("📌 Basic Statistics")
    st.write(df.describe())

    # -------------------------------
    # Distribution of categories
    # -------------------------------
    if "bottom_category" in df.columns:
        st.subheader("📊 Product Categories Distribution")
        category_counts = df["bottom_category"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(y=category_counts.index[:10], x=category_counts.values[:10], palette="viridis", ax=ax, ci=None)
        ax.set_title("Top 10 Categories by Product Count")
        st.pyplot(fig)

    # -------------------------------
    # Average Actual vs Discounted Price
    # -------------------------------
    if "actual_price" in df.columns and "discounted_price" in df.columns:
        st.subheader("💰 Average Actual Price vs Discounted Price (per category)")
        price_comparison = df.groupby("bottom_category")[["actual_price", "discounted_price"]].mean().sort_values("actual_price", ascending=False)

        st.dataframe(price_comparison.head(10))

        fig, ax = plt.subplots(figsize=(10, 5))
        price_comparison.head(10).plot(kind="bar", ax=ax)
        plt.title("Average Prices by Category")
        st.pyplot(fig)

    # -------------------------------
    # Average rating by category
    # -------------------------------
    if "rating" in df.columns:
        st.subheader("⭐ Average Rating by Category")
        avg_rating_category = df.groupby("bottom_category")["rating"].mean().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 5))
        avg_rating_category.head(10).plot(kind="bar", color="orange", ax=ax)
        plt.title("Top 10 Categories by Average Rating")
        st.pyplot(fig)

    # -------------------------------
    # Correlation heatmap
    # -------------------------------
    st.subheader("📈 Correlation Heatmap")
    numeric_cols = ["actual_price", "discounted_price", "discount_percentage", "rating", "rating_count"]
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    plt.title("Correlation Heatmap")
    st.pyplot(fig)

else:
    st.info("👆 Please upload a CSV file to start exploring.")

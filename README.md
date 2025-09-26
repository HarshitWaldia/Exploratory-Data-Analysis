# 📊 Amazon Product Reviews - Exploratory Data Analysis (EDA)

## 📌 Overview
This project performs **Exploratory Data Analysis (EDA)** on an Amazon product dataset.  
The dataset contains product details, prices, discounts, ratings, reviews, and user information.  

The goal of this analysis is to:
- Understand the structure and quality of the dataset.  
- Identify trends in pricing, discounting, and ratings.  
- Explore customer review patterns.  
- Detect potential issues like missing values, duplicates, or imbalances.  

---

## 🗂️ Dataset Description
The dataset includes the following key columns:

| Column | Description |
|--------|-------------|
| `product_id` | Unique identifier for each product |
| `product_name` | Name/description of the product |
| `category` | Product category (e.g., Electronics, Accessories) |
| `discounted_price` | Selling price after discount |
| `actual_price` | Original price before discount |
| `discount_percentage` | Percentage discount offered |
| `rating` | Customer rating (out of 5) |
| `rating_count` | Number of ratings |
| `about_product` | Short description/features |
| `user_id` | Unique ID of reviewer |
| `user_name` | Name of reviewer |
| `review_id` | Unique ID of review |
| `review_title` | Title of review |
| `review_content` | Full review text |
| `img_link` | Product image link |
| `product_link` | Product page link |

---

## 🔍 Steps in EDA
### 1. **Data Inspection**
- Used `.info()` to check data types, null values, and dataset size.  
- Found that most columns are complete, with very few missing values.  

### 2. **Descriptive Statistics**
- `.describe()` applied to both numeric and categorical columns.  
- Found **mean ≈ median** in prices → data is fairly symmetric.  
- Ratings cluster around **4.1**, showing positive bias.  

### 3. **Correlation Analysis**
- Computed correlation matrix for numeric features.  
- Observed strong negative correlation between `discount_percentage` and `discounted_price`.  
- Weak/no correlation between `rating` and price → ratings are not price-driven.  

### 4. **Visualizations**
- **Bar Chart**: Average rating per category.  
- **Boxplot**: Discount % distribution across categories.  
- **Scatterplot**: Discounted price vs rating.  
- **Word Cloud**: Most frequent terms in reviews.  
- **Heatmap**: Correlations between numeric features.  

### 5. **Data Quality Checks**
- Found duplicate product IDs (same product reviewed multiple times).  
- Prices and discounts stored as strings (`₹`, `%`) → cleaned and converted to numeric.  

---

## 📈 Insights
- Many products receive **4★ or higher** → customer reviews skew positive.  
- Discounts are widely offered (~50% most frequent).  
- Certain categories dominate the dataset (e.g., Electronics & Accessories).  
- Some reviews and users appear multiple times → dataset contains duplicate/overlapping entries.  

---

## 🛠️ Tools & Libraries
- **Python 3**  
- **Pandas** → data cleaning & manipulation  
- **NumPy** → numerical operations  
- **Matplotlib / Seaborn** → data visualization  
- **WordCloud** → review text analysis  

---

## 📌 How to Run
1. Clone the repository:  
   ```
   git clone https://github.com/your-username/amazon-eda.git
   cd amazon-eda
   ```
2. Install required libraries:
  ```
  pip install -r requirements.txt
  ```

3.Open the Jupyter Notebook:
  ```
  jupyter notebook Amazon_EDA.ipynb
  ```

4. Run the cells step by step to reproduce the analysis.

## 🚀 Future Work

-- **Build a recommendation system using ratings & categories.**

-- **Perform sentiment analysis on review text.**

-- **Use ML models to predict product ratings based on price & discount.**

## 👨‍💻 Author

**Harshit Waldia**

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    file_path = '/Users/hassanmulla/Downloads/NOVA_Phase2/Test/amazon.csv'
    df = pd.read_csv(file_path)
    df['discounted_price_num'] = pd.to_numeric(df['discounted_price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    df['actual_price_num'] = pd.to_numeric(df['actual_price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    df['discount_pct_num'] = pd.to_numeric(df['discount_percentage'].astype(str).str.replace('%', '', regex=True), errors='coerce')
    df['rating_count_num'] = pd.to_numeric(df['rating_count'].astype(str).str.replace(',', '', regex=True), errors='coerce')
    df['rating_num'] = pd.to_numeric(df['rating'], errors='coerce')
    df['revenue_proxy'] = df['discounted_price_num'] * df['rating_count_num']
    date_candidates = ['date', 'Date', 'timestamp', 'Timestamp', 'sales_date']
    for col in date_candidates:
        if col in df.columns:
            df['parsed_date'] = pd.to_datetime(df[col], errors='coerce')
            break
    else:
        df['parsed_date'] = pd.NaT
    if 'country' not in df.columns:
        df['country'] = 'Unknown'
    if 'latitude' not in df.columns:
        df['latitude'] = np.nan
    if 'longitude' not in df.columns:
        df['longitude'] = np.nan
    return df

df = load_data()

cats = st.sidebar.multiselect("Category", df['category'].dropna().unique(), default=df['category'].dropna().unique()[:5])
rat_min, rat_max = st.sidebar.slider("Rating", 0.0, 5.0, (0.0, 5.0), 0.1)
p_min = float(df['discounted_price_num'].min())
p_max = float(df['discounted_price_num'].max())
pri_min, pri_max = st.sidebar.slider("Discounted Price", p_min, p_max, (p_min, p_max))

data = df[
    (df['category'].isin(cats)) &
    (df['rating_num'] >= rat_min) &
    (df['rating_num'] <= rat_max) &
    (df['discounted_price_num'] >= pri_min) &
    (df['discounted_price_num'] <= pri_max)
]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Categories", data['category'].nunique())
k2.metric("Products", len(data))
k3.metric("Avg Price", f"{data['discounted_price_num'].mean():.2f}")
k4.metric("Avg Rating", f"{data['rating_num'].mean():.2f}")

c1, c2 = st.columns(2)
cat_counts = data['category'].value_counts().head(15).reset_index()
cat_counts.columns = ['category', 'count']
fig1 = px.bar(cat_counts, x='category', y='count', title="Products per Category (Top 15)")
c1.plotly_chart(fig1, use_container_width=True)

cat_price = data.groupby('category')['discounted_price_num'].mean().reset_index().sort_values('discounted_price_num', ascending=False).head(15)
fig2 = px.bar(cat_price, x='category', y='discounted_price_num', title="Average Price by Category (Top 15)")
c2.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
cat_discount = data.groupby('category')['discount_pct_num'].mean().reset_index().sort_values('discount_pct_num', ascending=False).head(15)
fig3 = px.bar(cat_discount, x='category', y='discount_pct_num', title="Average Discount % by Category (Top 15)")
c3.plotly_chart(fig3, use_container_width=True)

cat_rev = data.groupby('category')['revenue_proxy'].sum().reset_index().sort_values('revenue_proxy', ascending=False).head(15)
fig4 = px.bar(cat_rev, x='category', y='revenue_proxy', title="Revenue Proxy by Category (Top 15)")
c4.plotly_chart(fig4, use_container_width=True)

c5, c6 = st.columns(2)
cat_rating = data.groupby('category')['rating_num'].mean().reset_index().sort_values('rating_num', ascending=False).head(15)
fig5 = px.bar(cat_rating, x='category', y='rating_num', title="Average Rating by Category (Top 15)")
c5.plotly_chart(fig5, use_container_width=True)

fig6 = px.box(data, x='category', y='discounted_price_num', title="Price Distribution by Category")
c6.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.subheader("Category Summary")
summary = data.groupby('category').agg(
    products=('discounted_price_num', 'count'),
    avg_price=('discounted_price_num', 'mean'),
    avg_discount=('discount_pct_num', 'mean'),
    avg_rating=('rating_num', 'mean'),
    total_revenue=('revenue_proxy', 'sum')
).sort_values('total_revenue', ascending=False)
st.dataframe(summary, use_container_width=True)

st.markdown("---")
st.caption("Data Source: Amazon Dataset | Built with Streamlit")
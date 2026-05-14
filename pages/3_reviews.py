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

data = df[(df['category'].isin(cats)) & (df['rating_num'] >= rat_min) & (df['rating_num'] <= rat_max) & (df['discounted_price_num'] >= pri_min) & (df['discounted_price_num'] <= pri_max)]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Avg Rating", f"{data['rating_num'].mean():.2f}")
k2.metric("Total Reviews", f"{data['rating_count_num'].sum():,.0f}")
k3.metric("Products", f"{len(data):,}")
k4.metric("Avg Review Count", f"{data['rating_count_num'].mean():.0f}")

c1, c2 = st.columns(2)
avg_rat = data.groupby('category')['rating_num'].mean().reset_index().sort_values('rating_num', ascending=False).head(10)
fig1 = px.bar(avg_rat, x='category', y='rating_num', title="Average Rating by Category (Top 10)")
c1.plotly_chart(fig1, use_container_width=True)

rev_vol = data.groupby('category')['rating_count_num'].sum().reset_index().sort_values('rating_count_num', ascending=False).head(10)
fig2 = px.bar(rev_vol, x='category', y='rating_count_num', title="Review Volume by Category (Top 10)")
c2.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
fig3 = px.scatter(data, x='rating_num', y='rating_count_num', color='category', title="Rating vs Review Count", opacity=0.6, log_y=True)
c3.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter(data, x='discount_pct_num', y='rating_num', title="Discount % vs Rating", opacity=0.6)
c4.plotly_chart(fig4, use_container_width=True)

c5, c6 = st.columns(2)
fig5 = px.histogram(data, x='rating_num', nbins=10, title="Rating Distribution")
c5.plotly_chart(fig5, use_container_width=True)

fig6 = px.histogram(data, x='rating_count_num', nbins=20, title="Review Count Distribution", log_y=True)
c6.plotly_chart(fig6, use_container_width=True)
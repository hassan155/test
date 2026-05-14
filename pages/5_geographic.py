import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Geographic", layout="wide")

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

st.title("Geographic")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Products", len(data))
k2.metric("Avg Rating", round(data['rating_num'].mean(), 2) if not data.empty else 0.0)
k3.metric("Avg Price", round(data['discounted_price_num'].mean(), 2) if not data.empty else 0.0)
k4.metric("Revenue Proxy", round(data['revenue_proxy'].sum(), 2) if not data.empty else 0.0)

c1, c2 = st.columns(2)

map_data = data.dropna(subset=['latitude', 'longitude'])
if not map_data.empty:
    fig1 = px.scatter_geo(map_data, lat='latitude', lon='longitude', color='rating_num', size='discounted_price_num', projection='natural earth', title="Product Locations")
else:
    geo = data['country'].value_counts().head(10).reset_index()
    geo.columns = ['country', 'count']
    fig1 = px.bar(geo, x='country', y='count', title="Top Countries by Product Count")
c1.plotly_chart(fig1, use_container_width=True)

country_rev = data.groupby('country')['revenue_proxy'].sum().reset_index().sort_values('revenue_proxy', ascending=False).head(10)
fig2 = px.bar(country_rev, x='country', y='revenue_proxy', title="Revenue Proxy by Country (Top 10)")
c2.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)

country_count = data['country'].value_counts().head(10).reset_index()
country_count.columns = ['country', 'count']
fig3 = px.bar(country_count, x='country', y='count', title="Product Count by Country (Top 10)")
c3.plotly_chart(fig3, use_container_width=True)

country_avg = data.groupby('country')['rating_num'].mean().reset_index().sort_values('rating_num', ascending=False).head(10)
fig4 = px.bar(country_avg, x='country', y='rating_num', title="Average Rating by Country (Top 10)")
c4.plotly_chart(fig4, use_container_width=True)
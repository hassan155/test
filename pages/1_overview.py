import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    file_path = 'amazon.csv'
    df = pd.read_csv(file_path)
    df['discounted_price_num'] = pd.to_numeric(df['discounted_price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    df['actual_price_num'] = pd.to_numeric(df['actual_price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    df['discount_pct_num'] = pd.to_numeric(df['discount_percentage'].astype(str).str.replace('%', '', regex=True), errors='coerce')
    df['rating_count_num'] = pd.to_numeric(df['rating_count'].astype(str).str.replace(',', '', regex=True), errors='coerce')
    df['rating_num'] = pd.to_numeric(df['rating'], errors='coerce')
    df['revenue_proxy'] = df['discounted_price_num'] * df['rating_count_num']
    if 'parsed_date' not in df.columns:
        df['parsed_date'] = pd.NaT
    if 'country' not in df.columns:
        df['country'] = 'Unknown'
    if 'latitude' not in df.columns:
        df['latitude'] = np.nan
    if 'longitude' not in df.columns:
        df['longitude'] = np.nan
    return df

df = load_data()

cats = st.sidebar.multiselect('Category', df['category'].unique(), default=df['category'].unique()[:5])
rat_min, rat_max = st.sidebar.slider('Rating', 0.0, 5.0, (0.0, 5.0), 0.1)
p_min = float(df['discounted_price_num'].min())
p_max = float(df['discounted_price_num'].max())
pri_min, pri_max = st.sidebar.slider('Discounted Price', p_min, p_max, (p_min, p_max))

data = df[
    (df['category'].isin(cats)) &
    (df['rating_num'] >= rat_min) &
    (df['rating_num'] <= rat_max) &
    (df['discounted_price_num'] >= pri_min) &
    (df['discounted_price_num'] <= pri_max)
]

k1, k2, k3, k4 = st.columns(4)
k1.metric('Products', len(data))
k2.metric('Avg Rating', round(data['rating_num'].mean(), 2) if not data.empty else 0.0)
k3.metric('Avg Price', round(data['discounted_price_num'].mean(), 2) if not data.empty else 0.0)
k4.metric('Avg Revenue Proxy', round(data['revenue_proxy'].mean(), 2) if not data.empty else 0.0)

c1, c2 = st.columns(2)
top_cats = data['category'].value_counts().head(10).reset_index()
top_cats.columns = ['category', 'count']
fig1 = px.bar(top_cats, x='category', y='count', title='Top 10 Categories')
c1.plotly_chart(fig1, use_container_width=True)

cat_val = data.groupby('category')['discounted_price_num'].sum().reset_index().sort_values('discounted_price_num', ascending=False).head(10)
fig2 = px.bar(cat_val, x='category', y='discounted_price_num', title='Top 10 Categories by Value')
c2.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
fig3 = px.histogram(data, x='rating_num', nbins=10, title='Rating Distribution')
c3.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter(data, x='actual_price_num', y='discounted_price_num', color='rating_num', title='Actual vs Discounted Price', opacity=0.6)
c4.plotly_chart(fig4, use_container_width=True)

c5, c6 = st.columns(2)
nums = ['actual_price_num', 'discounted_price_num', 'discount_pct_num', 'rating_num', 'rating_count_num']
corr = data[nums].corr()
fig5 = px.imshow(corr, text_auto=True, aspect='auto', title='Correlation Matrix')
c5.plotly_chart(fig5, use_container_width=True)

if not data[['latitude', 'longitude']].dropna().empty:
    fig6 = px.scatter_geo(data.dropna(subset=['latitude', 'longitude']), lat='latitude', lon='longitude', color='rating_num', title='Geographic Distribution')
else:
    geo = data['country'].value_counts().head(10).reset_index()
    geo.columns = ['country', 'count']
    fig6 = px.bar(geo, x='country', y='count', title='Geographic Distribution (Top Countries)')
c6.plotly_chart(fig6, use_container_width=True)

st.markdown('---')
st.subheader('Data Preview')
st.dataframe(data)

st.sidebar.markdown('---')
st.sidebar.caption('Data Source: Amazon Dataset')
if st.sidebar.button('Refresh'):
    st.rerun()

st.markdown('---')
st.caption('Data Source: Amazon Dataset | Built with Streamlit')
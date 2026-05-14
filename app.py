import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Amazon Dashboard", layout="wide")

@st.cache_data
def load_data():
    file_path = '/Users/hassanmulla/Downloads/NOVA_Phase2/Test/amazon.csv'
    df = pd.read_csv(file_path)
    df['discounted_price_num'] = pd.to_numeric(df['discounted_price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    df['actual_price_num'] = pd.to_numeric(df['actual_price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    df['discount_pct_num'] = pd.to_numeric(df['discount_percentage'].astype(str).str.replace('%', '', regex=True), errors='coerce')
    df['rating_count_num'] = pd.to_numeric(df['rating_count'].astype(str).str.replace(',', '', regex=True), errors='coerce')
    df['rating_num'] = pd.to_numeric(df['rating'], errors='coerce')
    return df

df = load_data()

st.sidebar.header("Options")
cats = st.sidebar.multiselect("Category", df['category'].unique(), default=df['category'].unique()[:5])
rat_min, rat_max = st.sidebar.slider("Rating", 0.0, 5.0, (0.0, 5.0), 0.1)
p_min = float(df['discounted_price_num'].min())
p_max = float(df['discounted_price_num'].max())
pri_min, pri_max = st.sidebar.slider("Discounted Price", p_min, p_max, (p_min, p_max))

data = df[(df['category'].isin(cats)) & (df['rating_num'] >= rat_min) & (df['rating_num'] <= rat_max) & (df['discounted_price_num'] >= pri_min) & (df['discounted_price_num'] <= pri_max)]

st.title("Amazon Dataset Dashboard")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Products", len(data))
k2.metric("Avg Rating", round(data['rating_num'].mean(), 2))
k3.metric("Avg Discount %", round(data['discount_pct_num'].mean(), 2))
k4.metric("Categories", data['category'].nunique())

c1, c2 = st.columns(2)
top_cats = data['category'].value_counts().head(10).reset_index()
top_cats.columns = ['category', 'count']
fig1 = px.bar(top_cats, x='category', y='count', title="Top 10 Categories")
c1.plotly_chart(fig1, use_container_width=True)

cat_sum = data.groupby('category')['discounted_price_num'].sum().reset_index().sort_values('discounted_price_num', ascending=False).head(10)
fig2 = px.bar(cat_sum, x='category', y='discounted_price_num', title="Top 10 Categories by Value")
c2.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
fig3 = px.histogram(data, x='rating_num', nbins=10, title="Rating Distribution")
c3.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter(data, x='actual_price_num', y='discounted_price_num', color='rating_num', title="Actual vs Discounted Price", opacity=0.6)
c4.plotly_chart(fig4, use_container_width=True)

nums = ['actual_price_num', 'discounted_price_num', 'discount_pct_num', 'rating_num', 'rating_count_num']
corr = data[nums].corr()
fig5 = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(data)

st.sidebar.markdown("---")
st.sidebar.caption("Data Source: Amazon Dataset")
if st.sidebar.button("Refresh"):
    st.rerun()

st.markdown("---")
st.caption("Data Source: Amazon Dataset | Built with Streamlit")
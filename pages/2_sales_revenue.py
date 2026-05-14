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

mask = (df['category'].isin(cats)) & (df['rating_num'] >= rat_min) & (df['rating_num'] <= rat_max) & (df['discounted_price_num'] >= pri_min) & (df['discounted_price_num'] <= pri_max)
filtered = df[mask]

st.title("Sales & Revenue")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"${filtered['revenue_proxy'].sum():,.2f}")
k2.metric("Sales Volume", f"{len(filtered):,}")
k3.metric("Avg Rating", f"{filtered['rating_num'].mean():.2f}")
k4.metric("Avg Discount %", f"{filtered['discount_pct_num'].mean():.2f}")

c1, c2 = st.columns(2)

ts_df = filtered.dropna(subset=['parsed_date']).copy()
if not ts_df.empty:
    ts_df['period'] = ts_df['parsed_date'].dt.to_period('M').dt.to_timestamp()
    ts_group = ts_df.groupby('period')['revenue_proxy'].sum().reset_index()
    fig1 = px.line(ts_group, x='period', y='revenue_proxy', title="Revenue Over Time")
else:
    fig1 = px.line(title="Revenue Over Time (No Date Data)")
c1.plotly_chart(fig1, use_container_width=True)

cat_rev = filtered.groupby('category')['revenue_proxy'].sum().reset_index().sort_values('revenue_proxy', ascending=False).head(10)
fig2 = px.bar(cat_rev, x='category', y='revenue_proxy', title="Top Categories by Revenue")
c2.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)

geo_map_data = filtered.dropna(subset=['latitude', 'longitude'])
if not geo_map_data.empty:
    fig3 = px.scatter_geo(geo_map_data, lat='latitude', lon='longitude', color='rating_num', title="Geographic Distribution")
else:
    geo = filtered['country'].value_counts().head(10).reset_index()
    geo.columns = ['country', 'count']
    fig3 = px.bar(geo, x='country', y='count', title="Geographic Distribution (Top Countries)")
c3.plotly_chart(fig3, use_container_width=True)

fig4 = px.histogram(filtered, x='discount_pct_num', nbins=20, title="Discount Distribution")
c4.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("Data Preview")
st.dataframe(filtered)

st.sidebar.markdown("---")
st.sidebar.caption("Data Source: Amazon Dataset")
if st.sidebar.button("Refresh"):
    st.rerun()

st.markdown("---")
st.caption("Data Source: Amazon Dataset | Built with Streamlit")
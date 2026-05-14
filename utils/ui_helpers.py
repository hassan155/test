import streamlit as st
import plotly.express as px
import pandas as pd


def render_sidebar_filters(df):
    st.sidebar.header("Options")
    cats = st.sidebar.multiselect("Category", options=df['category'].unique(), default=list(df['category'].unique()[:5]))
    rat_min, rat_max = st.sidebar.slider("Rating", 0.0, 5.0, (0.0, 5.0), 0.1)
    p_min = float(df['discounted_price_num'].min())
    p_max = float(df['discounted_price_num'].max())
    pri_min, pri_max = st.sidebar.slider("Discounted Price", p_min, p_max, (p_min, p_max))
    return cats, rat_min, rat_max, pri_min, pri_max


def filter_data(df, cats, rat_min, rat_max, pri_min, pri_max):
    return df[
        df['category'].isin(cats) &
        (df['rating_num'] >= rat_min) &
        (df['rating_num'] <= rat_max) &
        (df['discounted_price_num'] >= pri_min) &
        (df['discounted_price_num'] <= pri_max)
    ].copy()


def render_metrics(data):
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Products", len(data))
    k2.metric("Avg Rating", round(data['rating_num'].mean(), 2) if len(data) > 0 else 0.0)
    k3.metric("Avg Discount %", round(data['discount_pct_num'].mean(), 2) if len(data) > 0 else 0.0)
    k4.metric("Categories", data['category'].nunique())
    k5.metric("Total Rev Proxy", f"{data['revenue_proxy'].sum():,.0f}" if len(data) > 0 and 'revenue_proxy' in data.columns else "0")
    k6.metric("Sales Volume Proxy", f"{data['rating_count_num'].sum():,.0f}" if len(data) > 0 and 'rating_count_num' in data.columns else "0")


def render_top_categories(data):
    top_cats = data['category'].value_counts().head(10).reset_index()
    top_cats.columns = ['category', 'count']
    fig = px.bar(top_cats, x='category', y='count', title="Top 10 Categories")
    return fig


def render_revenue_chart(data):
    if 'parsed_date' in data.columns and pd.api.types.is_datetime64_any_dtype(data['parsed_date']) and data['parsed_date'].notna().any():
        ts = data.groupby(data['parsed_date'].dt.to_period('M').astype(str))['revenue_proxy'].sum().reset_index()
        ts.columns = ['month', 'revenue']
        fig = px.line(ts, x='month', y='revenue', title="Revenue Trend Over Time")
    else:
        cat_rev = data.groupby('category')['revenue_proxy'].sum().reset_index().sort_values('revenue_proxy', ascending=False).head(10)
        fig = px.bar(cat_rev, x='category', y='revenue_proxy', title="Revenue by Category (Top 10)")
    return fig


def render_rating_distribution(data):
    fig = px.histogram(data, x='rating_num', nbins=10, title="Rating Distribution")
    return fig


def render_price_scatter(data):
    fig = px.scatter(data, x='actual_price_num', y='discounted_price_num', color='rating_num', title="Actual vs Discounted Price", opacity=0.6)
    return fig


def render_correlation_heatmap(data):
    nums = ['actual_price_num', 'discounted_price_num', 'discount_pct_num', 'rating_num', 'rating_count_num']
    available_nums = [n for n in nums if n in data.columns]
    fig = px.imshow(data[available_nums].corr(), text_auto=True, aspect="auto", title="Correlation Matrix")
    return fig


def render_geo_distribution(data):
    map_data = data.dropna(subset=['latitude', 'longitude'])
    if not map_data.empty:
        fig = px.scatter_geo(map_data, lat='latitude', lon='longitude', color='rating_num', title="Geographic Distribution")
    else:
        geo = data['country'].value_counts().head(10).reset_index()
        geo.columns = ['country', 'count']
        fig = px.bar(geo, x='country', y='count', title="Geographic Distribution (Top Countries)")
    return fig


def render_data_preview(data):
    st.subheader("Data Preview")
    st.dataframe(data)


def render_footer():
    st.sidebar.markdown("---")
    st.sidebar.caption("Data Source: Amazon Dataset")
    if st.sidebar.button("Refresh"):
        st.rerun()
    st.markdown("---")
    st.caption("Data Source: Amazon Dataset | Built with Streamlit")
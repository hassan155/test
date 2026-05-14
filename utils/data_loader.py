import pandas as pd
import numpy as np


def clean_price(series):
    return pd.to_numeric(series.astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')


def clean_pct(series):
    return pd.to_numeric(series.astype(str).str.replace('%', '', regex=True), errors='coerce')


def clean_count(series):
    return pd.to_numeric(series.astype(str).str.replace(',', '', regex=True), errors='coerce')


def load_and_clean(file_path):
    df = pd.read_csv(file_path)
    
    df['discounted_price_num'] = clean_price(df['discounted_price'])
    df['actual_price_num'] = clean_price(df['actual_price'])
    df['discount_pct_num'] = clean_pct(df['discount_percentage'])
    df['rating_count_num'] = clean_count(df['rating_count'])
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
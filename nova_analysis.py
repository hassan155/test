import pandas as pd
import numpy as np

def load_and_clean(file_path):
    df = pd.read_csv(file_path)
    
    def clean_price(series):
        return pd.to_numeric(series.astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    
    def clean_pct(series):
        return pd.to_numeric(series.astype(str).str.replace('%', '', regex=True), errors='coerce')
    
    def clean_count(series):
        return pd.to_numeric(series.astype(str).str.replace(',', '', regex=True), errors='coerce')
    
    df['discounted_price_num'] = clean_price(df['discounted_price'])
    df['actual_price_num'] = clean_price(df['actual_price'])
    df['discount_pct_num'] = clean_pct(df['discount_percentage'])
    df['rating_count_num'] = clean_count(df['rating_count'])
    df['rating_num'] = pd.to_numeric(df['rating'], errors='coerce')
    
    return df

def analyze(file_path):
    df = load_and_clean(file_path)
    
    print("=== DATASET SHAPE ===")
    print(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}\n")
    
    print("=== MISSING VALUES ===")
    print(df.isnull().sum().sort_values(ascending=False))
    print()
    
    numeric_cols = ['actual_price_num', 'discounted_price_num', 'discount_pct_num', 'rating_num', 'rating_count_num']
    
    print("=== DESCRIPTIVE STATISTICS ===")
    print(df[numeric_cols].describe().T)
    print()
    
    print("=== SKEWNESS & KURTOSIS ===")
    print(df[numeric_cols].agg(['skew', 'kurtosis']))
    print()
    
    print("=== CORRELATION MATRIX ===")
    print(df[numeric_cols].corr())
    print()
    
    print("=== TOP 10 CATEGORIES ===")
    print(df['category'].value_counts().head(10))
    print()
    
    print("=== RATING DISTRIBUTION ===")
    print(df['rating_num'].value_counts().sort_index())
    print()
    
    print("=== DUPLICATE PRODUCT_IDS ===")
    print(df['product_id'].duplicated().sum())
    print()
    
    print("=== ZERO/NEGATIVE PRICE ROWS ===")
    print(f"Actual price <= 0: {(df['actual_price_num'] <= 0).sum()}")
    print(f"Discounted price <= 0: {(df['discounted_price_num'] <= 0).sum()}")
    print()
    
    print("=== AVG RATING BY DISCOUNT BUCKET ===")
    df['discount_bucket'] = pd.cut(df['discount_pct_num'], bins=[0, 20, 40, 60, 80, 100])
    print(df.groupby('discount_bucket')['rating_num'].mean())
    print()
    
    return df

if __name__ == "__main__":
    analyze('/Users/hassanmulla/Downloads/NOVA_Phase2/Test/amazon.csv')
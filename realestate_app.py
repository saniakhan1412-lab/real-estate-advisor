import streamlit as st
import pandas as pd

df = pd.read_csv(Users/saniakhan/Downloads/'housing_cleaned.csv.gz')

st.set_page_config(page_title="Real Estate Investment Advisor", layout="wide")
st.title('🏠 Real Estate Investment Advisor')
st.markdown('Analyze property trends and make smart investment decisions - By Sania Khan')

st.sidebar.header('🔍 Filter Properties')

city_filter = st.sidebar.multiselect(
    'Select City',
    options=df['City'].unique(),
    default=list(df['City'].unique()[:5])
)

property_filter = st.sidebar.multiselect(
    'Select Property Type',
    options=df['Property_Type'].unique(),
    default=list(df['Property_Type'].unique())
)

bhk_filter = st.sidebar.multiselect(
    'Select BHK',
    options=sorted(df['BHK'].unique()),
    default=sorted(df['BHK'].unique())
)

filtered_df = df[
    (df['City'].isin(city_filter)) &
    (df['Property_Type'].isin(property_filter)) &
    (df['BHK'].isin(bhk_filter))
]

st.subheader('📊 Key Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Properties', f"{len(filtered_df):,}")
col2.metric('Avg Price (Lakhs)', f"₹{filtered_df['Price_in_Lakhs'].mean():.1f}L")
col3.metric('Avg Size (SqFt)', f"{filtered_df['Size_in_SqFt'].mean():.0f}")
col4.metric('Avg Price/SqFt', f"₹{filtered_df['Price_per_SqFt'].mean():.0f}")

st.markdown('---')

col1, col2 = st.columns(2)

with col1:
    st.subheader('🏙️ Average Price by City')
    city_price = filtered_df.groupby('City')['Price_in_Lakhs'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(city_price)

with col2:
    st.subheader('🏠 Properties by Type')
    type_counts = filtered_df['Property_Type'].value_counts()
    st.bar_chart(type_counts)

col3, col4 = st.columns(2)

with col3:
    st.subheader('🛏️ Average Price by BHK')
    bhk_price = filtered_df.groupby('BHK')['Price_in_Lakhs'].mean()
    st.bar_chart(bhk_price)

with col4:
    st.subheader('💰 Good Investment Distribution')
    investment_counts = filtered_df['Good_Investment'].value_counts()
    investment_counts.index = ['Good Investment', 'Not Good Investment']
    st.bar_chart(investment_counts)

st.markdown('---')

col5, col6 = st.columns(2)

with col5:
    st.subheader('📈 Top 10 Cities by Future Price')
    future_price = filtered_df.groupby('City')['Future_Price'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(future_price)

with col6:
    st.subheader('🛋️ Furnished Status vs Price')
    furnished_price = filtered_df.groupby('Furnished_Status')['Price_in_Lakhs'].mean()
    st.bar_chart(furnished_price)

st.markdown('---')
st.subheader('📋 Property Data')
st.dataframe(filtered_df[['City', 'Property_Type', 'BHK', 'Size_in_SqFt', 'Price_in_Lakhs', 'Price_per_SqFt', 'Good_Investment', 'Future_Price']].head(100))

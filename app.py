import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import openai

# Load API keys
load_dotenv()
fmp_key = os.getenv("FMP_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# FMP API base URL
BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_company_profile(symbol):
    url = f"{BASE_URL}/profile/{symbol}?apikey={fmp_key}"
    response = requests.get(url)
    return response.json()[0] if response.json() else None

def fetch_balance_sheet(symbol, period="annual", limit=5):
    url = f"{BASE_URL}/balance-sheet-statement/{symbol}?period={period}&limit={limit}&apikey={fmp_key}"
    response = requests.get(url)
    return pd.DataFrame(response.json())

def analyze_with_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a financial analyst expert in Indian stock markets."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

def main():
    st.title("📊 Indian Stock Balance Sheet Analyzer")
    
    # User input
    symbol = st.text_input("Enter Indian Stock Symbol (e.g., TCS, INFY, RELIANCE):", "TCS")
    
    if st.button("Analyze"):
        with st.spinner("Fetching data..."):
            # Fetch data
            profile = fetch_company_profile(symbol)
            balance_sheet = fetch_balance_sheet(symbol)
            
            if profile and not balance_sheet.empty:
                st.success(f"Data loaded for **{profile['companyName']}**!")
                
                # Display company info
                st.subheader("Company Overview")
                col1, col2 = st.columns(2)
                col1.metric("Sector", profile['sector'])
                col2.metric("Market Cap", f"${profile['mktCap']/1e9:.2f}B")
                
                # Visualize key metrics
                st.subheader("Balance Sheet Trends")
                fig = px.bar(
                    balance_sheet,
                    x='date',
                    y=['totalAssets', 'totalLiabilities', 'totalStockholdersEquity'],
                    title="Assets vs Liabilities vs Equity",
                    labels={"value": "Amount (USD)", "variable": "Category"}
                )
                st.plotly_chart(fig)
                
                # Generate AI analysis
                st.subheader("AI-Powered Analysis")
                prompt = f"""
                Analyze the balance sheet trends for {symbol} (Indian Stock) below. Focus on:
                1. Asset-Liability health
                2. Debt-to-Equity trends
                3. Liquidity risks
                4. Overall financial stability
                
                Balance Sheet Data (Last 5 years):
                {balance_sheet[['date', 'totalAssets', 'totalLiabilities', 'totalStockholdersEquity', 'cashAndCashEquivalents']].to_csv(index=False)}
                """
                
                ai_analysis = analyze_with_ai(prompt)
                st.write(ai_analysis)
                
            else:
                st.error("Invalid symbol or no data found. Try: INFY, RELIANCE, HDFCBANK")

if __name__ == "__main__":
    main()

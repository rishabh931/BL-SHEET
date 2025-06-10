import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from textwrap import fill

# Initialize styling
sns.set(style="whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'

def get_stock_data(symbol):
    """Fetch financial data using yfinance with Indian stock suffix handling"""
    # Append .NS for NSE if not provided
    if '.' not in symbol:
        symbol += ".NS"
    
    stock = yf.Ticker(symbol)
    
    # Get financial statements
    balance_sheet = stock.balance_sheet
    income_stmt = stock.financials
    cash_flow = stock.cashflow
    
    # Get additional info
    info = stock.info
    return balance_sheet, income_stmt, cash_flow, info

def analyze_balance_sheet(balance_sheet, income_stmt, info):
    """Perform comprehensive balance sheet analysis with visualizations"""
    # Convert to DataFrame and clean
    bs_df = balance_sheet.T
    bs_df.index = pd.to_datetime(bs_df.index).year
    
    # Key metrics extraction
    results = {
        'years': bs_df.index.tolist(),
        'total_assets': bs_df.get('Total Assets', pd.Series([np.nan]*len(bs_df))).values,
        'total_liab': bs_df.get('Total Liabilities', pd.Series([np.nan]*len(bs_df))).values,
        'total_equity': bs_df.get('Total Equity', pd.Series([np.nan]*len(bs_df))).values,
        'current_assets': bs_df.get('Current Assets', pd.Series([np.nan]*len(bs_df))).values,
        'current_liab': bs_df.get('Current Liabilities', pd.Series([np.nan]*len(bs_df))).values,
        'long_term_debt': bs_df.get('Long Term Debt', pd.Series([np.nan]*len(bs_df))).values,
        'cash': bs_df.get('Cash And Cash Equivalents', pd.Series([np.nan]*len(bs_df))).values
    }
    
    # Calculate financial ratios
    results['current_ratio'] = results['current_assets'] / results['current_liab']
    results['debt_to_equity'] = results['long_term_debt'] / results['total_equity']
    results['debt_to_assets'] = results['long_term_debt'] / results['total_assets']
    results['equity_ratio'] = results['total_equity'] / results['total_assets']
    
    # Generate visualizations
    generate_visualizations(results, info)
    
    # Generate AI-driven analysis
    analysis = generate_ai_analysis(results, info)
    
    return results, analysis

def generate_visualizations(results, info):
    """Create professional financial visualizations"""
    years = results['years']
    
    # Create figure with subplots
    plt.figure(figsize=(18, 20))
    plt.suptitle(f"Financial Analysis: {info.get('shortName', 'N/A')} ({info.get('symbol', '')})", 
                fontsize=16, fontweight='bold')
    
    # 1. Balance Sheet Composition
    plt.subplot(3, 2, 1)
    plt.stackplot(years, 
                results['current_assets']/1e7, 
                (results['total_assets'] - results['current_assets'])/1e7,
                labels=['Current Assets', 'Non-Current Assets'])
    plt.title('Asset Composition (₹ Crores)', fontweight='bold')
    plt.ylabel('Value (₹ Crores)')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # 2. Liability vs Equity
    plt.subplot(3, 2, 2)
    plt.stackplot(years, 
                results['current_liab']/1e7, 
                results['long_term_debt']/1e7,
                (results['total_equity'])/1e7,
                labels=['Current Liabilities', 'Long-Term Debt', 'Shareholders Equity'])
    plt.title('Capital Structure (₹ Crores)', fontweight='bold')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # 3. Financial Health Ratios
    plt.subplot(3, 2, 3)
    plt.plot(years, results['current_ratio'], 'bo-', label='Current Ratio')
    plt.axhline(y=1.5, color='r', linestyle='--', alpha=0.3)
    plt.axhline(y=1, color='g', linestyle='--', alpha=0.3)
    plt.title('Liquidity Analysis', fontweight='bold')
    plt.ylabel('Current Ratio')
    plt.grid(True, alpha=0.3)
    
    # 4. Debt Management
    plt.subplot(3, 2, 4)
    plt.plot(years, results['debt_to_equity'], 'mo-', label='Debt/Equity')
    plt.plot(years, results['debt_to_assets'], 'co-', label='Debt/Assets')
    plt.title('Leverage Analysis', fontweight='bold')
    plt.ylabel('Ratio')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 5. Cash Position
    plt.subplot(3, 2, 5)
    plt.bar(years, results['cash']/1e7, color='green')
    plt.title('Cash Reserves (₹ Crores)', fontweight='bold')
    plt.ylabel('Cash (₹ Crores)')
    plt.grid(True, alpha=0.3)
    
    # 6. Equity Growth
    plt.subplot(3, 2, 6)
    plt.plot(years, results['total_equity']/1e7, 'go-')
    plt.fill_between(years, results['total_equity']/1e7, alpha=0.3, color='green')
    plt.title('Shareholders Equity (₹ Crores)', fontweight='bold')
    plt.ylabel('Equity (₹ Crores)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('balance_sheet_analysis.png', dpi=300)
    plt.show()

def generate_ai_analysis(results, info):
    """Generate AI-driven fundamental analysis"""
    latest_year = results['years'][-1]
    cr = results['current_ratio'][-1]
    dte = results['debt_to_equity'][-1]
    equity_ratio = results['equity_ratio'][-1]
    cash = results['cash'][-1] / 1e7  # in crores
    
    # Liquidity analysis
    if cr > 2.0:
        liquidity = "excellent short-term financial health"
    elif cr > 1.5:
        liquidity = "comfortable liquidity position"
    elif cr > 1.2:
        liquidity = "adequate current assets coverage"
    elif cr > 1.0:
        liquidity = "minimal liquidity buffer"
    else:
        liquidity = "potential liquidity concerns"
    
    # Debt analysis
    if dte < 0.3:
        debt = "conservative debt management with low financial risk"
    elif dte < 0.7:
        debt = "moderate leverage that's typically manageable"
    elif dte < 1.0:
        debt = "aggressive financing strategy"
    else:
        debt = "highly leveraged position increasing bankruptcy risk"
    
    # Equity analysis
    if equity_ratio > 0.6:
        equity = "strong equity base providing financial stability"
    elif equity_ratio > 0.4:
        equity = "balanced capital structure"
    else:
        equity = "asset-heavy with potential refinancing risks"
    
    # Cash position
    cash_str = f"₹{cash:.2f} Crores" if not np.isnan(cash) else "insufficient data"
    
    # Compile final analysis
    analysis = f"""
    Fundamental Analysis Report: {info.get('shortName', 'N/A')} ({info.get('symbol', '')})
    As of {latest_year} Fiscal Year
    
    * Liquidity Position: 
    Current Ratio of {cr:.2f} indicates {liquidity}. 
    This measures the company's ability to meet short-term obligations.
    
    * Debt Management: 
    Debt-to-Equity ratio of {dte:.2f} suggests {debt}. 
    Long-term debt stands at ₹{results['long_term_debt'][-1]/1e7:.2f} Crores.
    
    * Capital Structure: 
    Equity Ratio of {equity_ratio:.2f} shows {equity}.
    Total Equity: ₹{results['total_equity'][-1]/1e7:.2f} Crores
    
    * Cash Position: 
    Strong cash reserves of {cash_str} providing operational flexibility.
    
    * Asset Efficiency: 
    Current assets comprise {(results['current_assets'][-1]/results['total_assets'][-1])*100:.1f}% of total assets, 
    indicating {'efficient working capital management' if results['current_assets'][-1]/results['total_assets'][-1] > 0.4 else 'capital-intensive operations'}.
    
    Recommendation: {'Conservative' if dte < 0.5 and cr > 1.5 else 'Moderate'} risk profile.
    """
    
    return fill(analysis, width=80)

def main():
    """Main function to run the balance sheet analyzer"""
    print("Indian Stock Balance Sheet Analyzer")
    symbol = input("Enter stock symbol or name (e.g., RELIANCE, TCS.NS, INFY): ").strip()
    
    try:
        print(f"\nFetching data for {symbol}...")
        balance_sheet, income_stmt, cash_flow, info = get_stock_data(symbol)
        
        if balance_sheet.empty:
            print("Error: No balance sheet data available for this stock")
            return
        
        print("Analyzing financial health...")
        results, analysis = analyze_balance_sheet(balance_sheet, income_stmt, info)
        
        print("\n" + "="*80)
        print(analysis)
        print("="*80)
        print("Visual analysis saved as 'balance_sheet_analysis.png'")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please check the stock symbol and try again. Use '.NS' suffix for NSE stocks.")

if __name__ == "__main__":
    main()

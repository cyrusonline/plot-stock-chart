import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
from datetime import datetime, timedelta

def format_stock_symbol(symbol):
    """
    Format stock symbol to proper format
    - For HK stocks: Convert numbers like "700" to "0700.HK"
    - For US stocks: Return as is
    """
    # Check if it's a number (potential HK stock)
    try:
        number = int(symbol)
        # If it's likely a HK stock (usually 1-4 digits)
        if number < 10000:
            return f"{number:04d}.HK"
        return symbol
    except ValueError:
        # If it already has .HK suffix, return as is
        if '.HK' in symbol.upper():
            return symbol.upper()
        return symbol

def generate_stock_charts(symbols, period='6mo', save_dir='stock_charts'):
    """
    Generate stock charts with candlesticks and SMAs
    
    Parameters:
    symbols (list): List of stock symbols (e.g., ['AAPL', '700', '9988'])
    period (str): Time period ('1mo', '6mo', '1y', etc.)
    save_dir (str): Directory to save the charts
    """
    
    # Create output directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Style configuration for dark theme
    mc = mpf.make_marketcolors(up='#26A69A',
                              down='#EF5350',
                              edge='inherit',
                              wick='inherit',
                              volume='in',
                              ohlc='inherit')
    
    s = mpf.make_mpf_style(marketcolors=mc,
                          figcolor='#1E1E1E',
                          facecolor='#1E1E1E',
                          edgecolor='#3E3E3E',
                          gridcolor='#3E3E3E',
                          gridstyle=':',
                          gridaxis='both',
                          y_on_right=True)
    
    for symbol in symbols:
        try:
            # Format the symbol
            formatted_symbol = format_stock_symbol(symbol)
            
            # Download data
            stock = yf.Ticker(formatted_symbol)
            df = stock.history(period=period)
            
            if df.empty:
                print(f"No data found for {formatted_symbol}")
                continue
                
            # Calculate SMAs
            df['SMA10'] = df['Close'].rolling(window=10).mean()
            df['SMA20'] = df['Close'].rolling(window=20).mean()
            
            # Get company name (if available)
            try:
                company_name = stock.info.get('longName', formatted_symbol)
            except:
                company_name = formatted_symbol
            
            # Create the plot
            apds = [
                mpf.make_addplot(df['SMA10'], color='#42A5F5', width=1, label='10 SMA'),
                mpf.make_addplot(df['SMA20'], color='#FF7043', width=1, label='20 SMA')
            ]
            
            # Plot and save
            fig, axes = mpf.plot(df,
                               type='candle',
                               style=s,
                               addplot=apds,
                               volume=True,
                               title=f'\n{company_name} ({formatted_symbol})',
                               figsize=(12, 8),
                               panel_ratios=(2, 0.5),
                               returnfig=True)
            
            # Adjust title color and add legend
            axes[0].set_title(f'{company_name} ({formatted_symbol})', color='white')
            
            # Create legend with correct parameters
            legend = axes[0].legend(['10 SMA', '20 SMA'])
            legend.get_frame().set_facecolor('#1E1E1E')
            legend.get_frame().set_edgecolor('#3E3E3E')
            for text in legend.get_texts():
                text.set_color('white')
            
            # Save the plot
            filename = f'{save_dir}/{formatted_symbol}_{datetime.now().strftime("%Y%m%d")}.png'
            fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#1E1E1E')
            print(f'Chart saved: {filename}')
            
        except Exception as e:
            print(f'Error processing {symbol} ({formatted_symbol}): {str(e)}')

# Example usage
symbols = [
  1310,
  2573,
  3626,
  8007,
  1693,
  2312,
  2350,
  8401,
  1715,
  7841,
  94,
  1664,
  2440,
  8137,
  1529,
  1726,
  205,
  6877,
  1948,
  1920,
  1728,
  1788,
  8087,
  8500,
  6128,
  204,
  2699,
  2974,
  2550,
  1143,
  620,
  243,
  381,
  720,
  476,
  1159,
  2159,
  2503,
  1991,
  1025,
  8050,
  2569,
  2566,
  2610,
  2629,
  2597,
  613,
  770,
  2340
]
# symbols = ['JOE','ACM','AMRX'，'ENS']  # Mix of US and HK stocks
generate_stock_charts(symbols,period='1y')
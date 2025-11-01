import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
from datetime import datetime, timedelta

def generate_stock_charts(symbols, period='6mo'):
    """
    Generate stock charts with candlesticks and SMAs
    
    Parameters:
    symbols (list): List of stock symbols (e.g., ['AAPL', '0700.HK'])
    period (str): Time period ('1mo', '6mo', '1y', etc.)
    """
    
    # Create output directory if it doesn't exist
    output_dir = 'stock_charts'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Style configuration for dark theme
    mc = mpf.make_marketcolors(up='#26A69A',down='#EF5350',
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
            # Download data
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            
            # Calculate SMAs
            df['SMA10'] = df['Close'].rolling(window=10).mean()
            df['SMA20'] = df['Close'].rolling(window=20).mean()
            
            # Create the plot
            apds = [
                mpf.make_addplot(df['SMA10'], color='#42A5F5', width=1),
                mpf.make_addplot(df['SMA20'], color='#FF7043', width=1)
            ]
            
            # Plot and save
            fig, axes = mpf.plot(df,
                               type='candle',
                               style=s,
                               addplot=apds,
                               volume=True,
                               title=f'\n{symbol} Stock Chart',
                               figsize=(12, 8),
                               panel_ratios=(2, 0.5),
                               returnfig=True)
            
            # Adjust title color
            axes[0].set_title(f'{symbol} Stock Chart', color='white')
            
            # Save the plot
            filename = f'{output_dir}/{symbol}_{datetime.now().strftime("%Y%m%d")}.png'
            fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#1E1E1E')
            print(f'Chart saved: {filename}')
            
        except Exception as e:
            print(f'Error processing {symbol}: {str(e)}')

# Example usage
symbols = ['AAPL', 'MSFT', '0700.HK', '9988.HK']
generate_stock_charts(symbols)
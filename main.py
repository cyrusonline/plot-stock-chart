import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
from datetime import datetime, timedelta

def format_stock_symbol(symbol):
    try:
        number = int(symbol)
        if number < 10000:
            return f"{number:04d}.HK"
        return symbol
    except ValueError:
        if '.HK' in symbol.upper():
            return symbol.upper()
        return symbol

def generate_stock_charts(symbols, period='6mo', save_dir='stock_charts'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
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
            formatted_symbol = format_stock_symbol(symbol)
            stock = yf.Ticker(formatted_symbol)
            df = stock.history(period=period)
            
            if df.empty:
                print(f"No data found for {formatted_symbol}")
                continue
                
            df['SMA10'] = df['Close'].rolling(window=10).mean()
            df['SMA20'] = df['Close'].rolling(window=20).mean()
            
            try:
                company_name = stock.info.get('longName', formatted_symbol)
            except:
                company_name = formatted_symbol
            
            apds = [
                mpf.make_addplot(df['SMA10'], color='#42A5F5', width=1, label='10 SMA'),
                mpf.make_addplot(df['SMA20'], color='#FF7043', width=1, label='20 SMA')
            ]
            
            fig, axes = mpf.plot(df,
                               type='candle',
                               style=s,
                               addplot=apds,
                               volume=True,
                               title=f'\n{company_name} ({formatted_symbol})',
                               figsize=(12, 8),
                               panel_ratios=(2, 0.5),
                               returnfig=True)
            
            # Set title and axis labels to white
            axes[0].set_title(f'{company_name} ({formatted_symbol})', color='white', pad=20)
            
            # Set axis labels and tick colors to white for both price and volume panels
            for ax in axes:
                ax.set_ylabel(ax.get_ylabel(), color='white')
                ax.set_xlabel(ax.get_xlabel(), color='white')
                ax.tick_params(colors='white')
                for spine in ax.spines.values():
                    spine.set_color('white')
            
            # Create legend with white text
            legend = axes[0].legend(['10 SMA', '20 SMA'])
            legend.get_frame().set_facecolor('#1E1E1E')
            legend.get_frame().set_edgecolor('#3E3E3E')
            for text in legend.get_texts():
                text.set_color('white')
            
            filename = f'{save_dir}/{formatted_symbol}_{datetime.now().strftime("%Y%m%d")}.png'
            fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#1E1E1E')
            print(f'Chart saved: {filename}')
            
        except Exception as e:
            print(f'Error processing {symbol} ({formatted_symbol}): {str(e)}')

# Example usage
symbols = [1645,'NVDA',6162, 1660]
generate_stock_charts(symbols)
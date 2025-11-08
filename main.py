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
    
    # --- Custom Market Colors ---
    mc = mpf.make_marketcolors(
        up='#00C853',  # light green for up candles
        down='#D50000',  # bright red for down candles
        edge='white',
        wick='white',
        volume='in'
    )

    # --- Custom Style matching AASTOCKS theme ---
    s = mpf.make_mpf_style(
        marketcolors=mc,
        base_mpf_style='nightclouds',
        facecolor='#000C2E',       # deep navy background
        figcolor='#000C2E',        # outer background
        edgecolor='#1C265A',
        gridcolor='#1C265A',
        gridstyle='-',
        gridaxis='both',
        y_on_right=True
    )

    # --- Fonts and plot settings ---
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
                mpf.make_addplot(df['SMA10'], color='#FFCC00', width=1.2, label='SMA10'),  # yellow
                mpf.make_addplot(df['SMA20'], color='#FF5252', width=1.2, label='SMA20')   # red
            ]

            fig, axes = mpf.plot(
                df,
                type='candle',
                style=s,
                addplot=apds,
                volume=True,
                title=f'{company_name}  ({formatted_symbol})',
                ylabel='Price (HKD)',
                ylabel_lower='Volume',
                figsize=(12, 8),
                tight_layout=True,
                returnfig=True
            )

            # --- Adjust axis color, labels, and tick style ---
            for ax in axes:
                ax.tick_params(colors='white')
                ax.yaxis.label.set_color('white')
                ax.xaxis.label.set_color('white')
                for spine in ax.spines.values():
                    spine.set_color('#1C265A')

            # Volume bar style — desaturate to light blue
            axes[-1].patch.set_facecolor('#00174F')

            # --- Title formatting ---
            axes[0].set_title(f'{company_name} ({formatted_symbol})', color='white', fontsize=13, pad=16)

            # --- Legend (top-left) ---
            legend = axes[0].legend(facecolor='#000C2E', edgecolor='#1C265A', fontsize=9, loc='upper left')
            for text in legend.get_texts():
                text.set_color('white')

            # Save to file
            filename = f'{save_dir}/{formatted_symbol}_{datetime.now().strftime("%Y%m%d")}.png'
            fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#000C2E')
            print(f'Chart saved: {filename}')

        except Exception as e:
            print(f'Error processing {symbol} ({formatted_symbol}): {str(e)}')
# def generate_stock_charts(symbols, period='6mo', save_dir='stock_charts'):
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
    
#     mc = mpf.make_marketcolors(up='#26A69A',
#                               down='#EF5350',
#                               edge='inherit',
#                               wick='inherit',
#                               volume='in',
#                               ohlc='inherit')
    
#     s = mpf.make_mpf_style(marketcolors=mc,
#                           figcolor='#1E1E1E',
#                           facecolor='#1E1E1E',
#                           edgecolor='#3E3E3E',
#                           gridcolor='#3E3E3E',
#                           gridstyle=':',
#                           gridaxis='both',
#                           y_on_right=True)
    
#     for symbol in symbols:
#         try:
#             formatted_symbol = format_stock_symbol(symbol)
#             stock = yf.Ticker(formatted_symbol)
#             df = stock.history(period=period)
            
#             if df.empty:
#                 print(f"No data found for {formatted_symbol}")
#                 continue
                
#             df['SMA10'] = df['Close'].rolling(window=10).mean()
#             df['SMA20'] = df['Close'].rolling(window=20).mean()
            
#             try:
#                 company_name = stock.info.get('longName', formatted_symbol)
#             except:
#                 company_name = formatted_symbol
            
#             apds = [
#                 mpf.make_addplot(df['SMA10'], color='#42A5F5', width=1, label='10 SMA'),
#                 mpf.make_addplot(df['SMA20'], color='#FF7043', width=1, label='20 SMA')
#             ]
            
#             fig, axes = mpf.plot(df,
#                                type='candle',
#                                style=s,
#                                addplot=apds,
#                                volume=True,
#                                title=f'\n{company_name} ({formatted_symbol})',
#                                figsize=(12, 8),
#                                panel_ratios=(2, 0.5),
#                                returnfig=True)
            
#             # Set title and axis labels to white
#             axes[0].set_title(f'{company_name} ({formatted_symbol})', color='white', pad=20)
            
#             # Set axis labels and tick colors to white for both price and volume panels
#             for ax in axes:
#                 ax.set_ylabel(ax.get_ylabel(), color='white')
#                 ax.set_xlabel(ax.get_xlabel(), color='white')
#                 ax.tick_params(colors='white')
#                 for spine in ax.spines.values():
#                     spine.set_color('white')
            
#             # Create legend with white text
#             legend = axes[0].legend(['10 SMA', '20 SMA'])
#             legend.get_frame().set_facecolor('#1E1E1E')
#             legend.get_frame().set_edgecolor('#3E3E3E')
#             for text in legend.get_texts():
#                 text.set_color('white')
            
#             filename = f'{save_dir}/{formatted_symbol}_{datetime.now().strftime("%Y%m%d")}.png'
#             fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#1E1E1E')
#             print(f'Chart saved: {filename}')
            
#         except Exception as e:
#             print(f'Error processing {symbol} ({formatted_symbol}): {str(e)}')

# Example usage

symbols = [
  "2432",
  "419",
  "2503",
  "464",
  "8391",
  "2175",
  "1130",
  "8365",
  "3395",
  "666",
  "544",
  "1028",
  "1140",
  "8460",
  "2371",
  "3919",
  "6181",
  "1801",
  "2012",
  "1709",
  "1822",
  "8623",
  "8482",
  "8510",
  "8246",
  "2330",
  "3677",
  "1783",
  "2582",
  "2373",
  "1769",
  "8238",
  "2577",
  "2216",
  "2110",
  "1541",
  "197",
  "2312",
  "810",
  "8159",
  "776",
  "804",
  "1119",
  "1939",
  "264",
  "1283",
  "2340",
  "2250",
  "8160",
  "1466",
  "2160",
  "2570",
  "9660",
  "2489",
  "139",
  "1380",
  "8305",
  "8153",
  "2212",
  "2221",
  "736",
  "8547",
  "3896",
  "8299",
  "1912",
  "3788",
  "8377",
  "2429",
  "2411",
  "9936",
  "1592",
  "2013",
  "1072",
  "1676",
  "2582",
  "1341",
  "8029",
  "8093",
  "376",
  "3800",
  "1662",
  "8367",
  "1228",
  "875",
  "3709",
  "209",
  "2105",
  "6628",
  "6610",
  "2257",
  "1355",
  "471",
  "1712",
  "1280",
  "65",
  "310",
  "1943",
  "697",
  "290",
  "6069",
  "2268",
  "261",
  "1787",
  "2096",
  "1030",
  "1931",
  "2582",
  "1347",
  "9986",
  "2487",
  "2142",
  "2228",
  "147",
  "1280",
  "8148",
  "279",
  "2250",
  "9926",
  "6080",
  "1870",
  "1729",
  "1413",
  "1772",
  "2209",
  "1282",
  "956",
  "2221",
  "2522",
  "1380",
  "205",
  "3939",
  "434",
  "8121",
  "399",
  "8148",
  "264",
  "3692",
  "1672",
  "2012",
  "2509",
  "1775",
  "8305",
  "858",
  "1718",
  "8245",
  "3395",
  "1228",
  "1949",
  "620",
  "6955",
  "1709",
  "1341",
  "6918",
  "2195",
  "8196",
  "9939",
  "120",
  "136",
  "8537",
  "8427",
  "8069",
  "2359",
  "1396",
  "2012",
  "8521",
  "2221",
  "1901",
  "1119",
  "8198",
  "1102",
  "1783",
  "6911",
  "1952",
  "863",
  "433",
  "1380",
  "1201",
  "1725",
  "1498",
  "3938",
  "6683",
  "20",
  "2550",
  "1530",
  "1908",
  "1473",
  "1725",
  "2453",
  "2577",
  "9880",
  "1069",
  "428",
  "8056",
  "593",
  "3681",
  "1341",
  "3933",
  "8153",
  "2512",
  "476",
  "6682",
  "399",
  "917",
  "9636",
  "254",
  "2586",
  "6855",
  "2432",
  "1520",
  "2159",
  "8283",
  "815",
  "2225",
  "2598",
  "1274",
  "6696",
  "329",
  "8275",
  "620",
  "2616",
  "8030",
  "959",
  "1091",
  "243",
  "809",
  "994",
  "2157",
  "1918",
  "1159",
  "381",
  "2431",
  "1991",
  "2503",
  "8635",
  "9986",
  "1942",
  "1611",
  "2562",
  "582",
  "2511",
  "1801",
  "6936",
  "6060",
  "8172",
  "8087",
  "2012",
  "8017",
  "1380",
  "8191",
  "1909",
  "1143",
  "377",
  "2550",
  "1783",
  "456",
  "767",
  "145",
  "36",
  "767",
  "8308",
  "1877",
  "990",
  "1967",
  "2159",
  "770",
  "9660",
  "854",
  "2246",
  "8536",
  "2162",
  "8246",
  "931",
  "2465",
  "6990",
  "1129",
  "8340",
  "1920",
  "6955",
  "8237",
  "863",
  "8493",
  "2255",
  "1683",
  "1872",
  "399",
  "2453",
  "1683",
  "399",
  "769",
  "3738",
  "8403",
  "428",
  "8455",
  "2297",
  "1247",
  "673",
  "8471",
  "9995",
  "2149",
  "899",
  "2127",
  "2521",
  "1119",
  "3919",
  "943",
  "2252",
  "6069",
  "3681",
  "8446",
  "2211",
  "3666",
  "1159",
  "9985",
  "6181",
  "613",
  "8176",
  "9860",
  "30",
  "3623",
  "264",
  "3680",
  "6610",
  "3390",
  "1468",
  "2012",
  "1011",
  "8472",
  "8163",
  "2522",
  "1723",
  "2330",
  "544",
  "3896",
  "2367",
  "2012",
  "476",
  "931",
  "8246",
  "769",
  "970",
  "464",
  "8196",
  "995",
  "1091",
  "2309",
  "1783",
  "1643",
  "290",
  "1693",
  "8189",
  "340",
  "575",
  "484",
  "2616",
  "1520",
  "1991",
  "8619",
  "707",
  "1810",
  "1818",
  "2142",
  "8292",
  "8176",
  "8403",
  "1466",
  "1421",
  "1782",
  "1949",
  "1872",
  "1870",
  "6696",
  "2362",
  "8645",
  "9958",
  "8482",
  "3311",
  "3330",
  "2429",
  "340",
  "1575",
  "515",
  "1211",
  "6660",
  "339",
  "572",
  "2498",
  "1865",
  "1762",
  "2556",
  "8195",
  "8198",
  "264",
  "875",
  "9880",
  "8093",
  "2533",
  "2228",
  "8431",
  "2342",
  "8292",
  "471",
  "1368",
  "400",
  "1020",
  "377",
  "1274",
  "6682",
  "3893",
  "274",
  "193",
  "136",
  "1636",
  "2098",
  "1728",
  "8107",
  "8320",
  "1232",
  "8340",
  "209",
  "8308",
  "464",
  "1059",
  "8391",
  "727",
  "815",
  "2228",
  "632",
  "456",
  "8189",
  "9669",
  "8316",
  "689",
  "632",
  "572",
  "136",
  "451",
  "1163",
  "2503",
  "887",
  "110",
  "1427",
  "1748",
  "9923",
  "8611",
  "92",
  "8283",
  "3708",
  "8162",
  "2212",
  "8262",
  "290",
  "261",
  "8622",
  "1253",
  "8026",
  "206",
  "8657",
  "1252",
  "2276",
  "2399",
  "6680",
  "3889",
  "3800",
  "1007",
  "1907",
  "2556",
  "8213",
  "804",
  "8613",
  "1825",
  "8168",
  "1783",
  "8511",
  "33",
  "20",
  "2498",
  "1942",
  "2322",
  "8115",
  "8406"
]
generate_stock_charts(symbols, period='1y')
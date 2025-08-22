import pandas as pd
from ta.trend import MACD, SMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def calculate_technical_indicators(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates technical indicators using the 'ta' library.
    Assumes prices_df has columns: 'open', 'high', 'low', 'close', 'volume'
    """
    if prices_df.empty:
        return prices_df

    # Ensure columns are lowercase as expected by the rest of the app
    prices_df.columns = [col.lower() for col in prices_df.columns]

    # RSI
    prices_df['rsi'] = RSIIndicator(close=prices_df['close'], window=14).rsi()

    # MACD
    macd_indicator = MACD(close=prices_df['close'], window_slow=26, window_fast=12, window_sign=9)
    prices_df['macd'] = macd_indicator.macd()
    prices_df['macd_signal'] = macd_indicator.macd_signal()
    prices_df['macd_hist'] = macd_indicator.macd_diff()

    # Bollinger Bands
    bb_indicator = BollingerBands(close=prices_df['close'], window=20, window_dev=2)
    prices_df['bb_lower'] = bb_indicator.bollinger_lband()
    prices_df['bb_upper'] = bb_indicator.bollinger_hband()
    prices_df['bb_middle'] = bb_indicator.bollinger_mavg()

    # SMAs
    prices_df['sma_50'] = SMAIndicator(close=prices_df['close'], window=50).sma_indicator()
    prices_df['sma_200'] = SMAIndicator(close=prices_df['close'], window=200).sma_indicator()
    
    return prices_df
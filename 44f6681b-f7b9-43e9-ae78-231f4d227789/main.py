from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InstitutionalOwnership, SocialSentiment
from surmount.technical_indicators import RSI, SMA, Volume
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers of interest for small to mid-cap stocks 
        # (This static list should be dynamically generated or updated in practice)
        self.tickers = ["TICKER1", "TICKER2", "TICKER3"]

        # Creating data list with needed signals
        self.data_list = [InstitutionalOwnership(ticker) for ticker in self.tickers] + \
                         [SocialSentiment(ticker) for ticker in self.tickers]
    
    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}

        for ticker in self.tickers:
            allocation_dict[ticker] = 0  # Default no position
            
            # Checking for Institutional Signal
            institutional_data = data[("institutional_ownership", ticker)]
            if institutional_data:
                dark_pool_activity = any(activity['totalInvested'] > 500000 for activity in institutional_data)
                options_sweep_activity = any(activity['totalCalls'] > 100000 and activity['volume'] > activity['openInterest'] for activity in institutional_data)
            else:
                dark_pool_activity = options_sweep_activity = False
                
            # Checking for Retail Frenzy 
            social_sentiment_data = data[("social_sentiment", ticker)]
            if social_sentiment_data:
                # Assuming a function to calculate the spike exists 
                social_volume_spike = check_social_volume_spike(social_sentiment_data)
            else:
                social_volume_spike = False
                
            # Technical Signal - Assuming functions for momentum checks and resistance level calculation exist
            is_momentum_candle = check_momentum_candle(ticker, data)
            is_volume_spike = check_volume_spike(ticker, data, 3)
            
            # Entry Logic
            if dark_pool_activity or options_sweep_activity:
                if social_volume_spike:
                    if is_momentum_candle and is_volume_spike:
                        allocation_dict[ticker] = 1  # Full allocation
            
            # Exit Logic: Assuming RSI and price data checks function exist
            if should_exit_based_on_rsi(ticker, data) or should_exit_based_on_social_sentiment(social_sentiment_data) or not check_price_attempt(ticker, data):
                allocation_dict[ticker] = 0  # Close position
                
        return TargetAllocation(allocation_dict)
    
# Helpers (Pseudo code - implement these based on actual data and logic required)
def check_social_volume_spike(social_data):
    # Analyze social volume for 5x average spike
    return True  # Placeholder return

def check_momentum_candle(ticker, ohlcv_data):
    # Check last candle for bullish engulfing or strong momentum candle pattern
    return True  # Placeholder return

def check_volume_spike(ticker, data, multiple):
    # Check if volume > 3x the 10-day average
    return True  # Placeholder return

def should_exit_based_on_rsi(ticker, data):
    # Get latest RSI and check if greater than 70 and slowing
    return False  # Placeholder return
  
def should_exit_based_on_social_sentiment(social_data):
    # Check for decline in social sentiment or tweet volume
    return False  # Placeholder return

def check_price_attempt(ticker, data):
    # Check if price fails to break high-of-day on second attempt
    return True  # Placeholder return
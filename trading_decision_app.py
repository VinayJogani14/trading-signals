import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# Try to import roboquant and ta, with fallback handling
try:
    import roboquant as rq
    ROBOQUANT_AVAILABLE = True
except ImportError:
    ROBOQUANT_AVAILABLE = False
    st.warning("Roboquant not fully loaded. Using alternative analysis methods.")

try:
    import ta
    TA_AVAILABLE = True
except ImportError:
    TA_AVAILABLE = False
    st.error("TA library not available. Please install: pip install ta")

# Configure the page
st.set_page_config(
    page_title="Trading Decision Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.decision-box {
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    text-align: center;
    font-size: 1.2rem;
    font-weight: bold;
}
.buy-signal {
    background-color: #d4edda;
    border: 2px solid #28a745;
    color: #155724;
}
.sell-signal {
    background-color: #f8d7da;
    border: 2px solid #dc3545;
    color: #721c24;
}
.neutral-signal {
    background-color: #fff3cd;
    border: 2px solid #ffc107;
    color: #856404;
}
</style>
""", unsafe_allow_html=True)

class TradingAnalyzer:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        self.current_price = None
        
    def fetch_data(self, period="6mo"):
        """Fetch stock data using yfinance"""
        try:
            ticker = yf.Ticker(self.symbol)
            self.data = ticker.history(period=period)
            self.current_price = self.data['Close'].iloc[-1]
            return True
        except Exception as e:
            st.error(f"Error fetching data for {self.symbol}: {e}")
            return False
    
    def calculate_technical_indicators(self):
        """Calculate various technical indicators"""
        if self.data is None:
            return None
        
        df = self.data.copy()
        
        try:
            if TA_AVAILABLE:
                # Moving Averages
                df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
                df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
                df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
                df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)
                
                # RSI
                df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
                
                # MACD
                df['MACD'] = ta.trend.macd_diff(df['Close'])
                df['MACD_signal'] = ta.trend.macd_signal(df['Close'])
                
                # Bollinger Bands
                bb = ta.volatility.BollingerBands(df['Close'])
                df['BB_upper'] = bb.bollinger_hband()
                df['BB_lower'] = bb.bollinger_lband()
                df['BB_middle'] = bb.bollinger_mavg()
            else:
                # Fallback manual calculations
                df['SMA_20'] = df['Close'].rolling(window=20).mean()
                df['SMA_50'] = df['Close'].rolling(window=50).mean()
                df['EMA_12'] = df['Close'].ewm(span=12).mean()
                df['EMA_26'] = df['Close'].ewm(span=26).mean()
                
                # Simple RSI calculation
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                df['RSI'] = 100 - (100 / (1 + rs))
                
                # Simple MACD calculation
                df['MACD'] = df['EMA_12'] - df['EMA_26']
                df['MACD_signal'] = df['MACD'].ewm(span=9).mean()
                
                # Simple Bollinger Bands
                sma_20 = df['Close'].rolling(window=20).mean()
                std_20 = df['Close'].rolling(window=20).std()
                df['BB_upper'] = sma_20 + (std_20 * 2)
                df['BB_lower'] = sma_20 - (std_20 * 2)
                df['BB_middle'] = sma_20
            
            # Support and Resistance levels (works with both)
            df['Support'] = df['Low'].rolling(window=20).min()
            df['Resistance'] = df['High'].rolling(window=20).max()
            
            return df
            
        except Exception as e:
            st.error(f"Error calculating technical indicators: {e}")
            return None
    
    def generate_signals(self):
        """Generate buy/sell signals based on technical analysis"""
        df = self.calculate_technical_indicators()
        if df is None:
            return None, None, "No data available"
        
        latest = df.iloc[-1]
        signals = []
        
        # Moving Average Signals
        if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
            signals.append(("Moving Average", "BUY", "Price above both SMA20 and SMA50"))
        elif latest['Close'] < latest['SMA_20'] < latest['SMA_50']:
            signals.append(("Moving Average", "SELL", "Price below both SMA20 and SMA50"))
        else:
            signals.append(("Moving Average", "NEUTRAL", "Mixed moving average signals"))
        
        # RSI Signals
        if latest['RSI'] < 30:
            signals.append(("RSI", "BUY", f"Oversold condition (RSI: {latest['RSI']:.1f})"))
        elif latest['RSI'] > 70:
            signals.append(("RSI", "SELL", f"Overbought condition (RSI: {latest['RSI']:.1f})"))
        else:
            signals.append(("RSI", "NEUTRAL", f"Neutral RSI ({latest['RSI']:.1f})"))
        
        # MACD Signals
        if latest['MACD'] > latest['MACD_signal']:
            signals.append(("MACD", "BUY", "MACD above signal line"))
        else:
            signals.append(("MACD", "SELL", "MACD below signal line"))
        
        # Bollinger Bands Signals
        if latest['Close'] < latest['BB_lower']:
            signals.append(("Bollinger Bands", "BUY", "Price below lower band"))
        elif latest['Close'] > latest['BB_upper']:
            signals.append(("Bollinger Bands", "SELL", "Price above upper band"))
        else:
            signals.append(("Bollinger Bands", "NEUTRAL", "Price within bands"))
        
        # Calculate overall signal
        buy_signals = len([s for s in signals if s[1] == "BUY"])
        sell_signals = len([s for s in signals if s[1] == "SELL"])
        
        if buy_signals > sell_signals:
            overall_signal = "BUY"
        elif sell_signals > buy_signals:
            overall_signal = "SELL"
        else:
            overall_signal = "NEUTRAL"
        
        return signals, overall_signal, df
    
    def calculate_price_targets(self, action, buy_price=None):
        """Calculate suggested entry/exit prices"""
        df = self.calculate_technical_indicators()
        if df is None:
            return None
        
        latest = df.iloc[-1]
        current_price = self.current_price
        
        if action == "BUY":
            # Support level as buy target
            support = latest['Support']
            buy_target = max(support * 0.98, current_price * 0.95)  # 2% below support or 5% below current
            stop_loss = buy_target * 0.95  # 5% below buy target
            take_profit = buy_target * 1.15  # 15% above buy target
            
            return {
                "entry_price": buy_target,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "risk_reward": (take_profit - buy_target) / (buy_target - stop_loss)
            }
        
        elif action == "SELL" and buy_price:
            # Resistance level as sell target
            resistance = latest['Resistance']
            sell_target = min(resistance * 1.02, current_price * 1.05)  # 2% above resistance or 5% above current
            
            profit_loss = sell_target - buy_price
            profit_percentage = (profit_loss / buy_price) * 100
            
            return {
                "sell_price": sell_target,
                "profit_loss": profit_loss,
                "profit_percentage": profit_percentage,
                "current_price": current_price
            }
        
        return None

def create_price_chart(df, symbol):
    """Create an interactive price chart with technical indicators"""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=[f'{symbol} Price Chart', 'RSI', 'MACD'],
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    # Moving averages
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='orange')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='blue')),
        row=1, col=1
    )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_upper'], name='BB Upper', line=dict(color='gray', dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_lower'], name='BB Lower', line=dict(color='gray', dash='dash')),
        row=1, col=1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')),
        row=2, col=1
    )
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # MACD
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD_signal'], name='MACD Signal', line=dict(color='red')),
        row=3, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text=f"{symbol} Technical Analysis"
    )
    
    fig.update_xaxes(rangeslider_visible=False)
    
    return fig

def main():
    st.markdown('<h1 class="main-header">🚀 Trading Decision Tool</h1>', unsafe_allow_html=True)
    st.markdown("*Powered by Roboquant - Make informed trading decisions with technical analysis*")
    
    # Sidebar for inputs
    st.sidebar.header("📊 Trading Parameters")
    
    # Stock symbol input
    symbol = st.sidebar.text_input("Stock Symbol", value="AAPL", help="Enter stock symbol (e.g., AAPL, TSLA, MSFT)")
    
    # Main decision: Buy or Sell
    decision = st.sidebar.radio("What would you like to do?", ["🔍 Analyze for Buy Signal", "💰 Analyze for Sell Signal"])
    
    if not symbol:
        st.warning("Please enter a stock symbol to begin analysis.")
        return
    
    # Initialize analyzer
    analyzer = TradingAnalyzer(symbol.upper())
    
    # Fetch data
    with st.spinner(f"Fetching data for {symbol.upper()}..."):
        if not analyzer.fetch_data():
            return
    
    # Generate signals
    signals, overall_signal, df = analyzer.generate_signals()
    
    if signals is None:
        st.error("Could not generate trading signals. Please try again.")
        return
    
    # Display current price
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Price", f"${analyzer.current_price:.2f}")
    with col2:
        change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
        change_pct = (change / df['Close'].iloc[-2]) * 100
        st.metric("Daily Change", f"${change:.2f}", f"{change_pct:.2f}%")
    with col3:
        volume = df['Volume'].iloc[-1]
        st.metric("Volume", f"{volume:,.0f}")
    
    # Handle Buy Analysis
    if decision == "🔍 Analyze for Buy Signal":
        st.header("📈 Buy Signal Analysis")
        
        # Display overall recommendation
        if overall_signal == "BUY":
            st.markdown(f'<div class="decision-box buy-signal">✅ RECOMMENDATION: BUY {symbol.upper()}</div>', 
                       unsafe_allow_html=True)
        elif overall_signal == "SELL":
            st.markdown(f'<div class="decision-box sell-signal">❌ RECOMMENDATION: DO NOT BUY {symbol.upper()}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="decision-box neutral-signal">⚠️ RECOMMENDATION: NEUTRAL - WAIT {symbol.upper()}</div>', 
                       unsafe_allow_html=True)
        
        # Calculate price targets
        price_targets = analyzer.calculate_price_targets("BUY")
        
        if price_targets:
            st.subheader("🎯 Suggested Entry Strategy")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Entry Price", f"${price_targets['entry_price']:.2f}")
            with col2:
                st.metric("Stop Loss", f"${price_targets['stop_loss']:.2f}")
            with col3:
                st.metric("Take Profit", f"${price_targets['take_profit']:.2f}")
            with col4:
                st.metric("Risk/Reward", f"{price_targets['risk_reward']:.2f}:1")
        
        # Detailed signal analysis
        st.subheader("🔍 Technical Indicator Analysis")
        for indicator, signal, explanation in signals:
            if signal == "BUY":
                st.success(f"**{indicator}**: {signal} - {explanation}")
            elif signal == "SELL":
                st.error(f"**{indicator}**: {signal} - {explanation}")
            else:
                st.info(f"**{indicator}**: {signal} - {explanation}")
    
    # Handle Sell Analysis
    else:
        st.header("📉 Sell Signal Analysis")
        
        # Get buy price from user
        buy_price = st.sidebar.number_input(
            "Your Buy Price ($)", 
            min_value=0.01, 
            value=float(analyzer.current_price * 0.9),
            step=0.01,
            help="Enter the price at which you bought the stock"
        )
        
        # Calculate sell targets
        price_targets = analyzer.calculate_price_targets("SELL", buy_price)
        
        if price_targets:
            # Display sell recommendation
            if price_targets['profit_percentage'] > 5:
                st.markdown(f'<div class="decision-box buy-signal">✅ RECOMMENDATION: SELL {symbol.upper()} FOR PROFIT</div>', 
                           unsafe_allow_html=True)
            elif price_targets['profit_percentage'] < -10:
                st.markdown(f'<div class="decision-box sell-signal">🛑 RECOMMENDATION: SELL {symbol.upper()} TO CUT LOSSES</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="decision-box neutral-signal">⚠️ RECOMMENDATION: HOLD {symbol.upper()}</div>', 
                           unsafe_allow_html=True)
            
            # Show profit/loss analysis
            st.subheader("💰 Profit/Loss Analysis")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Suggested Sell Price", f"${price_targets['sell_price']:.2f}")
            with col2:
                profit_color = "normal" if price_targets['profit_loss'] >= 0 else "inverse"
                st.metric("Profit/Loss", f"${price_targets['profit_loss']:.2f}", 
                         delta_color=profit_color)
            with col3:
                st.metric("Return %", f"{price_targets['profit_percentage']:.2f}%")
        
        # Technical signal analysis for sell decision
        st.subheader("🔍 Technical Sell Signals")
        sell_score = 0
        for indicator, signal, explanation in signals:
            if signal == "SELL":
                st.error(f"**{indicator}**: {signal} - {explanation}")
                sell_score += 1
            elif signal == "BUY":
                st.success(f"**{indicator}**: {signal} - {explanation}")
                sell_score -= 1
            else:
                st.info(f"**{indicator}**: {signal} - {explanation}")
        
        if sell_score > 0:
            st.warning(f"⚠️ {sell_score} indicators suggest selling")
        elif sell_score < 0:
            st.success(f"✅ {abs(sell_score)} indicators suggest holding")
        else:
            st.info("📊 Mixed signals - consider market conditions")
    
    # Display the chart
    st.subheader("📊 Technical Analysis Chart")
    fig = create_price_chart(df, symbol.upper())
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional market insights
    st.subheader("📈 Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Levels")
        latest = df.iloc[-1]
        st.write(f"**Support Level**: ${latest['Support']:.2f}")
        st.write(f"**Resistance Level**: ${latest['Resistance']:.2f}")
        st.write(f"**RSI**: {latest['RSI']:.1f}")
        
    with col2:
        st.subheader("Risk Assessment")
        volatility = df['Close'].pct_change().std() * np.sqrt(252) * 100
        st.write(f"**Annual Volatility**: {volatility:.1f}%")
        
        if volatility > 30:
            st.error("⚠️ High volatility - Higher risk")
        elif volatility > 20:
            st.warning("📊 Moderate volatility - Medium risk")
        else:
            st.success("✅ Low volatility - Lower risk")
    
    # Disclaimer
    st.markdown("---")
    st.markdown("""
    **⚠️ Important Disclaimer**: This tool is for educational and informational purposes only. 
    It does not constitute financial advice. Always do your own research and consider consulting 
    with a qualified financial advisor before making investment decisions. Trading involves risk, 
    including the potential loss of principal.
    """)

if __name__ == "__main__":
    main()
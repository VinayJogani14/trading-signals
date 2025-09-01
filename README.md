# 🚀 Trading Decision Tool

A powerful **real-time trading decision application** built with **Streamlit** and **Roboquant** that provides data-driven buy/sell recommendations using advanced technical analysis.

---

## 🌟 Features

### 📊 **Real-Time Analysis**
- Live stock data from Yahoo Finance
- Multi-timeframe technical analysis
- Real-time price updates and market data

### 🎯 **Smart Recommendations**
- **BUY/SELL/HOLD** signals with confidence scores
- Multi-indicator consensus approach
- Risk-adjusted entry and exit points

### 📈 **Advanced Technical Indicators**
- **Moving Averages** (SMA 20 & 50) - Trend identification
- **RSI** (Relative Strength Index) - Overbought/oversold conditions
- **MACD** (Moving Average Convergence Divergence) - Momentum analysis
- **Bollinger Bands** - Volatility and support/resistance levels

### 💰 **Price Target Suggestions**
- **Entry Price** recommendations
- **Stop Loss** levels for risk management
- **Take Profit** targets with risk/reward ratios
- **Profit/Loss** calculations for sell decisions

### 📊 **Interactive Visualizations**
- Candlestick charts with technical overlays
- Multi-panel analysis (Price, RSI, MACD)
- Real-time indicator plotting
- Professional trading charts

### 🎨 **User-Friendly Interface**
- Clean, intuitive Streamlit interface
- Responsive design for all screen sizes
- Color-coded signals and recommendations
- Easy-to-understand metrics and explanations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Trading Decision Tool                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌──────────────────┐              │
│  │   Streamlit UI  │    │  Data Sources    │              │
│  │   - Input Forms │    │  - Yahoo Finance │              │
│  │   - Charts      │    │  - Real-time API │              │
│  │   - Metrics     │    └──────────────────┘              │
│  └─────────────────┘                                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              TradingAnalyzer Core Engine                │ │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐  │ │
│  │  │ Data Processing │  │    Technical Indicators     │  │ │
│  │  │ - Price data    │  │ - Moving Averages (SMA)    │  │ │
│  │  │ - Volume data   │  │ - RSI (Momentum)           │  │ │
│  │  │ - Preprocessing │  │ - MACD (Trend)             │  │ │
│  │  └─────────────────┘  │ - Bollinger Bands (Vol)    │  │ │
│  │                       └─────────────────────────────┘  │ │
│  │                                                         │ │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐  │ │
│  │  │ Signal Engine   │  │    Price Targets           │  │ │
│  │  │ - Multi-factor  │  │ - Entry/Exit points        │  │ │
│  │  │ - Consensus     │  │ - Stop Loss calculation    │  │ │
│  │  │ - Risk scoring  │  │ - Take Profit targets      │  │ │
│  │  └─────────────────┘  └─────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   Roboquant Integration                 │ │
│  │  - Algorithmic trading platform                        │ │
│  │  - High-performance backtesting                        │ │
│  │  - Strategy development framework                      │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** installed on your system
- **pip** package manager
- Internet connection for real-time data

### 1. Clone the Repository

```bash
git clone https://github.com/VinayJogani14/trading-signals.git
cd trading-signals
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run trading_decision_app.py
```

### 4. Open in Browser

The app will automatically open in your browser at: `http://localhost:8501`

---

## 📦 Installation

### Option 1: Using pip (Recommended)

```bash
# Create virtual environment (recommended)
python -m venv trading_env
source trading_env/bin/activate  # On Windows: trading_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run trading_decision_app.py
```

### Option 2: Using conda

```bash
# Create conda environment
conda create -n trading_env python=3.11
conda activate trading_env

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run trading_decision_app.py
```

---

## 🎯 Usage Guide

### 📊 **Buy Signal Analysis**

1. **Enter Stock Symbol** (e.g., AAPL, TSLA, MSFT, GOOGL)
2. **Select "Analyze for Buy Signal"**
3. **Review the Results:**
   - ✅ **BUY** - Multiple indicators suggest buying
   - ❌ **DON'T BUY** - Indicators suggest waiting
   - ⚠️ **NEUTRAL** - Mixed signals, use caution

4. **Check Price Targets:**
   - **Entry Price** - Suggested buy price
   - **Stop Loss** - Risk management exit point
   - **Take Profit** - Profit-taking target
   - **Risk/Reward Ratio** - Expected return vs risk

### 💰 **Sell Signal Analysis**

1. **Enter Stock Symbol**
2. **Select "Analyze for Sell Signal"**
3. **Input Your Buy Price**
4. **Review the Results:**
   - ✅ **SELL FOR PROFIT** - Take profits now
   - 🛑 **SELL TO CUT LOSSES** - Minimize further losses
   - ⚠️ **HOLD** - Wait for better conditions

5. **Check Profit Analysis:**
   - **Suggested Sell Price** - Optimal exit price
   - **Profit/Loss** - Expected gain/loss in dollars
   - **Return %** - Percentage return on investment

### 📈 **Understanding the Charts**

- **Candlestick Chart** - Price action over time
- **Moving Averages** - Trend direction (Orange: SMA20, Blue: SMA50)
- **Bollinger Bands** - Volatility and potential reversal points
- **RSI Panel** - Momentum indicator (30-70 normal, <30 oversold, >70 overbought)
- **MACD Panel** - Trend strength and momentum changes

---

## 🔧 Technical Details

### Core Components

#### 1. **TradingAnalyzer Class**
```python
class TradingAnalyzer:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        self.current_price = None
    
    def fetch_data(self, period="6mo")
    def calculate_technical_indicators(self)
    def generate_signals(self)
    def calculate_price_targets(self, action, buy_price=None)
```

#### 2. **Technical Indicators Implementation**
- **SMA (Simple Moving Average)**: `df['Close'].rolling(window=N).mean()`
- **RSI (Relative Strength Index)**: Measures momentum using gain/loss ratio
- **MACD**: Difference between EMA12 and EMA26, with signal line
- **Bollinger Bands**: SMA ± (2 × Standard Deviation)

#### 3. **Signal Generation Logic**
```python
def generate_signals(self):
    signals = []
    
    # Moving Average Signal
    if price > sma20 > sma50:
        signals.append(("Moving Average", "BUY"))
    
    # RSI Signal  
    if rsi < 30:
        signals.append(("RSI", "BUY"))
    elif rsi > 70:
        signals.append(("RSI", "SELL"))
    
    # MACD Signal
    if macd > macd_signal:
        signals.append(("MACD", "BUY"))
    
    # Bollinger Bands Signal
    if price <= bb_lower:
        signals.append(("Bollinger", "BUY"))
    
    # Consensus Decision
    return calculate_consensus(signals)
```

### Data Sources

- **Primary**: Yahoo Finance (`yfinance` library)
- **Backup**: Roboquant data feeds
- **Update Frequency**: Real-time (on page refresh)
- **Historical Data**: 6 months default (configurable)

### Performance Optimizations

- **Caching**: Streamlit's built-in caching for data fetching
- **Lazy Loading**: Data fetched only when needed
- **Efficient Calculations**: Vectorized pandas operations
- **Error Handling**: Graceful fallbacks for network issues

---

## 📊 Supported Assets

### Stock Markets
- **US Stocks** - NYSE, NASDAQ (AAPL, TSLA, MSFT, GOOGL, etc.)
- **International Stocks** - Major global exchanges
- **ETFs** - Exchange-traded funds (SPY, QQQ, VTI, etc.)
- **Indices** - S&P 500, NASDAQ, Dow Jones (^GSPC, ^IXIC, ^DJI)

### Cryptocurrencies
- **Major Coins** - Bitcoin, Ethereum (BTC-USD, ETH-USD)
- **Popular Altcoins** - Available through Yahoo Finance

### Forex (Limited Support)
- **Major Pairs** - EUR/USD, GBP/USD (EURUSD=X, GBPUSD=X)

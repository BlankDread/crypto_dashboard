import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time
import numpy as np

st.set_page_config(page_title="🧬 Ultra Crypto Dashboard", layout="wide")

# === 🌈 FULL Futuristic CSS ===
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top left, #0d1117, #080b10);
}
h1.title {
    font-size: 3em;
    background: linear-gradient(90deg, #0affef, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0;
    animation: glow 4s ease-in-out infinite;
    font-family: 'Trebuchet MS', sans-serif;
}
@keyframes glow {
    0% { text-shadow: 0 0 5px #0affef44; }
    50% { text-shadow: 0 0 25px #8b5cf6; }
    100% { text-shadow: 0 0 5px #0affef44; }
}
.metric-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid #2c2c2e;
    border-radius: 16px;
    padding: 1.5em;
    backdrop-filter: blur(6px);
    box-shadow: 0 0 15px rgba(10, 255, 239, 0.15);
    color: #c9d1d9;
    font-family: 'Segoe UI', sans-serif;
}
.metric-card h3 {
    margin: 0;
    font-size: 1.2em;
    background: linear-gradient(to right, #ff00cc, #3333ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card p {
    font-size: 2em;
    margin: 0.2em 0 0;
    background: linear-gradient(to right, #0affef, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
/* Gradient tab labels with readable text */
.stTabs [data-baseweb="tab"]:nth-child(1) {
    background: linear-gradient(to right, #8b5cf6, #0affef);
    color: white;
}
.stTabs [data-baseweb="tab"]:nth-child(2) {
    background: linear-gradient(to right, #ff00cc, #3333ff);
    color: white;
}
.stTabs [data-baseweb="tab"]:nth-child(3) {
    background: linear-gradient(to right, #00ff88, #00c6ff);
    color: white;
}
hr {
    border: none;
    border-top: 1px solid #222;
    margin: 2em 0 1em;
}
</style>
""", unsafe_allow_html=True)

# === 🧬 Title ===
st.markdown("<h1 class='title'>🧬 Ultra Crypto Dashboard</h1>", unsafe_allow_html=True)

# === Sidebar Filters ===
crypto_list = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'cardano']
vs_currency = 'usd'
selected = st.sidebar.selectbox("💳 Choose coin", crypto_list)
days = st.sidebar.slider("🗓️ History (days)", 1, 365, 90)

# === Tabs ===
tabs = st.tabs(["📈 Price Chart", "🔮 Coin Info", "🧠 Forecast"])

@st.cache_data(ttl=600)
def get_data(coin, days):
    time.sleep(1)
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency={vs_currency}&days={days}"
    r = requests.get(url)
    if r.status_code != 200:
        return pd.DataFrame()
    data = r.json()['prices']
    df = pd.DataFrame(data, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

@st.cache_data(ttl=300)
def get_info(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# === Tab 1: Price Chart ===
with tabs[0]:
    df = get_data(selected, days)
    if not df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['price'], mode='lines',
                                 line=dict(color='#8b5cf6', width=3), name="Price"))
        fig.update_layout(
            paper_bgcolor='#0d1117',
            plot_bgcolor='#0d1117',
            font=dict(color='#c9d1d9'),
            title=f"📈 {selected.capitalize()} Price for {days} days",
            title_x=0.5,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(title='Date'),
            yaxis=dict(title='Price (USD)')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ Failed to load chart data")

# === Tab 2: Coin Info ===
with tabs[1]:
    info = get_info(selected)
    if info:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(info['image']['large'], width=80)
        with col2:
            st.markdown(f"<div class='metric-card'><h3>🔹 Name:</h3><p>{info['name']} ({info['symbol'].upper()})</p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-card'><h3>🌐 Website:</h3><p><a href='{info['links']['homepage'][0]}' target='_blank'>{info['links']['homepage'][0]}</a></p></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-card'><h3>🧾 Description:</h3><p>{info['description']['en'][:300]}...</p></div>", unsafe_allow_html=True)
    else:
        st.error("❌ Failed to load coin info")

# === Tab 3: Forecast (simple linear model) ===
with tabs[2]:
    st.subheader("🧠 Price Forecast")
    df = get_data(selected, days)
    if not df.empty:
        df['days'] = (df['date'] - df['date'].min()).dt.days
        X = df['days'].values.reshape(-1, 1)
        y = df['price'].values
        coef = np.polyfit(df['days'], df['price'], 1)
        forecast = coef[0] * df['days'] + coef[1]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['price'], mode='lines', name='Actual'))
        fig.add_trace(go.Scatter(x=df['date'], y=forecast, mode='lines', name='Forecast', line=dict(dash='dash')))
        fig.update_layout(
            title="🔮 Linear Forecast Based on History",
            paper_bgcolor='#0d1117',
            plot_bgcolor='#0d1117',
            font=dict(color='#c9d1d9'),
            title_x=0.5,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Not enough data for forecast.")

# === Bottom Showcase: Join the Future ===
st.markdown("""
<hr>
<h2 style='text-align:center; font-size:2.5em; background: linear-gradient(to right, #ff00cc, #3333ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🚀 Join the Future of Crypto</h2>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image("assets/bitcoin.png", width=120)
    st.markdown("<div class='metric-card'><h3>Bitcoin</h3><p>The original pioneer</p><a href='https://bitcoin.org' target='_blank'>🌐 Explore</a></div>", unsafe_allow_html=True)

with col2:
    st.image("assets/ethereum.png", width=120)
    st.markdown("<div class='metric-card'><h3>Ethereum</h3><p>Smart contract giant</p><a href='https://ethereum.org' target='_blank'>🌐 Explore</a></div>", unsafe_allow_html=True)

with col3:
    st.image("assets/cardano.png", width=120)
    st.markdown("<div class='metric-card'><h3>Cardano</h3><p>Sustainable blockchain</p><a href='https://cardano.org' target='_blank'>🌐 Explore</a></div>", unsafe_allow_html=True)
# === Footer ===
st.markdown("""
<hr>
<div style='text-align:center; font-size:0.85em; color:#666'>
Made with ✨ using Streamlit & CoinGecko API • 2025
</div>
""", unsafe_allow_html=True)

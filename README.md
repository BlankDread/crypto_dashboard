# 🧬 Ultra Crypto Dashboard

**Live futuristic dashboard for monitoring and forecasting cryptocurrency trends — with real-time data, stylish visuals, and analytics.**

![screenshot](assets/preview.png)

---

## 🚀 Features

- 📈 **Live price charts** with interactive Plotly graphs  
- 💹 **Forecasting** (linear trend model) based on historical price data  
- 🌐 **Crypto info cards** with real descriptions, logos, and links  
- 🎨 **Futuristic gradient UI** inspired by blockchain design trends  
- 📡 **Powered by CoinGecko API** (no API key required)  
- 🖼️ Custom token visuals (Bitcoin, Ethereum, Cardano)

---

## 🧩 Tech Stack

- [Streamlit](https://streamlit.io/) — fast and interactive web apps for Python  
- [Plotly](https://plotly.com/python/) — data visualizations  
- [CoinGecko API](https://www.coingecko.com/en/api/documentation) — live crypto data  
- [Pandas, NumPy, Requests] — data processing and HTTP requests  
- Custom CSS for a sleek, immersive UI 💫

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/ultra-crypto-dashboard.git
cd ultra-crypto-dashboard
pip install -r requirements.txt
streamlit run crypto_dashboard.py

⚙️ Usage
Select the coin from the sidebar
Choose historical range (1–365 days)

View:
📊 Price charts
📚 Coin info
🔮 Forecasts

🖼️ Assets
Icons and coin artwork located in assets/ folder:
bitcoin.png
ethereum.png
cardano.png

Designed with a futuristic cyber aesthetic ⚡

📌 To-Do
 Integrate news or tweets for selected coin
 Add AI/ML-based forecasting models (e.g., Prophet)
 Dark/Light theme toggle
 Crypto portfolio simulation

🧠 Credits
👨‍💻 Built by BlankDread
🎨 Visuals by AI + design direction
🛰️ Data from CoinGecko API

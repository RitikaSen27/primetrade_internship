# 📊 PrimeTrade.ai Internship Assignment

## 🧾 Project Overview
This project analyzes trader behavior and performance under different market sentiment conditions—**Fear**, **Greed**, and **Neutral**—by combining trading data with the **CNN Fear & Greed Index**.

The objective is to identify patterns in trading activity, evaluate performance across sentiments, and derive actionable trading strategies.

---

## 👩‍💻 Author
**Ritika Sen**

---

## 📁 Repository Structure

```
primetrade_internship/
├── data/
│   ├── fear_greed_index.csv
│   └── historical_data.csv
│
├── PART_A/
│   ├── part_a.py
│   ├── aligned_data.csv
│   └── trader_metrics.csv
│
├── PARTB_Q1/
│   ├── partb_q1.py
│   ├── analysis answer.txt
│   └── performance_by_sentiment.png
│
├── PARTB_Q2/
│   ├── partb_q2.py
│   ├── analysis answer.txt
│   └── behavior_by_sentiment.png
│
├── PARTB_Q3/
│   ├── partb_q3.py
│   └── segment_analysis.png
│
├── PARTB__Analysis_Insights.txt
├── PART_C_strategies.txt
├── README.md
└── requirements.txt
```

---

## 📥 Data Sources

- **Fear & Greed Index**  
  https://drive.google.com/file/d/1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf/view  

- **Trading History**  
  https://drive.google.com/file/d/1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs/view  

---

## ⚙️ Setup Instructions

### 🔹 Prerequisites
- Python 3.8 or higher

### 🔹 Installation

1. Clone the repository:
```bash
git clone https://github.com/RitikaSen27/primetrade_internship.git
cd primetrade_internship
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure the dataset files are placed inside the `data/` folder.

---

## ▶️ How to Run

### 🅰️ Part A: Data Preparation
```bash
python "PART_A/part_a.py"
```

**Output:**
- `aligned_data.csv`
- `trader_metrics.csv`

---

### 🅱️ Part B: Analysis

#### Q1 – Performance by Sentiment
```bash
python "PARTB_Q1/partb_q1.py"
```
- Output: `performance_by_sentiment.png`
- Analysis: `analysis answer.txt`

---

#### Q2 – Behavioral Metrics
```bash
python "PARTB_Q2/partb_q2.py"
```
- Output: `behavior_by_sentiment.png`
- Analysis: `analysis answer.txt`

---

#### Q3 – Trader Segmentation
```bash
python "PARTB_Q3/partb_q3.py"
```
- Output: `segment_analysis.png`

---

### 🅲 Part C: Strategy Insights
- File: `PART_C strategies.txt`

---

## 📈 Key Findings

### 🔍 Insight 1: Overtrading on Fear Days
- Fear days have significantly higher trading activity compared to Greed days  
- However, profit increase is not proportional → reduced efficiency per trade  

---

### 🔍 Insight 2: Higher Win Rate During Fear
- Traders perform better during Fear conditions compared to Greed and Neutral  

---

### 🔍 Insight 3: Frequent Traders Perform Better
- Frequent traders significantly outperform infrequent traders during Fear days  

---

## 💡 Strategy Recommendations

### 📌 Strategy 1: Position Sizing Adjustment
- Increase position size during Fear conditions for experienced traders  
- Maintain or reduce for less frequent traders  

---

### 📌 Strategy 2: Trade Limiting
- Limit excessive trading during high-volatility (Fear) periods  
- Helps avoid diminishing returns  

---

## 📊 Clustering Insights (Trader Archetypes)

### 🧩 Identified Trader Segments

| Archetype | Trades/Day | Position Size | Win Rate | Daily PnL | Profile |
|----------|------------|---------------|----------|-----------|--------|
| Moderate, Balanced | 11,995 | $1,789 | 58.6% | $374,388 | ⭐ Best performers – high frequency, small size, highest win rate |
| High Volume, Low Win Rate | 1,909 | $15,578 | 21.6% | $800,115 | 💰 Most profitable despite low win rate – large positions |
| Aggressive, Large Size | 2,433 | $19,176 | 41.5% | $70,853 | 🎯 Large positions, moderate win rate |
| Conservative, High Win Rate | 1,422 | $3,589 | 37.6% | $63,412 | 🛡️ Cautious approach with smaller positions |

---

### 🔍 Key Insights

- **High Volume, Low Win Rate traders generate the highest profits ($800K)**  
  Despite a low win rate of **21.6%**, profitability comes from **very large position sizes**

- **Moderate, Balanced traders achieve the highest win rate (58.6%)**  
  Indicates **strong trade selection and consistency**

- **Conservative traders maintain profitability with lower risk**  
  Smaller positions but stable returns suggest a **risk-controlled strategy**

---

### 💡 Interpretation

These clusters highlight a key trade-off in trading strategies:

- Profitability is **not solely dependent on win rate**
- **Position sizing plays a crucial role** in overall returns
- Different strategies can succeed depending on **risk appetite and execution style**

  
## 📦 Requirements

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

---

## 📜 License
This project is intended for internship assignment purposes only.


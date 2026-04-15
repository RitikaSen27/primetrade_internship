# PrimeTrade.ai Internship Assignment - Complete Write-Up

**Author:** Ritika Sen

---

## Methodology

Loaded 2,644 fear-greed records and 211,224 trades. Converted Unix timestamps (milliseconds) to datetime and aligned datasets by date. Created key metrics: daily PnL, win rate, average trade size, trade frequency. Segmented traders into Frequent/Infrequent and Consistent/Inconsistent winners.

---

## Key Insights

**Insight 1: Fear days drive higher profits**
- Fear days: $6.7M average PnL vs Greed days: $1.06M (6.3x higher)
- Win rate: 41.6% on Fear vs 37.4% on Greed
- Traders are more active AND more profitable on Fear days

**Insight 2: Behavior changes dramatically on Fear days**
- Trade frequency: 4,183 trades/day on Fear vs 1,134 on Greed (269% increase)
- Position sizes: Slightly larger on Fear ($5,927 vs $5,839)
- Win rate: Peaks on Fear (41.6%), lowest on Neutral (26.1%)

**Insight 3: Frequent traders excel during Fear**
- Frequent traders: $329,421 PnL on Fear days
- Infrequent traders: $89,324 PnL on Fear days
- Frequent traders outperform by 269% during fearful sentiment

---

## Strategy Recommendations

**Strategy 1:** During Fear days, frequent traders increase position size by 20%; infrequent traders maintain or reduce.

**Strategy 2:** Cap daily trades at 3,000 during Fear days to prevent diminishing returns (269% more trades but only 110% higher PnL).

---

## Bonus Results

**Predictive Model:** 67% accuracy predicting next-day profitability. Key drivers: trade size (32%), win rate (29%), frequency (27%).

**Trader Archetypes:** 4 clusters identified - Moderate Balanced (58.6% win rate), High Volume Low Win Rate ($800K PnL), Aggressive Large Size, Conservative High Win Rate.

---

## Files

| File | Purpose |
|------|---------|
| `PART_A.py` | Data preparation |
| `PART_B.py` | Analysis & charts |
| `PART_C_strategies.py` | Strategy rules |
| `predictive_model.py` | Profitability prediction |
| `clustering.py` | Trader archetypes |

---

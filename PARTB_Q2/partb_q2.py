"""
Part B - Question 2: Do traders change behavior based on sentiment?
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create outputs folder
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# Load trader metrics
traders = pd.read_csv('trader_metrics.csv')

# Behavior by sentiment
behavior = traders.groupby('classification').agg({
    'num_trades': 'mean',
    'avg_trade_size_usd': 'mean',
    'win_rate': 'mean'
}).round(2)

print("="*60)
print("Trader Behavior by Sentiment")
print("="*60)
print(behavior)

# Create 3 charts in a row (1x3 layout)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Chart 1: Trade Frequency
sns.barplot(data=traders, x='classification', y='num_trades', ax=axes[0],
            order=['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed'])
axes[0].set_title('Trade Frequency by Sentiment')
axes[0].set_ylabel('Avg Trades per Day')
axes[0].tick_params(axis='x', rotation=45)

# Chart 2: Position Size
sns.barplot(data=traders, x='classification', y='avg_trade_size_usd', ax=axes[1],
            order=['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed'])
axes[1].set_title('Position Size by Sentiment')
axes[1].set_ylabel('Avg Size (USD)')
axes[1].tick_params(axis='x', rotation=45)

# Chart 3: Win Rate
sns.barplot(data=traders, x='classification', y='win_rate', ax=axes[2],
            order=['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed'])
axes[2].set_title('Win Rate by Sentiment')
axes[2].set_ylabel('Win Rate (%)')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('outputs/behavior_by_sentiment.png', dpi=150)
plt.show()

print("\n✓ Chart saved to 'outputs/behavior_by_sentiment.png'")
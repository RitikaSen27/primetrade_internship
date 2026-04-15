"""
Part B - Question 1: Performance on Fear vs Greed Days
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create outputs folder if it doesn't exist
if not os.path.exists('outputs'):
    os.makedirs('outputs')
# Load the aligned data
df = pd.read_csv('aligned_data.csv')
df['date_only'] = pd.to_datetime(df['date_only'])

# Calculate drawdown proxy (max decline from peak)
df['cumulative_pnl'] = df['total_pnl'].cumsum()
df['peak'] = df['cumulative_pnl'].cummax()
df['drawdown'] = (df['peak'] - df['cumulative_pnl']) / df['peak'] * 100

# Group by sentiment
performance_by_sentiment = df.groupby('classification').agg({
    'total_pnl': ['mean', 'median', 'std'],
    'total_trades': 'mean',
    'drawdown': 'max'
}).round(2)

print("="*60)
print("Performance by Sentiment")
print("="*60)
print(performance_by_sentiment)

# Create bar chart
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Chart 1: Average PnL by Sentiment
avg_pnl = df.groupby('classification')['total_pnl'].mean().sort_values()
axes[0].bar(avg_pnl.index, avg_pnl.values, color=['red', 'gray', 'green'])
axes[0].set_title('Average Daily PnL by Sentiment')
axes[0].set_ylabel('Average PnL ($)')
axes[0].tick_params(axis='x', rotation=45)

# Chart 2: Average Trades by Sentiment
avg_trades = df.groupby('classification')['total_trades'].mean()
axes[1].bar(avg_trades.index, avg_trades.values, color=['red', 'gray', 'green'])
axes[1].set_title('Average Daily Trades by Sentiment')
axes[1].set_ylabel('Number of Trades')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('outputs/performance_by_sentiment.png', dpi=150)
plt.show()
"""
Part B - Question 3: Segment Analysis
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create outputs folder
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# Load trader metrics
traders = pd.read_csv('trader_metrics.csv')

print("Available columns:", traders.columns.tolist())

# ============================================
# SEGMENT 1: Frequent vs Infrequent Traders
# ============================================

# Calculate average trades per trader
trader_trades = traders.groupby('trader_id')['num_trades'].mean().reset_index()
median_trades = trader_trades['num_trades'].median()
trader_trades['freq_segment'] = np.where(trader_trades['num_trades'] > median_trades, 'Frequent', 'Infrequent')

# Merge back to traders
traders = traders.merge(trader_trades[['trader_id', 'freq_segment']], on='trader_id', how='left')

print("\n" + "="*60)
print("Segment 1: Frequent vs Infrequent Traders")
print("="*60)
freq_results = traders.groupby(['freq_segment', 'classification'])['daily_pnl'].mean().unstack()
print(freq_results.round(2))

# ============================================
# SEGMENT 2: Consistent Winners vs Inconsistent
# ============================================

# Calculate win rate per trader (average across all days)
trader_winrate = traders.groupby('trader_id')['win_rate'].mean().reset_index()
trader_winrate['winner_segment'] = np.where(trader_winrate['win_rate'] > 50, 'Consistent Winner', 'Inconsistent')

# Merge back to traders
traders = traders.merge(trader_winrate[['trader_id', 'winner_segment']], on='trader_id', how='left')

print("\n" + "="*60)
print("Segment 2: Consistent Winners vs Inconsistent")
print("="*60)

# Check if winner_segment exists
if 'winner_segment' in traders.columns:
    winner_results = traders.groupby(['winner_segment', 'classification'])['win_rate'].mean().unstack()
    print(winner_results.round(2))
else:
    print("Error: winner_segment column not created")
    # Alternative: create on the fly
    traders['winner_segment'] = np.where(traders['win_rate'] > 50, 'Consistent Winner', 'Inconsistent')
    winner_results = traders.groupby(['winner_segment', 'classification'])['win_rate'].mean().unstack()
    print(winner_results.round(2))

# ============================================
# CREATE CHARTS
# ============================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Frequent vs Infrequent - PnL by Sentiment
freq_pnl = traders.groupby(['freq_segment', 'classification'])['daily_pnl'].mean().unstack()
freq_pnl.plot(kind='bar', ax=axes[0])
axes[0].set_title('Daily PnL: Frequent vs Infrequent Traders', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Avg Daily PnL (USD)')
axes[0].set_xlabel('Trader Segment')
axes[0].legend(title='Sentiment')
axes[0].tick_params(axis='x', rotation=0)

# Chart 2: Winners vs Inconsistent - Win Rate by Sentiment
winner_rate = traders.groupby(['winner_segment', 'classification'])['win_rate'].mean().unstack()
winner_rate.plot(kind='bar', ax=axes[1])
axes[1].set_title('Win Rate: Consistent vs Inconsistent Winners', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Win Rate (%)')
axes[1].set_xlabel('Trader Segment')
axes[1].legend(title='Sentiment')
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('outputs/segment_analysis.png', dpi=150)
plt.close()

print("\n" + "="*60)
print("INSIGHTS FROM SEGMENT ANALYSIS")
print("="*60)

# Insight 1: Frequent vs Infrequent on Greed days
freq_greed = freq_results.loc['Frequent', 'Greed'] if 'Greed' in freq_results.columns else 0
infreq_greed = freq_results.loc['Infrequent', 'Greed'] if 'Greed' in freq_results.columns else 0
print(f"\n1. On Greed days, Frequent traders make ${freq_greed:,.0f} vs Infrequent traders make ${infreq_greed:,.0f}")

# Insight 2: Frequent vs Infrequent on Fear days
freq_fear = freq_results.loc['Frequent', 'Fear'] if 'Fear' in freq_results.columns else 0
infreq_fear = freq_results.loc['Infrequent', 'Fear'] if 'Fear' in freq_results.columns else 0
print(f"\n2. On Fear days, Frequent traders make ${freq_fear:,.0f} vs Infrequent traders make ${infreq_fear:,.0f}")

# Insight 3: Which segment performs better?
if freq_greed > infreq_greed:
    print(f"\n3. Frequent traders outperform infrequent traders by ${freq_greed - infreq_greed:,.0f} on Greed days")
else:
    print(f"\n3. Infrequent traders outperform frequent traders by ${infreq_greed - freq_greed:,.0f} on Greed days")

print("\n✓ Chart saved to 'outputs/segment_analysis.png'")
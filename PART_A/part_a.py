"""
PART A: DATA PREPARATION - COMPLETE WORKING VERSION (CSV only)
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("PART A: DATA PREPARATION")
print("="*70)

# ============================================
# STEP 1: LOAD DATASETS
# ============================================
print("\n[STEP 1] Loading datasets...")

fear_greed = pd.read_csv('fear_greed_index.csv')
trades = pd.read_csv('historical_data.csv')

print(f"  ✓ Fear & Greed: {fear_greed.shape[0]:,} rows, {fear_greed.shape[1]} columns")
print(f"  ✓ Trades: {trades.shape[0]:,} rows, {trades.shape[1]} columns")

# ============================================
# STEP 2: DOCUMENT ROWS/COLUMNS & MISSING VALUES
# ============================================
print("\n[STEP 2] Data quality inspection...")

print(f"\n  --- FEAR & GREED DATASET ---")
print(f"  Rows: {fear_greed.shape[0]:,}")
print(f"  Columns: {fear_greed.shape[1]}")
print(f"  Column names: {fear_greed.columns.tolist()}")
print(f"  Missing values: {fear_greed.isnull().sum().sum()}")
print(f"  Duplicates: {fear_greed.duplicated().sum()}")

print(f"\n  --- TRADES DATASET ---")
print(f"  Rows: {trades.shape[0]:,}")
print(f"  Columns: {trades.shape[1]}")
print(f"  Column names: {trades.columns.tolist()}")
print(f"  Missing values: {trades.isnull().sum().sum()}")
print(f"  Duplicates: {trades.duplicated().sum()}")

# Handle missing values
if trades.isnull().sum().sum() > 0:
    print("\n  Handling missing values...")
    numeric_cols = trades.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if trades[col].isnull().sum() > 0:
            trades[col] = trades[col].fillna(trades[col].median())
    print("  ✓ Missing values filled")

# ============================================
# STEP 3: CONVERT TIMESTAMPS
# ============================================
print("\n[STEP 3] Converting timestamps...")

# Fear-Greed dataset
fear_greed['date'] = pd.to_datetime(fear_greed['date'])
fear_greed['date_only'] = fear_greed['date'].dt.date
print("  ✓ Fear-Greed dates converted")

# Trades dataset - auto-detect timestamp format
if 'Timestamp' in trades.columns:
    test_val = trades['Timestamp'].iloc[0]
    
    if test_val > 10**15:
        print("  Detected: Nanoseconds format")
        trades['datetime'] = pd.to_datetime(trades['Timestamp'], unit='ns')
    elif test_val > 10**12:
        print("  Detected: Milliseconds format")
        trades['datetime'] = pd.to_datetime(trades['Timestamp'], unit='ms')
    elif test_val > 10**9:
        print("  Detected: Seconds format")
        trades['datetime'] = pd.to_datetime(trades['Timestamp'], unit='s')
    else:
        trades['datetime'] = pd.to_datetime(trades['Timestamp'])
    
    trades['date_only'] = trades['datetime'].dt.date
    print("  ✓ Trades dates converted")

print(f"  ✓ Trades date range: {trades['date_only'].min()} to {trades['date_only'].max()}")
print(f"  ✓ Total unique dates: {trades['date_only'].nunique():,}")

# ============================================
# STEP 4: ALIGN DATASETS BY DATE
# ============================================
print("\n[STEP 4] Aligning datasets by date...")

# Aggregate trades to daily level
daily_trades = trades.groupby('date_only').agg({
    'Trade ID': 'count',
    'Closed PnL': 'sum',
    'Size USD': 'sum',
    'Account': 'nunique'
}).reset_index()

daily_trades.rename(columns={
    'Trade ID': 'total_trades',
    'Closed PnL': 'total_pnl',
    'Size USD': 'total_volume_usd',
    'Account': 'active_traders'
}, inplace=True)

print(f"  ✓ Daily aggregation: {len(daily_trades)} days")

# Merge with fear-greed
aligned_data = pd.merge(
    daily_trades,
    fear_greed[['date_only', 'value', 'classification']],
    on='date_only',
    how='inner'
)
aligned_data = aligned_data.sort_values('date_only').reset_index(drop=True)

print(f"  ✓ Aligned data: {len(aligned_data)} days")
print(f"  ✓ Date range: {aligned_data['date_only'].min()} to {aligned_data['date_only'].max()}")

# ============================================
# STEP 5: CREATE PER-TRADER METRICS
# ============================================
print("\n[STEP 5] Creating per-trader metrics...")

trades['trader_id'] = trades['Account']

trader_metrics = trades.groupby(['date_only', 'trader_id']).agg({
    'Trade ID': 'count',
    'Closed PnL': 'sum',
    'Size USD': 'mean'
}).reset_index()

trader_metrics.rename(columns={
    'Trade ID': 'num_trades',
    'Closed PnL': 'daily_pnl',
    'Size USD': 'avg_trade_size_usd'
}, inplace=True)

# Calculate win rate
wins = trades[trades['Closed PnL'] > 0].groupby(['date_only', 'trader_id']).size().reset_index(name='wins')
total = trades.groupby(['date_only', 'trader_id']).size().reset_index(name='total_trades')
win_rate_data = wins.merge(total, on=['date_only', 'trader_id'], how='right').fillna(0)
win_rate_data['win_rate'] = (win_rate_data['wins'] / win_rate_data['total_trades']) * 100
trader_metrics = trader_metrics.merge(
    win_rate_data[['date_only', 'trader_id', 'win_rate']], 
    on=['date_only', 'trader_id'], 
    how='left'
)

# Calculate long/short ratio if Side exists
if 'Side' in trades.columns:
    long_trades = trades[trades['Side'] == 'Long'].groupby(['date_only', 'trader_id']).size().reset_index(name='longs')
    all_trades = trades.groupby(['date_only', 'trader_id']).size().reset_index(name='all_trades')
    ratio_data = long_trades.merge(all_trades, on=['date_only', 'trader_id'], how='right').fillna(0)
    ratio_data['long_ratio'] = ratio_data['longs'] / ratio_data['all_trades']
    ratio_data['long_short_ratio'] = ratio_data['long_ratio'] / (1 - ratio_data['long_ratio'] + 0.001)
    trader_metrics = trader_metrics.merge(
        ratio_data[['date_only', 'trader_id', 'long_ratio', 'long_short_ratio']],
        on=['date_only', 'trader_id'],
        how='left'
    )
    print("  ✓ Long/short ratio added")

# Add sentiment
trader_metrics = trader_metrics.merge(
    fear_greed[['date_only', 'value', 'classification']],
    on='date_only',
    how='left'
)

print(f"  ✓ Trader metrics: {trader_metrics.shape[0]:,} records")
print(f"  ✓ Unique traders: {trader_metrics['trader_id'].nunique():,}")

# ============================================
# STEP 6: CREATE TRADER SEGMENTS
# ============================================
print("\n[STEP 6] Creating trader segments...")

# Frequent vs Infrequent traders
trader_frequency = trades.groupby('trader_id').size().reset_index(name='total_trades')
median_freq = trader_frequency['total_trades'].median()
trader_frequency['frequency_segment'] = np.where(
    trader_frequency['total_trades'] > median_freq, 'Frequent', 'Infrequent'
)
trader_metrics = trader_metrics.merge(
    trader_frequency[['trader_id', 'frequency_segment']], on='trader_id', how='left'
)

# Consistent winners vs Inconsistent
trader_win_rate = trader_metrics.groupby('trader_id')['win_rate'].mean().reset_index()
trader_win_rate['winner_segment'] = np.where(
    trader_win_rate['win_rate'] > 50, 'Consistent Winner', 'Inconsistent'
)
trader_metrics = trader_metrics.merge(
    trader_win_rate[['trader_id', 'winner_segment']], on='trader_id', how='left'
)

print("  ✓ Segments created: Frequency & Winner status")

# ============================================
# STEP 7: SAVE ALL FILES (CSV ONLY)
# ============================================
print("\n[STEP 7] Saving processed data...")

aligned_data.to_csv('aligned_data.csv', index=False)
trader_metrics.to_csv('trader_metrics.csv', index=False)
fear_greed.to_csv('fear_greed_cleaned.csv', index=False)
trades.to_csv('trades_cleaned.csv', index=False)

print("  ✓ Saved:")
print("     - aligned_data.csv (daily data with sentiment)")
print("     - trader_metrics.csv (per-trader daily metrics)")
print("     - fear_greed_cleaned.csv")
print("     - trades_cleaned.csv")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "="*70)
print("PART A COMPLETED SUCCESSFULLY ✓")
print("="*70)

print("\n📊 SUMMARY:")
print(f"   • Fear-Greed records: {fear_greed.shape[0]:,}")
print(f"   • Trades processed: {trades.shape[0]:,}")
print(f"   • Unique traders: {trader_metrics['trader_id'].nunique():,}")
print(f"   • Aligned days: {len(aligned_data)}")
print(f"   • Date range: {aligned_data['date_only'].min()} to {aligned_data['date_only'].max()}")

print("\n📈 KEY METRICS CREATED:")
for col in ['daily_pnl', 'win_rate', 'avg_trade_size_usd', 'num_trades', 'classification']:
    if col in trader_metrics.columns:
        print(f"   ✓ {col}")

print("\n👥 TRADER SEGMENTS:")
print(f"   ✓ Frequent/Infrequent traders")
print(f"   ✓ Consistent/Inconsistent winners")

print("\n💾 Open files in Excel:")
print("   • Double-click aligned_data.csv")
print("   • Double-click trader_metrics.csv")

print("\n" + "="*70)
print("✅ READY FOR PART B - ANALYSIS")
print("="*70)

# Show sample
print("\n📋 Sample of aligned data:")
print(aligned_data[['date_only', 'total_trades', 'total_pnl', 'classification']].head(10))

print("\n📊 Sentiment distribution:")
print(aligned_data['classification'].value_counts())
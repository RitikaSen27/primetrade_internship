"""
BONUS 2: Cluster traders into behavioral archetypes
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load data
traders = pd.read_csv('trader_metrics.csv')

# Aggregate trader behavior
trader_profile = traders.groupby('trader_id').agg({
    'num_trades': 'mean',
    'avg_trade_size_usd': 'mean',
    'win_rate': 'mean',
    'daily_pnl': 'mean'
}).reset_index()

# Normalize features
features = ['num_trades', 'avg_trade_size_usd', 'win_rate', 'daily_pnl']
scaler = StandardScaler()
scaled_features = scaler.fit_transform(trader_profile[features])

# Find optimal clusters (Elbow method)
inertias = []
for k in range(2, 8):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled_features)
    inertias.append(kmeans.inertia_)

# Use 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
trader_profile['cluster'] = kmeans.fit_predict(scaled_features)

# Name the clusters
cluster_names = {
    0: 'High Volume, Low Win Rate',
    1: 'Conservative, High Win Rate',
    2: 'Aggressive, Large Size',
    3: 'Moderate, Balanced'
}
trader_profile['archetype'] = trader_profile['cluster'].map(cluster_names)

print("="*60)
print("BONUS 2: Trader Archetypes")
print("="*60)
print(trader_profile.groupby('archetype')[features].mean().round(2))

# Visualize
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(trader_profile['num_trades'], trader_profile['win_rate'], 
                     c=trader_profile['cluster'], cmap='viridis', s=100, alpha=0.6)
ax.set_xlabel('Avg Trades per Day')
ax.set_ylabel('Win Rate (%)')
ax.set_title('Trader Behavioral Archetypes')
for i, row in trader_profile.iterrows():
    ax.annotate(row['archetype'].split(',')[0], (row['num_trades'], row['win_rate']), fontsize=8)
plt.tight_layout()
plt.savefig('outputs/trader_archetypes.png', dpi=150)
plt.close()
print("\n✓ Chart saved: outputs/trader_archetypes.png")
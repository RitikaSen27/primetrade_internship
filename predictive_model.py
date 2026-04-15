"""
BONUS 1: Predict next-day trader profitability
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load data
traders = pd.read_csv('trader_metrics.csv')
traders['date_only'] = pd.to_datetime(traders['date_only'])

# Create features
traders = traders.sort_values(['trader_id', 'date_only'])

# Create next-day profitability (1 if profit > 0, else 0)
traders['next_day_profit'] = traders.groupby('trader_id')['daily_pnl'].shift(-1)
traders['next_day_profit_bucket'] = (traders['next_day_profit'] > 0).astype(int)

# Features: sentiment + behavior
features = ['num_trades', 'avg_trade_size_usd', 'win_rate', 'value']
target = 'next_day_profit_bucket'

# Remove NaN
df_model = traders[features + [target]].dropna()

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    df_model[features], df_model[target], test_size=0.3, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("="*60)
print("BONUS 1: Predictive Model")
print("="*60)
print(f"Model: Random Forest Classifier")
print(f"Accuracy: {accuracy:.2%}")
print(f"\nFeature Importance:")
for feature, importance in zip(features, model.feature_importances_):
    print(f"  {feature}: {importance:.3f}")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Loss', 'Profit']))
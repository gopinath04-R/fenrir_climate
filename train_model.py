import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("Loading merged data...")
df = pd.read_csv('merged_climate_data.csv')
df['date'] = pd.to_datetime(df['date'])

print(f"Total rows: {len(df)}")

# Split: train on 2021-2024, test on 2025 (real backtesting!)
train_df = df[df['year'] <= 2024]
test_df = df[df['year'] == 2025]

print(f"Training rows (2021-2024): {len(train_df)}")
print(f"Testing rows (2025): {len(test_df)}")

# Sample for faster training (full data is huge)
train_sample = train_df.sample(n=min(300000, len(train_df)), random_state=42)
test_sample = test_df.sample(n=min(50000, len(test_df)), random_state=42)

features = ['lat', 'lon', 'tmax', 'tmin', 'month', 'day_of_year']
X_train = train_sample[features]
y_train = train_sample['rain_occurred']
X_test = test_sample[features]
y_test = test_sample['rain_occurred']

print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

print("Predicting on 2025 test data...")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n=== MODEL ACCURACY ON 2025 DATA: {accuracy*100:.2f}% ===\n")
print(classification_report(y_test, y_pred, target_names=['No Rain', 'Rain']))

# Feature importance
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nFeature Importance:")
print(importance)

# Save model
joblib.dump(model, 'rain_model.pkl')
print("\nModel saved as rain_model.pkl")
print("DONE!")
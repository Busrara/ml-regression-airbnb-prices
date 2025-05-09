# -*- coding: utf-8 -*-
"""Welcome To Colab

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/notebooks/intro.ipynb
"""

import pandas as pd
import numpy as np
import zipfile
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Path for the zip file
zip_file = "/content/AB_NYC_2019.csv.zip"
#Exact name of the file in zip
csv_filename = "AB_NYC_2019.csv"

# Read the zip file
with zipfile.ZipFile(zip_file_path) as z:
  with z.open(csv_filename) as f:
    df = pd.read_csv(f)

print(df.head())
print(df.info())

#Check the missing values
print("\nMissing values:\n", df.isnull().sum())

#Description of num columns
print("\nDescriptive stats:\nn", df.describe())

#Unique values in categorical features
print("\nRoom Types:\n", df['room_type'].value_counts())
print("\nNeighbourhood groups:\n", df['neighbourhood_group'].value_counts())

plt.figure(figsize=(10,6))
sns.histplot(df['price'], bins=50, kde=True)
plt.title('Price Distribution Before Outlier Removal')
plt.xlim(0,1000)
plt.show()

price_quantiles = df['price'].quantile([0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]).to_dict()
print("\nPrice quantiles:\n", price_quantiles)

# Set threshold for price outliers (using 99th percentile as upper limit)
price_upper_limit = df['price'].quantile(0.99)
print(f"\nSetting upper price limit to ${price_upper_limit:.2f}")

# ADDED: Check minimum_nights distribution
plt.figure(figsize=(10,6))
sns.histplot(df['minimum_nights'], bins=50, kde=True)
plt.title('Minimum Nights Distribution Before Outlier Removal')
plt.xlim(0,50)
plt.show()

# ADDED: Check quantiles for minimum_nights
min_nights_quantiles = df['minimum_nights'].quantile([0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 0.999]).to_dict()
print("\nMinimum nights quantiles:\n", min_nights_quantiles)

# ADDED: Set threshold for minimum_nights outliers (using 99th percentile)
min_nights_upper_limit = df['minimum_nights'].quantile(0.99)
print(f"\nSetting upper minimum nights limit to {min_nights_upper_limit:.0f}")

# Filter out price and minimum_nights outliers
df_filtered = df[(df['price'] <= price_upper_limit) & (df['minimum_nights'] <= min_nights_upper_limit)]

print(f"\nRemoved {len(df) - len(df_filtered)} outliers ({(len(df) - len(df_filtered))/len(df)*100:.2f}% of data)")

plt.figure(figsize=(10,6))
sns.histplot(df_filtered['price'], bins=50, kde=True)
plt.title('Price Distribution After Outlier Removal')
plt.xlim(0,1000)
plt.show()

# ADDED: Visualize minimum_nights distribution after outlier removal
plt.figure(figsize=(10,6))
sns.histplot(df_filtered['minimum_nights'], bins =50, kde=True)
plt.title('Minimum Nights Distribution After Outlier Removal')
plt.xlim(0,50)
plt.show()

df = df_filtered
df = df.drop(['id', 'name', 'host_name', 'last_review'], axis = 1)
df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
df.dropna(subset=['price'])
df = df.reset_index(drop=True)

# One-hot encode categorical columns
df = pd.get_dummies(df, columns = ['room_type', 'neighbourhood_group', 'neighbourhood'], drop_first=True)

y = df['price']
X = df.drop('price', axis=1)

# Split the data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred_rf = rf_model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred_rf)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_rf)

print(f"\nModel Performance After Outlier Removal:")
print(f"RMSE: {rmse:.2f}")
print(f"R² score: {r2:.2f}")

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x='Importance', y='Feature', data=feature_importance)
plt.title('Top 10 Most Features')
plt.tight_layout()
plt.show()

# Let's plot actual vs predicted prices
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred_rf, alpha=0.5)
plt.plot([0, max(y_test)], [0, max(y_test)], 'r--')
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title('Actual vs Predicted Prices')
plt.tight_layout()
plt.show()

residuals = y_test-y_pred_rf
plt.figure(figsize=(10,6))
sns.histplot(residuals, bins=50, kde=True)
plt.title('Residuals Distribution')
plt.xlabel('Residuals (Actual - Predicted)')
plt.tight_layout()
plt.show()

# Plot residuals vs predicted values
plt.figure(figsize=(10,6))
plt.scatter(y_pred_rf, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('Predicted Price')
plt.ylabel('Residual')
plt.title('Residuals vs Predicted Values')
plt.tight_layout()
plt.show()
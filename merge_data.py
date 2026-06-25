import pandas as pd
import numpy as np

print("Loading rainfall data...")
rain = pd.read_csv('rainfall_2021_2025.csv')
rain['date'] = pd.to_datetime(rain['date'])

print("Loading maxtemp data...")
maxtemp = pd.read_csv('maxtemp_2021_2025.csv')
maxtemp['date'] = pd.to_datetime(maxtemp['date'])

print("Loading mintemp data...")
mintemp = pd.read_csv('mintemp_2021_2025.csv')
mintemp['date'] = pd.to_datetime(mintemp['date'])

print("Mapping rainfall grid to temp grid...")
rain['temp_lat'] = (rain['lat'] - 0.5).round() + 0.5
rain['temp_lon'] = (rain['lon'] - 0.5).round() + 0.5

print("Aggregating temp data by date+lat+lon...")
maxtemp_agg = maxtemp.groupby(['date', 'lat', 'lon'])['tmax'].mean().reset_index()
maxtemp_agg = maxtemp_agg.rename(columns={'lat': 'temp_lat', 'lon': 'temp_lon'})

mintemp_agg = mintemp.groupby(['date', 'lat', 'lon'])['tmin'].mean().reset_index()
mintemp_agg = mintemp_agg.rename(columns={'lat': 'temp_lat', 'lon': 'temp_lon'})

print("Merging rainfall + maxtemp...")
merged = pd.merge(rain, maxtemp_agg, on=['date', 'temp_lat', 'temp_lon'], how='left')

print("Merging + mintemp...")
merged = pd.merge(merged, mintemp_agg, on=['date', 'temp_lat', 'temp_lon'], how='left')

merged = merged.dropna(subset=['tmax', 'tmin'])

merged['rain_occurred'] = (merged['rainfall'] > 2.5).astype(int)

merged['month'] = merged['date'].dt.month
merged['day_of_year'] = merged['date'].dt.dayofyear
merged['year'] = merged['date'].dt.year

final_cols = ['date', 'year', 'month', 'day_of_year', 'lat', 'lon', 'tmax', 'tmin', 'rainfall', 'rain_occurred']
final = merged[final_cols]

final.to_csv('merged_climate_data.csv', index=False)
print(f"Saved merged_climate_data.csv with {len(final)} rows")
print(final.head())
print("DONE!")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Loading merged climate data...")
df = pd.read_csv('../merged_climate_data.csv')
df['date'] = pd.to_datetime(df['date'])

print("Loading wind data...")
wind = pd.read_csv('reanalysis-era5-land-timeseries-sfc-wind9zgxdrsh.csv')
wind['valid_time'] = pd.to_datetime(wind['valid_time'])
wind['wind_speed'] = np.sqrt(wind['u10']**2 + wind['v10']**2)

def run_heat_seeking_and_validate(test_date_str, region_name, seed):
    target_date = pd.to_datetime(test_date_str)
    day_data = df[df['date'] == target_date].copy()
    
    if len(day_data) == 0:
        return None, None
    
    cloud_source = day_data.loc[day_data['rainfall'].idxmax()]
    
    wind_on_date = wind[wind['valid_time'].dt.date == target_date.date()]
    if len(wind_on_date) == 0:
        wind_on_date = wind.tail(24)
    
    avg_u = wind_on_date['u10'].mean()
    avg_v = wind_on_date['v10'].mean()
    avg_speed = np.sqrt(avg_u**2 + avg_v**2)
    
    speed_kmh = avg_speed * 3.6
    deg_per_hour = speed_kmh / 111.0
    direction_lat = (avg_v / avg_speed) if avg_speed > 0 else 0
    direction_lon = (avg_u / avg_speed) if avg_speed > 0 else 0
    
    path_points = []
    for hours in [6, 12, 24, 72]:
        distance_deg = deg_per_hour * hours
        new_lat = cloud_source['lat'] + direction_lat * distance_deg
        new_lon = cloud_source['lon'] + direction_lon * distance_deg
        path_points.append({'hours': hours, 'lat': round(new_lat, 2), 'lon': round(new_lon, 2)})
    
    historical = df[df['year'] < 2025]
    target_month = target_date.month
    
    for point in path_points:
        nearby_hist = historical[
            (abs(historical['lat'] - point['lat']) <= 0.5) &
            (abs(historical['lon'] - point['lon']) <= 0.5) &
            (historical['month'] == target_month)
        ]
        point['avg_temp'] = nearby_hist['tmax'].mean() if len(nearby_hist) > 0 else np.nan
    
    valid_points = [p for p in path_points if not np.isnan(p['avg_temp'])]
    if not valid_points:
        return None, None
    
    hottest = max(valid_points, key=lambda p: p['avg_temp'])
    predicted_date = target_date + timedelta(hours=hottest['hours'])
    
    # HEAT-SEEKING prediction check
    actual_data = df[
        (df['date'].dt.date == predicted_date.date()) &
        (abs(df['lat'] - hottest['lat']) <= 0.5) &
        (abs(df['lon'] - hottest['lon']) <= 0.5)
    ]
    heat_seeking_correct = None
    if len(actual_data) > 0:
        heat_seeking_correct = actual_data['rain_occurred'].max() == 1
    
    # RANDOM baseline: pick a random location on same predicted date
    np.random.seed(seed)
    same_date_data = df[df['date'].dt.date == predicted_date.date()]
    random_correct = None
    if len(same_date_data) > 0:
        random_row = same_date_data.sample(n=1, random_state=seed).iloc[0]
        random_correct = random_row['rain_occurred'] == 1
    
    print(f"{region_name} ({test_date_str}): Heat-Seeking={'CORRECT' if heat_seeking_correct else 'WRONG' if heat_seeking_correct is not None else 'N/A'}, "
          f"Random={'CORRECT' if random_correct else 'WRONG' if random_correct is not None else 'N/A'}")
    
    return heat_seeking_correct, random_correct

test_cases = [
    ('2024-07-15', 'Monsoon - South India'),
    ('2024-08-01', 'Monsoon - West India'),
    ('2024-09-10', 'Late Monsoon - North India'),
    ('2024-06-20', 'Pre-Monsoon - Central India'),
    ('2024-07-25', 'Monsoon - East India'),
    ('2024-08-15', 'Monsoon - South India 2'),
    ('2024-09-01', 'Monsoon - North India'),
    ('2024-06-10', 'Pre-Monsoon - West India'),
    ('2024-01-15', 'Winter - North India'),
    ('2024-02-20', 'Winter - Central India'),
    ('2024-11-10', 'Post-Monsoon - South India'),
    ('2024-12-05', 'Winter - East India'),
]

heat_seeking_results = []
random_results = []

print(f"\n{'='*70}")
print("RUNNING HEAT-SEEKING VS RANDOM BASELINE COMPARISON")
print(f"{'='*70}\n")

for i, (date_str, region) in enumerate(test_cases):
    hs, rand = run_heat_seeking_and_validate(date_str, region, seed=i)
    if hs is not None:
        heat_seeking_results.append(hs)
    if rand is not None:
        random_results.append(rand)

print(f"\n{'='*70}")
print("FINAL COMPARISON SUMMARY")
print(f"{'='*70}")
print(f"Total test cases: {len(test_cases)}")

if len(heat_seeking_results) > 0:
    hs_accuracy = sum(heat_seeking_results) / len(heat_seeking_results) * 100
    print(f"\nHEAT-SEEKING Accuracy: {hs_accuracy:.1f}% ({sum(heat_seeking_results)}/{len(heat_seeking_results)})")

if len(random_results) > 0:
    rand_accuracy = sum(random_results) / len(random_results) * 100
    print(f"RANDOM Baseline Accuracy: {rand_accuracy:.1f}% ({sum(random_results)}/{len(random_results)})")

if len(heat_seeking_results) > 0 and len(random_results) > 0:
    improvement = hs_accuracy - rand_accuracy
    print(f"\n>>> IMPROVEMENT OVER RANDOM: {improvement:+.1f} percentage points")
    if improvement > 5:
        print(">>> Heat-Seeking system shows REAL predictive value over random guessing!")
    elif improvement > -5:
        print(">>> Heat-Seeking system performs SIMILAR to random - needs improvement")
    else:
        print(">>> Heat-Seeking system performs WORSE than random - needs investigation")

print("\nDONE!")
import xarray as xr
import pandas as pd

all_years = []

for year in [2021, 2022, 2023, 2024, 2025]:
    print(f"Processing Rainfall {year}...")
    ds = xr.open_dataset(f'RF25_ind{year}_rfp25.nc')
    df = ds.to_dataframe().reset_index()
    df = df.dropna(subset=['RAINFALL'])
    df = df.rename(columns={'TIME': 'date', 'LATITUDE': 'lat', 'LONGITUDE': 'lon', 'RAINFALL': 'rainfall'})
    all_years.append(df)
    ds.close()

rain_df = pd.concat(all_years, ignore_index=True)
rain_df.to_csv('rainfall_2021_2025.csv', index=False)
print(f"Saved rainfall_2021_2025.csv with {len(rain_df)} rows")
print("DONE!")
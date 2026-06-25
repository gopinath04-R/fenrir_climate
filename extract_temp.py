import numpy as np
import pandas as pd
from datetime import datetime, timedelta

lat = np.arange(7.5, 38.0, 1.0)
lon = np.arange(67.5, 98.0, 1.0)
nlat = len(lat)
nlon = len(lon)

def days_in_year(year):
    return 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365

def read_grd(filename, nlat, nlon, ndays):
    data = np.fromfile(filename, dtype=np.float32)
    data = data.reshape(ndays, nlat, nlon)
    return data

def grd_to_dataframe(filename, year, varname):
    ndays = days_in_year(year)
    data = read_grd(filename, nlat, nlon, ndays)
    
    records = []
    start_date = datetime(year, 1, 1)
    
    for day in range(ndays):
        date = start_date + timedelta(days=day)
        for i, la in enumerate(lat):
            for j, lo in enumerate(lon):
                val = data[day, i, j]
                if val < 90:  # filter out 99.9 missing marker
                    records.append({
                        'date': date,
                        'lat': la,
                        'lon': lo,
                        varname: val
                    })
    return pd.DataFrame(records)

# Process all years for Maxtemp
all_years_max = []
for year in [2021, 2022, 2023, 2024, 2025]:
    print(f"Processing Maxtemp {year}...")
    df = grd_to_dataframe(f'Maxtemp_MaxT_{year}.GRD', year, 'tmax')
    all_years_max.append(df)

maxtemp_df = pd.concat(all_years_max, ignore_index=True)
maxtemp_df.to_csv('maxtemp_2021_2025.csv', index=False)
print(f"Saved maxtemp_2021_2025.csv with {len(maxtemp_df)} rows")

# Process all years for Mintemp
all_years_min = []
for year in [2021, 2022, 2023, 2024, 2025]:
    print(f"Processing Mintemp {year}...")
    df = grd_to_dataframe(f'Mintemp_MinT_{year}.GRD', year, 'tmin')
    all_years_min.append(df)

mintemp_df = pd.concat(all_years_min, ignore_index=True)
mintemp_df.to_csv('mintemp_2021_2025.csv', index=False)
print(f"Saved mintemp_2021_2025.csv with {len(mintemp_df)} rows")

print("DONE!")
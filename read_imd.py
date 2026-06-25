import numpy as np

# IMD GRD format standard grid: 1deg x 1deg
# Lat: 7.5N to 37.5N (31 points), Lon: 67.5E to 97.5E (31 points)
lat = np.arange(7.5, 38.0, 1.0)
lon = np.arange(67.5, 98.0, 1.0)
nlat = len(lat)
nlon = len(lon)

def read_grd(filename, nlat, nlon, ndays):
    data = np.fromfile(filename, dtype=np.float32)
    expected = nlat * nlon * ndays
    print(f"File: {filename}")
    print(f"Total values in file: {data.size}")
    print(f"Expected (nlat*nlon*ndays): {expected}")
    print(f"nlat={nlat}, nlon={nlon}")
    return data

# Test with 2024 (leap year = 366 days)
data2024 = read_grd('Maxtemp_MaxT_2024.GRD', nlat, nlon, 366)
print("Sample values:", data2024[:10])
# tle
Two Line Element position calculator

A simple Python script which generates CSV files with time and satellite position (ECEF)

TLE data can come from [Celestrak](https://www.celestrak.com) or any other source which is formatted correctly. The TLE data is fetched and SV position is calculated for points at specified time intervals.

## Usage
```
python tle_calc.py
```

## Inputs

### Enter TLE url:
Enter the url of TLE data, e.g. https://www.celestrak.com/NORAD/elements/iridium.txt

### Enter satellite name (blank for all):
Enter a satellite name, e.g. 'IRIDIUM 70'. This field is optional; leaving it blank will generate generate tracks for all satellites in separate CSV files.

### Enter start date (YYYY, MM, DD, HH, MM, SS):
Enter the time of the first sample. This field is optional; leaving it blank will use the current system time.

### Enter sample interval (minutes):
Enter the sample interval in minutes, e.g. 1

### Enter total number of samples (max 24H duration):
Enter the total number of positions to calculate, e.g. 101. The 24 hour limit is not enforced, and running longer should work as expected so long as you don't cross a leap day/second; this is not throughly tested and you should verify timestamp transitions in the output.

## Outputs

A CSV file is generated containing timestamps and x, y, x satellite positions in ECEF coordinates. By default WGS84 is used, but this can be modified in the source code.

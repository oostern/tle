# tle
Two Line Element position calculator

A simple Python script which generates CSV files with time and satellite position (ECEF)

TLE data can come from [Celestrak](https://www.celestrak.com) or any other source which is formatted correctly. The TLE data is fetched and SV position is calculated for points at specified time intervals.

You will need SGP4 installed. On Ubuntu this can be accomplished with
```
apt install python-sgp4
```

## Usage
```
python tle_calc.py
```

## Inputs

### Enter TLE url:
Enter the url of TLE data, e.g. https://www.celestrak.com/NORAD/elements/iridium.txt

### Enter satellite name (blank=all):
Enter a satellite name, e.g. 'IRIDIUM 70'. This field is optional; leaving it blank will generate generate tracks for all satellites in separate CSV files.

This performs a partial match against the downloaded TLE; entering ```IRIDIUM 7``` will match against ```IRIDIUM 7 [-]           ```

### Enter start date and time (UTC, blank=system time) (YYYY, MM, DD, HH, MM, SS, MICROS):
Enter the time of the first sample. This field is optional; leaving it blank will use the current system time. Microseconds supports up to 6 digits.

### Enter field to be incremented [hr, min, sec, us]:
Enter the time field to increment

### Enter the incrementation value:
Enter the value by which to increment the previously specified field. For example, if you entered 'min' at the previous step, entering 15 will produce time steps of 15 minutes.

Note that the python datetime object used to represent timestamps does not support leap seconds, so if your specified interval crosses a leap second the physical time between samples is not expected to be correct.

### Enter total number of samples:
Enter the total number of positions to calculate, e.g. 101.

## Outputs

A CSV file is generated containing timestamps (year, month, day, hour, minute, second) and x, y, x satellite positions in ECEF coordinates. By default WGS84 is used, but this can be modified in the source code.

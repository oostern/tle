# Copyright Colton Riedel (2018)
# License: MIT

import datetime
import urllib2
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv

days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

url = raw_input("Enter TLE url: ")
sat = raw_input("Enter satellite name (blank for all): ").rstrip()
start = raw_input("Enter start date (YYYY, MM, DD, HH, MM, SS): ")
inc = int(raw_input("Enter sample interval (minutes): "))
num_samples = int(\
        raw_input("Enter total number of samples (max 24H duration): "))

if start.strip() == "":
    now = datetime.datetime.now()

    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
else:
    start = start.split()
    if len(start) != 6:
        print "\nUnable to parse date"
        exit(1)

    year = int(start[0])
    month = int(start[1])
    day = int(start[2])
    hour = int(start[3])
    minute = int(start[4])
    second = int(start[5])

yyear = year
mmonth = month
dday = day
hhour = hour
mminute = minute
ssecond = second

if num_samples * inc >= 1440:
    print "\nWarning: Longer than 24 hour period specified"
    print " (I won't stop you, but it might not work)"

if num_samples * inc > (24 - hour) * 60:
    print "\nWarning: Sample period involves date change"
    print " (Too lazy to test this well or handle leap years)"

response = urllib2.urlopen(url)
data = response.read()

name_index = data.find(sat.strip())
eol_index = data.find("\n", name_index)

if name_index == -1 or eol_index == -1:
    print "\nNo match for " + sat + " in TLE specified"
    exit(1)

if sat.strip() != "":
    output_filename = sat.strip() + "-" + str(year) + "_" + str(month) + "_" \
            + str(day) + "_" + str(hour) + "_" + str(minute) + "_" \
            + str(second) + "-" + str(inc) + "-" + str(num_samples) + ".csv"
    output_filename = output_filename.replace(" ", "_").replace("(", "_")\
            .replace(")", "_").replace("/", "_")

    outfile = open(output_filename, "w")

    line1_index = eol_index + 1
    line2_index = eol_index + 72

    line1 = data[line1_index:line1_index+70]
    line2 = data[line2_index:line2_index+70]

    satellite = twoline2rv(line1, line2, wgs84)

    for i in range(num_samples):
        minute += inc

        if minute > 59:
            hour += 1
            minute = minute % 60

        if hour > 23:
            day += 1
            hour = hour % 24

        if day > days_per_month[month - 1]:
            month += 1
            day = 1

        if month > 12:
            year += 1
            month = 1

        datestamp = str(year).zfill(4) + "," + str(month).zfill(2) + "," \
                + str(day).zfill(2) + "," + str(hour).zfill(2) + "," \
                + str(minute).zfill(2) + "," + str(second).zfill(2)

        position, v = \
                satellite.propagate(year, month, day, hour, minute, second)

        position_string = ","
        if (position[0] > 0):
            position_string += " "
        position_string += str(position[0]) + ","

        while len(position_string) < 16:
            position_string += " "

        if (position[1] > 0):
            position_string += " "

        position_string += str(position[1]) + ","

        while len(position_string) < 31:
            position_string += " "

        if (position[2] > 0):
            position_string += " "

        position_string += str(position[2])

        outfile.write(datestamp + position_string + "\n");

    outfile.close()

else:
    print "Getting all SVs"

    while(eol_index < len(data)):
        sat = data[(eol_index-25):eol_index].strip()

        output_filename = sat.strip() + "-" + str(year) + "_" + str(month) \
                + "_" + str(day) + "_" + str(hour) + "_" + str(minute) + "_" \
                + str(second) + "-" + str(inc) + "-" + str(num_samples) + ".csv"
        output_filename = output_filename.replace(" ", "_").replace("(", "_")\
                .replace(")", "_").replace("/", "_")

        outfile = open(output_filename, "w")

        line1_index = eol_index + 1
        line2_index = eol_index + 72

        line1 = data[line1_index:line1_index+70]
        line2 = data[line2_index:line2_index+70]

        satellite = twoline2rv(line1, line2, wgs84)

        for i in range(num_samples):
            minute += inc

            if minute > 59:
                hour += 1
                minute = minute % 60

            if hour > 23:
                day += 1
                hour = hour % 24

            if day > days_per_month[month - 1]:
                month += 1
                day = 1

            if month > 12:
                year += 1
                month = 1

            datestamp = str(year).zfill(4) + "," + str(month).zfill(2) + "," \
                    + str(day).zfill(2) + "," + str(hour).zfill(2) + "," \
                    + str(minute).zfill(2) + "," + str(second).zfill(2)

            position, v = \
                    satellite.propagate(year, month, day, hour, minute, second)

            position_string = ","
            if (position[0] > 0):
                position_string += " "
            position_string += str(position[0]) + ","

            while len(position_string) < 16:
                position_string += " "

            if (position[1] > 0):
                position_string += " "

            position_string += str(position[1]) + ","

            while len(position_string) < 31:
                position_string += " "

            if (position[2] > 0):
                position_string += " "

            position_string += str(position[2])

            outfile.write(datestamp + position_string + "\n");

        outfile.close()

        eol_index = eol_index + 71 + 71 + 26

        year = yyear
        month = mmonth
        day = dday
        hour = hhour
        minute = mminute
        second = ssecond

        print '.',

print "\nDone"

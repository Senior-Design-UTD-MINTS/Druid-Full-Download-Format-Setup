# NOTE: READ THIS BEFORE YOU RUN THIS PROGRAM
# THIS PROGRAM SHOULD BE RUN IN A FOLDER CALLED 'formatdata' INSIDE THE DRUID INCUBATING FOLDER. YOU MUST CREATE THIS FOLDER
# YOU MUST MANUALLY UPDATE THE upSpec.json FILE. THE FILE NEEDS THE FILE PATH TO WHERE THE CSV IS DOWNLOADED TO. IF THE LOCAL PATH IS NOT SPECIFIED IT WON'T WORK
# ONCE YOU RUN THIS PROGRAM THERE SHOULD BE THREE FILES IN 'formatdata': upSpec.json, formatCSV.py and formatted.csv
# DATA SHOULD LOAD INTO DRUID PROVIDED YOU HAVE THE UPLOAD SPEC WITH THE CORRECT DATA SOURCE
import urllib
import pandas as pd
import subprocess as sp
import os
import csv
from tempfile import NamedTemporaryFile
import shutil


urlPart1 = "http://mintsdata.utdallas.edu:4200/api/001e06305a12/2019/"
urlPart2 = "/MINTS_001e06305a12_calibrated_UTC_2019_"


with open("fullcsv.csv", 'wb') as f:
    for m in range(8, 13):  # loop thru months - starting in August going through December 2019. M stores month number
        if(m < 10):
            mString = "0" + str(m)
        else:
            mString = str(m)

        # loops through each day in month thru 31 - if only 30 days just skips and continues
        for j in range(1, 32):
            # Make it verbose so you know whats going on
            print("Fetching data for " + mString + "/" + str(j))
            if(j < 10):  # Format of date places 0 in front of day num - this formats string so it has that 0 when fetching
                url = "{}".format(urlPart1) + mString + "/" + "0" + str(j) + \
                    "{}".format(urlPart2) + mString + \
                    "_" + "0" + str(j) + ".csv"
            else:
                url = "{}".format(urlPart1) + mString + "/" + str(j) + \
                    "{}".format(urlPart2) + mString + "_" + str(j) + ".csv"

            try:
                filedata = urllib.request.urlopen(url)
            except urllib.request.HTTPError:  # If there is no csv data for specified date it will except, print, and continue
                print("No CSV data for " + mString + str(j))
                continue
            else:
                f.write(filedata.read())

f.close()


filename = "fullcsv.csv"
tempfile = NamedTemporaryFile(delete=False, mode='w')


with open(filename, 'r') as f, tempfile:
    # date formats are bad for early data. This fixes that
    print("Formatting csv file...")
    reader = csv.reader(f, delimiter=',', quotechar='"')
    writer = csv.writer(tempfile, delimiter=',', quotechar='"')

    for row in reader:  # cinitial column names
        writer.writerow(row)
        break

    for row in reader:  # don't read in column name rows
        if(row[0] == "dateTime"):
            continue
        else:  # Replaces str value with number value. Also rearranges date to be in proper format
            if "Aug" in row[0]:
                row[0] = row[0].replace("Aug", "08")
                row[0] = row[0].replace(" ", "T") + 'Z'
                date = row[0][0: 2]
                row[0] = row[0].replace("2019", date)
                row[0] = "2019" + row[0][2:]
            elif "Sep" in row[0]:
                row[0] = row[0].replace("Sep", "09")
                row[0] = row[0].replace(" ", "T")
                date = row[0][0: 2]
                row[0] = row[0].replace("2019", date)
                row[0] = "2019" + row[0][2:]

            if "-" not in row[0]:  # adds dashes and colons if missing
                row[0] = row[0][: 4] + '-' + row[0][4: 6] + '-' + \
                    row[0][6: 11] + ':' + row[0][11: 13] + ':' + row[0][13: 16]

            writer.writerow(row)

    # replace old, unformatted file with formatted file
    shutil.move(tempfile.name, filename)
    f.close

os.rename("fullcsv.csv", "formatted.csv")


print("All data has been succesfully downloaded and formatted. In order to upload it to Druid, a Druid instance must be running on the machine.\n"
      + "In order to upload the data, the proper upload spec must be provided in the command. \n"
      + "The upload spec must be in a folder called 'formatdata' and be named'upSpec.json'. \n"
      + " Make sure you have the right upload spec and Druid is running.\n"
      + "Do you wish to upload to Druid now? (y/n)")

ans = input()
if(ans == "y"):
    #os.system("cd ..")
    os.system(
        "./../bin/post-index-task --file upSpec.json --url http://localhost:8888")
else:
    print("Exiting")

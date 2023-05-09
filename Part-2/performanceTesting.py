# import required modules
import time as timer
import csv
import json
import sys
from MRTD import decode, encode


# This file tests the speed of encode and decode in MRTD.py


#This function opens the file, reads the data and returns it by taking off the extension of the filename.
def readData(jsonFile):

    #the file is opened as jsonData
    with open(jsonFile) as jsonData:
        data = json.load(jsonData) #returns json object in key/value pair

    data = data[jsonFile[:-5]] 
    return data

#this function tests the performance of the functions - encode and decode
#given csv files are used
def testPerformance(jsonfiles, function):

    #Loading the files
    print("Currently running: ", jsonfiles)
    #striping from the end of filename
    title = jsonfiles[:-5] 

    #0pen csv files
    with open('performance_'+title+'.csv', 'w') as file:
        headers = ["number of lines read (n)", "time in seconds (s)"]
        writer = csv.writer(file)
        writer.writerow(headers)
        data = readData(jsonfiles)
        iterations = 100 #initialising iterations to 100
        while iterations <= 10000:
            #Starting the timer using python timer function
            start = timer.perf_counter()
            for iteration in range(iterations):
                # Process the number of records specified by the iterations
                function(data[iteration])
            ##Stopping the timer by python timer functio
            stop = timer.perf_counter()
            #Calculating the time
            time = stop - start
            #Writing the iterations and time in the csv file
            writer.writerow([iterations, time])
            print("Processed ",iterations, " records in ",round(time,4),"seconds.")

            #Increasing the number of records to be processed
            if iterations == 100:
                iterations = 1000
                continue
            iterations += 1000
    #prints which file is done processesing
    print("Done processing - ",title)

#Runing the function for encode and decode for decoded and encoded records
testPerformance("records_decoded.json", encode)
testPerformance("records_encoded.json", decode)

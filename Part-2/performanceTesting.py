# import required modules
import time as timer
import csv
import json
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
    print("running: ", jsonfiles)
    #striping from the end of filename
    title = jsonfiles[:-5] 

    #0pen csv files
    with open('performance_'+title+'.csv', 'w') as file:
        headers = ["lines read (n)", "time (s)"]
        writer = csv.writer(file)
        writer.writerow(headers)
        data = readData(jsonfiles)
        iterations = 100 #initialising iterations to 100
        while iterations <= 10000:
            #Starting the timer using python timer function
            start = timer.perf_counter()
            for j in range(iterations):
                # Process the number of records specified by the iterations
                function(data[j])
            ##Stopping the timer by python timer functio
            stop = timer.perf_counter()
            #Calculating the time
            time = stop - start
            printResult = f"Processed {iterations} records in {time:.4f} seconds."
            result = [iterations, time]
            # Write the processing time and number of records to the csv file
            writer.writerow(result)
            print(printResult)

            # Increase the number of records to be processed
            if iterations == 100:
                iterations = 1000
                continue
            iterations += 1000

    print("Done processing - ",title)

# Run the test for encode and decode with different files
testPerformance("records_decoded.json", encode)
testPerformance("records_encoded.json", decode)

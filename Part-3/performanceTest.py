# import required modules
import time as timer
import csv
import json
from MRTD import decode, encode

# This file tests the speed of encode and decode in MRTD.py

def readData(file):
    """
    Load the data from json file and return the data by stripping the file name extension.
    """
    with open(file) as f:
        data = json.load(f)
    data = data[file[:-5]]
    return data

def testPerformance(file, function):
    """
    Test the performance of encode and decode functions on the given file.
    """
    # Load the files
    print("running: ", file)
    title = file[:-5]  # strip ending from the file name
    # Open the csv file for writing the results
    with open(f'performance_{title}.csv', 'w') as f:
        headers = ["lines read (n)", "time (s)"]
        writer = csv.writer(f)
        writer.writerow(headers)

        data = readData(file)
        iterations = 100
        while iterations <= 10000:
            # Start the timer
            start = timer.perf_counter()
            for j in range(iterations):
                # Process the number of records specified by the iterations
                function(data[j])
            # Stop the timer
            stop = timer.perf_counter()
            time = stop - start  # Calculate the processing time
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

    print(f"Done processing {title}.")

# Run the test for encode and decode with different files
testPerformance("records_decoded.json", encode)
testPerformance("records_encoded.json", decode)

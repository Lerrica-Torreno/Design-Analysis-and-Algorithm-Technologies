# TORRENO, Lerrica Jeremy S. (BSCS-DS 2nd yr)
# Prelim Examination: Algorithm Implementation 
# comb sort algorithm based on number of ratings 

# import for data handling and measurement of execution time
import pandas as pd
import time

# filepath of csv file 
csvFile = "C:\\Users\\lerri\\Desktop\\DAA\\Prelim-Finished\\Updated_Mobile_Dataset.csv"

# function for user's choice in sorting the number of ratings 
def userChoice():
    choice = input("Enter A for ascending order and D for descending order: ")

    # error handling if input is not valid  
    if choice.upper() not in ["A", "D"]:
        print("Please enter only A or D.")
        return userChoice()
    else:
        order = 'ascending' if choice.upper() == 'A' else 'descending' 
        csvRate(csvFile, order) # calls function to proceed with the order 

# function for accessing the csv file
def csvRate(csvFile, order):
    df = pd.read_csv(csvFile)
    # will access the column and replace comma in the data with space will remain as str then converted to int 
    df["No_of_ratings"] = df["No_of_ratings"].replace({',': ''}, regex=True)
    df["No_of_ratings"] = pd.to_numeric(df["No_of_ratings"], errors='coerce')

    # error handling if No_of_ratings is not in csv file 
    if "No_of_ratings" not in df.columns:
        print("Csv file error: 'No_of_ratings' column not found in the dataset.")
        return

    # function for comb sort algorithm
    def combSort(arr):
        n = len(arr)
        gap = n 
        shrink = 1.3 # default value 
        sorted = False # flag for sorting (sorting not started)

        # start of time execution 
        startTime = time.time()

        while not sorted:
            gap = int(gap / shrink) # formula 
            if gap <= 1:
                gap = 1  
                sorted = True # flag for sorting (sorting done)
            for i in range(n - gap):
                # swap condition for sorting order
                if (order == 'ascending' and arr[i] > arr[i + gap]) or (order == 'descending' and arr[i] < arr[i + gap]): 
                    arr[i], arr[i + gap] = arr[i + gap], arr[i] # swap if condition is met
                    sorted = False # flag for sorting (swap occured, run again)
    
        # computation of time after sorting is completed  
        endTime = time.time()
        elapsedTime = endTime - startTime
        print(f"Execution time of Comb Sort Algorithm: {elapsedTime:.8f} seconds.")
        return arr

    # applies comb sort to extracted column and adds to list "sorted ratings"
    sortedRatings = combSort(df['No_of_ratings'].tolist())
    # updates old column with new and sorted ones 
    df['No_of_ratings'] = sortedRatings
    # sorts column according to order based on No_of_ratings
    dfSorted = df.sort_values(by=['No_of_ratings', 'Model'], ascending=(order == 'ascending'))

    # creates and saves in csv file based on order 
    outputFilename = f"Sorted_No_of_Ratings_{order}.csv"
    # saves it as a new column to csv and prevents saving row numbers
    dfSorted[['No_of_ratings']].to_csv(outputFilename, index=False)
    print(f"Sorted 'No_of_ratings' data has been saved to {outputFilename}")

    # display 20 sorted data per page 
    displaySortedData(dfSorted[['No_of_ratings']])

# function to display sorted data 
def displaySortedData(dfSorted):
    pageSize = 30 
    totalRows = len(dfSorted[['No_of_ratings']])
    start = 0 

    while start < totalRows:
        # ensures 30 rows are shown each page
        end = min(start + pageSize, totalRows)
        # prints specific column up to 30 rows without showing row number 
        print(dfSorted[['No_of_ratings']].iloc[start:end].to_string(index=False))
        start += pageSize
        if start < totalRows:
            input("\nPress Enter to view next page.")

userChoice()
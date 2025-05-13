# Even Number Filter - print rows where the first number is even

import pandas as pd  # Data handling
csv_file = "C:\\Users\\lerri\\Desktop\\DAA\\Prelim-Finished\\machine_problems_dataset.csv"

def EvenFirstDigit(csv_file):
    """
    Reads a CSV file and prints numbers from the 'Number1' column
    where the first digit is even. Includes error handling for invalid entries.
    """
    df = pd.read_csv(csv_file)  # Load CSV into a DataFrame

    for number in df["Number1"]:
        try:
            # Convert number to string to extract first digit
            first_char = str(number).strip()[0]
            first_digit = int(first_char)  # Converting first character to integer

            if first_digit % 2 == 0:
                print(f"Even first digit: {number}")
            else:
                print(f"Odd first digit: {number}")

        except (ValueError, IndexError):
            # ValueError = non-digit character like a letter
            # IndexError = empty string
            print(f"Invalid entry in CSV: '{number}'")

# Call the function
EvenFirstDigit(csv_file)

# Time complexity: O(n), where n = number of rows in the 'Number1' column
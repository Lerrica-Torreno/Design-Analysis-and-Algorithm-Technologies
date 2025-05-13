# Torreno, Lerrica Jeremy S. 
# BSCS-DS 2 | DAA
# counting algo 

# Create a working program that will count the number of males, females and computers in this computer lab

dataStudent = ["male", "male", "male", "male", "male", "male", "male", "male", "male", "male", "male",
                "Female", "female", "female", "female", "female", "female"]

dataLab = ["computer", "Computer", "computer", "computer", "computer", "computer", "computer", "computer",
            "computer", "computer", "computer", "computer", "computer", "computer", "computer", "computer",
            "computer", "computer", "computer", "computer"]

NumberOfFemales = 0
NumberOfMales = 0
NumberOfComputers = 0

# Count the number of students
for student in dataStudent:
    if student.lower() == 'male':
        NumberOfMales += 1
    elif student.lower() == 'female':
        NumberOfFemales += 1
    else:
        print(f"Warning: Unknown entry '{student}' in student data.")

# Count the number of computers
for item in dataLab:
    if item.lower() == 'computer':
        NumberOfComputers += 1
    else:
        print(f"Warning: Unknown item '{item}' in laboratory data.")

print(f"Number of Males: {NumberOfMales}")
print(f"Number of Females: {NumberOfFemales}")
print(f"Number of Computers: {NumberOfComputers}")




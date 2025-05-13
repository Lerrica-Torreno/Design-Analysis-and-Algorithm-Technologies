# linear search 

# function for linearsearch with the parameter list and target 
def linearSearch(list, target): 
    SizeOfList = len(list) # SizeOfList = 5 
    for i in range(0, SizeOfList): # I will be the one to check starting from index 0, stop before 5
        if list[i] == target: # if I is equal to the target, it will return True, if not, False
            return True
    return False

list = [2, 4, 3, 40, 10] # array 
result1 = linearSearch(list, 40) # target = 40 
print (result1)

result2 = linearSearch(list, 9) # target = 9
print (result2)

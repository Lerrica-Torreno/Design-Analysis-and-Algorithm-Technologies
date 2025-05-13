# binary search - sorted array

# main function 
def BinarySearchAlgorithm(list, target):
    return BinarySearch(list, 0, len(list)-1, target) # len(list) = 5

# actual binary search 
def BinarySearch(list, left, right, target):
    while left <= right: # ensures that the number is part of the list 
        MiddleValue = (left+right)//2 # midpoint 
        if list[MiddleValue] == target: 
            return MiddleValue
        elif list[MiddleValue] < target: 
            left = MiddleValue + 1 # skips middle & all values at left
        else:
            right = MiddleValue - 1 # skips middle & all values at right
    return -1

list = [10, 20, 30, 40, 50]
print(BinarySearchAlgorithm(list, 40)) 
print(BinarySearchAlgorithm(list, 80)) 
import copy


nums = [3,3]
target = 6
def f(nums, target):
    result = []
    x = {}
    
    for index, i in enumerate(nums):
        x[i] = index
    for index, i in enumerate(nums):
        search = target-i
        if search in x and x[search]!=index:
            result.append(index)
            result.append(x[search])
            return result
    
result = f(nums,target)
print(result)
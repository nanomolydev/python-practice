nums = [1,2,3]
target = 7

def f(nums,target):
    x = {}
    for index, i in enumerate(nums):
        search = target-i
        
        if search not in x:
            x[i] = index
        else:
            return [x[search], index]
    return []

print(f(nums,target))
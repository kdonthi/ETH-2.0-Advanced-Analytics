def meansquareerror(currlist, listofoptdistance):
	#finds mean square error 
	listofdiff = []
	for i,j in zip(currlist, currlist[1:]):
		listofdiff.append(j - i)
	meansquareerror = 0
	for i,j in zip(listofdiff, listofoptdistance):
		meansquareerror += ((j - i) ** 2)
	meansquareerror /= len(listofdiff)
	return (meansquareerror)



def recursiveMethod(currlist, candidates, N, include, vectorofoptdistance):
	#currlist is the subset of initial list we are creating
	#candidates is numbers we can add to currlist
	#N is number of numbers we need to have in final list
	#include is 1 if we should add the next candidate and 0 if we should not
	if (len(currlist) == N):
		currlist.sort()
		return([meansquareerror(currlist, vectorofoptdistance), currlist])
	elif (len(candidates) + len(currlist) < N):
		return ([-1,[]]) #if you cannot get N members 
	else:
		newvalue = candidates.pop(0)
		a = currlist[:]
		if include == 1:
			a.append(newvalue)
		first = recursiveMethod(a[:], candidates[:], N, 1, vectorofoptdistance)
		second = recursiveMethod(a[:], candidates[:], N, 0, vectorofoptdistance)
		if first[0] == -1:  #if -1, not enough members, so pick other result
			return (second)
		elif second[0] == -1:
			return (first)
		elif first[0] <= second[0]: 
			return (first)
		else:
			return (second)

def optimalSubsampleTrees(nums, N):
	#finds most evenly spaced N numbers by minimizing mean square error between successive differences and optimal distance: (distance between ends) / (N - 1)
	assert(N >= 1 and N <= len(nums))
	if N == 1:
		return ([nums[0]])
	elif N == 2:
		return ([nums[0], nums[len(nums) - 1]])
	elif N == len(nums):
		return (nums)
	else:
		startinglist = [nums[0], nums[len(nums) - 1]]
		candidates = nums[1:len(nums) - 1]
		optimalDistance = (nums[len(nums) - 1] - nums[0])/(N - 1) #creating a repeating list of the optimal distance, which is (distance between ends) / (N - 1)
		listofoptdistance = []
		for i in range(N - 1):
			listofoptdistance.append(optimalDistance)
		a = recursiveMethod(startinglist,candidates[:], N, 1, listofoptdistance)
		b = recursiveMethod(startinglist,candidates[:], N, 0, listofoptdistance)
		if a[0] == -1:
			return (b[1])
		elif b[0] == -1:
			return (a[1])
		elif a[0] <= b[0]:
			return (a[1])
		else:
			return (b[1])

import OptimalSubsampleTrees as ost
import OptimalSubsampleNew as os
import random
import time

correct = 0
incorrect = 0
begin = time.time()
runs = 2000 #number of trials
errorcounter = 0
for i in range(runs): 
	nums = random.randint(2,20) #number of numbers in the initial list
	test = []
	for j in range(nums):
		test.append(random.randint(-1000,1000)) #range of numbers in the initial list
	numtochoose = random.randint(2,nums) #number of evenly spaced numbers to choose from "nums"
	test.sort()
	res1 = os.optimalSubsample(test, numtochoose) #result from new algorithm
	res2 = ost.optimalSubsampleTrees(test, numtochoose) #result from old algorithm (considered as base truth)
	optimalDiff = (test[len(test) - 1] - test[0]) / (len(test) - 1)
	if len(res2) == 1:
		res1 = [res1]
	if res1 == res2: #if the two lists are the same
		correct += 1
	else:
		if abs(os.mseDiff(res1,optimalDiff) - os.mseDiff(res2, optimalDiff)) <= 10 ** -9: #if the successive differences of the two lists have mean square errors with delta <= 10 ** -9  (w.r.t. optimalDiff), the answer is "correct" 
			correct += 1
		else:
			errorcounter += 1
			print("Error #" + str(errorcounter) + ":")
			print("MSE Randomized Method (Being Tested): " + str(os.mseDiff(res1,optimalDiff)))
			print("MSE Recursive Tree Method (Base Truth): " + str(os.mseDiff(res2,optimalDiff)))
			incorrect += 1
			print("Data: ",end='')
			print(test)
			print("Result of Randomized Method: ",end='')
			print(res1)
			print("Result of Tree Method: ",end='')
			print(res2, end = '\n\n')
end = time.time()
decimal = correct / (correct + incorrect)
print("Stress Test Results for " + str(runs) + " samples:")
print("Correct: " + str(correct))
print("Incorrect: " + str(incorrect))
print("Percentage Correct: " + str(round(decimal * 100, 2)) + "%")
print("Time: " + str(end - begin))







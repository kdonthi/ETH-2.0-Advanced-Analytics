import random


def sumdiffsq(number, leftNum, rightNum, optimalDiff):
    # This function finds the sum of the mean squared errors between the (number,leftnum) and (number, rightnum) with respect to optimalDiff.
    return ((abs(number - leftNum) - optimalDiff) ** 2 + (abs(number - rightNum) - optimalDiff) ** 2)


def moveindex(index, nL, iL, rightLeft, optimalDiff):
    # This function moves a number from one index to another; the moving is bounded by the indexes to the right or left of the number and when the difference between the number on the right and number on the left changes signs (MSE optimized when left distance and right distance is equal)
    # "nL" is the original number list
    # "iL" is the list of indexes we want to include in our final list
    # rightLeft is 1 if we should move to right (right distance is more than left distance), 0 if we should move to left (left distance is more than right distance)
    # "optimalDiff" is (max(numsList) - min(numsList)) / (N - 1)
    indexcpy = iL[index]  # the index of numsList we are looking at
    if rightLeft == 1:
        while (indexcpy < iL[index + 1]):
            # if right distance becomes less than left distance
            if (nL[iL[index + 1]] - nL[indexcpy] < nL[indexcpy] - nL[iL[index - 1]]):
                # print("indexcpy " + str(indexcpy))
                break
            indexcpy += 1
        if indexcpy == iL[index + 1]:
            indexcpy -= 1
            if indexcpy == iL[index]:
                return(0)
            iL[index] = indexcpy
            # print("here 1")
            return (1)
        else:  # if broke because right dist. became less than left dist.
            if (sumdiffsq(nL[indexcpy], nL[iL[index + 1]], nL[iL[index - 1]], optimalDiff) <= sumdiffsq(nL[indexcpy - 1], nL[iL[index + 1]], nL[iL[index - 1]], optimalDiff)):
                iL[index] = indexcpy
                return (1)
            else:  # if right dist becoming less increased the error,  reduce by 1
                indexcpy -= 1
                if indexcpy == iL[index]:
                    return (0)
                else:
                    iL[index] = indexcpy
                    # print("Here 3")
                    return (1)

    elif rightLeft == 0:
        while (indexcpy > iL[index - 1]):
            # if left distance becomes less than right distance
            if (nL[indexcpy] - nL[iL[index - 1]] < nL[iL[index + 1]] - nL[indexcpy]):
                break
            indexcpy -= 1
        if (indexcpy == iL[index - 1]):
            indexcpy += 1
            if indexcpy == iL[index]:
                return(0)
            iL[index] = indexcpy
            return (1)
        else:  # if broke because left dist. becamse more than right dist.
            if (sumdiffsq(nL[indexcpy], nL[iL[index + 1]], nL[iL[index - 1]], optimalDiff) < sumdiffsq(nL[indexcpy + 1], nL[iL[index + 1]], nL[iL[index - 1]], optimalDiff)):
                iL[index] = indexcpy
                return (1)
            else:  # if left dist becoming less increased the error,  increase by 1
                if indexcpy + 1 == iL[index]:
                    return (0)
                else:
                    iL[index] = indexcpy + 1
                    return (1)
    return (1)


def trialSubsample(numsList, iList, diffMatrix, optimalDiff):
    # Takes in:
    # "numList" - original list of numbers,
    # "iList" - the list of indices to potentially include (will be adjusted to reduce MSE of successive differences to optimal difference)
    # "diff" - a N-1 * N-1 list of lists that contains abs(numsList[j] - numsList[i]) in numslist[j][i] (it is symmetric)
    # "optimalDiff" is (max(numsList) - min(numsList)) / (N - 1)
    change = -1
    while(change != 0):
        change = 0
        for i in range(1, len(iList) - 1):
            left = True
            right = True
            if iList[i] - iList[i - 1] == 1:
                left = False
            if iList[i + 1] - iList[i] == 1:
                right = False
            rightleftdifference = diffMatrix[iList[i]
                ][iList[i + 1]] - diffMatrix[iList[i]][iList[i - 1]]
            if rightleftdifference > 0 and right:
                change += moveindex(i, numsList, iList, 1, optimalDiff)
            elif rightleftdifference < 0 and left:
                change += moveindex(i, numsList, iList, 0, optimalDiff)
    finalList = []
    for i in iList:
        finalList.append(numsList[i])
    return (finalList)


def mseDiff(resultlist, optimalDiff):
    # This gives the Mean Square Error of the differences of the numbers with the optimalDiff (end - begin)/(N-1)
    mse = 0
    for i, j in zip(resultlist, resultlist[1:]):
        mse += (abs(j - i) - optimalDiff) ** 2
    mse /= (len(resultlist) - 1)
    return (mse)


def optimalSubsample(numsList, N):
    # Optimizes 150 initializations of the indexlist and finds the mean optimization which has successive differences that have the lowest MSE to the optimal difference.
    # "numsList" - the original list of numbers
    # "N" - the number of numbers in the final list
    assert(N >= 1 and len(numsList) >= 1)
    if N == 1:
        return(numsList[0])
    finallist = [numsList[0], numsList[len(numsList) - 1]]
    if N == 2:
        return (finallist)
    if N == len(numsList):
        return (numsList)
    diff = []
    for i in numsList:
        listtoadd = []
        for j in numsList:
            listtoadd.append(abs(j - i))
        diff.append(listtoadd)

    optimalDiff = (numsList[len(numsList) - 1] - numsList[0]) / (N - 1)
    # this list includes indexes we are considering - we always have ends
    ilist = [0, len(numsList)-1]
    reinitnum = 100

    #Reinitialization similar to k-means - around 100% accuracy.
    #reinitnum = (len(numsList) * N) * 2

    for i in range(reinitnum): #number of different initializations
        ilistcpy = ilist[:]
        ilistcpy += random.sample(range(1,len(numsList)-1), N - 2)
        ilistcpy.sort()
        resultlist = trialSubsample(numsList, ilistcpy, diff, optimalDiff)
        resultlist.sort()
        if i == 0:
            lowestMse = mseDiff(resultlist, optimalDiff)
            lowestMseList = resultlist
        else:
            mse = mseDiff(resultlist, optimalDiff)
            if mse < lowestMse:
                lowestMse = mse
                lowestMseList = resultlist
    return (lowestMseList)
if __name__ == "__main__":
    print(optimalSubsample(list(range(100)),10))
    for i in range(2,5):
        print(optimalSubsample([0,1,2,3,4,100],i))
    print(optimalSubsample([0,33,50,66,100], 3))
    print(optimalSubsample([0,33,50,66,100], 4))
    print()

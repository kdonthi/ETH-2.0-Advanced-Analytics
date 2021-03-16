import csv 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rand
import time
import math
from EvenlySpacedNumbers import OptimalSubsampleNew
def costFunction(W, X, y):
    diff = (X.dot(W) - y)
    diffsq = diff * diff
    return (diffsq.mean(axis=0))

def gradientDescent(W, X, y, alpha, m):
    xT = X.T
    errorMat = (X.dot(W) - y)
    dCostdW = (1/m) * (xT.dot(errorMat))
    W = W - (alpha * dCostdW)
    return (W)

def mMS(x): #short for min-max scaling
    xmin = x.min()
    xmax = x.max()
    return ((x - xmin)/(xmax - xmin))

def solveForMinW(X, y):
    xT = X.T
    return (np.linalg.inv(xT.dot(X)).dot(xT.dot(y)))

def createFeatures(X): 
    x = X
    sqrtX = np.sqrt(x)
    x2 = x * x
    x3 = x * x2
    x4 = x * x3
    x5 = x * x4
    x6 = x * x5
    x7 = x * x6
    x8 = x * x7
    x9 = x * x8
    x10 = x * x9
    x11 = x * x10
    x12 = x * x11
    x13 = x * x12
    logx = np.log(x)
    sinx = np.sin(x + 3.14/2) #shifted back pi/2 because this seems to fit the model better
    xmattuple =  ([1] * X.shape[0], mMS(logx), mMS(x), mMS(x2), mMS(x3), mMS(x4), mMS(x5), mMS(x6), mMS(x7), mMS(x8), mMS(x9), mMS(x10)) #this is a tuple of columns of all the features we want to include, edit this trying different features 
    return (np.column_stack(xmattuple))
#Creates a line plot of ETH avg. price over time
with open("EthPricingData.txt") as obj:
    priceDictReader = csv.DictReader(obj, fieldnames = ["Epoch", "Start Interval", "End Interval", "Low Price", "High Price", "Avg. Price", "Last Price"])
    priceDict = {"Epoch": [], "Start Interval": [], "End Interval": [], "Low Price": [], "High Price": [], "Avg. Price": [], "Last Price": []}
    for i in priceDictReader:
        for j in i:
            if (i[j]) and j != "Start Interval" and j != "End Interval":
                priceDict[j].append(float(i[j]))
            else:
                priceDict[j].append(i[j])
    epoch = np.array(priceDict["Epoch"])
    avgPrice = np.array(priceDict["Avg. Price"])
    avgPrice = avgPrice[epoch > 0] 
    epoch = epoch[epoch > 0] #removed 0 value to make normalizing epoch easier
    #epochSubset = epoch[epoch > 500]
    #avgpriceSubset = avgPrice[epoch > 500]
    #plt.plot(epochSubset, avgpriceSubset)
    plt.title("Avg. Price Over Epoch Number")

    iterations = 0
    #Hypothesis is going to be of form (W_0)(1) + (W_1)(x) + (W_2)(x ** 2) + (W_3)(sin(x)) = h(x)
    #Training data is going to be epochs 5000 to 16000
    minEpoch = epoch.min()
    minAvgPrice = avgPrice.min()
    xtrain = epoch[(epoch >= 5000) & (epoch <= 17000)]
    xtrain -= (minEpoch - 1) #normalizing the epoch values
    xtest = epoch[(epoch > 17000)]
    xtest -= (minEpoch - 1)
    ytrain = avgPrice[(epoch >= 5000) & (epoch <= 17000)]
    ytrain -= minAvgPrice #normalizing the avg price values
    ytest = avgPrice[(epoch > 17000)]
    ytest -= minAvgPrice
    plt.xlabel("Epochs - " + str(int(minEpoch - 1)))
    plt.ylabel("Avg Price - " + str(round(minAvgPrice, 2)))
    plt.plot(xtrain, ytrain, label = "Actual")
    onesList = []
    m = xtrain.shape[0]
    for i in range(m): #size doesn't count 0 index??
        onesList.append(1)
    oneArr = np.array(onesList)
    #x = xvals / xvals.max(axis = 0)
    #x = xvals * (6.28/4000) #want 2pi rad to be approximately 2000
    xmat = createFeatures(xtrain)
    n = xmat.shape[1]
    weightlist = [rand.randint(0,0) for i in range(n)]
    weightArr = np.array(weightlist)
    alpha = 0.1
    iterList = [] #list of all iterations
    costList = [] #list of cost at each iteration
    for i in range(1,10**5):
        costList.append(costFunction(weightArr, xmat, ytrain))
        iterList.append(i)
        weightArr = gradientDescent(weightArr, xmat, ytrain, alpha, m)
    #print(costList[-1])
    iterArr = np.array(iterList)
    costArr = np.array(costList)
    Wmat = solveForMinW(xmat, ytrain)
    pred = xmat.dot(Wmat)
    print("Training cost: ", end = "")
    print(costFunction(Wmat, createFeatures(xtrain), ytrain))
    print("Testing cost: ", end = "")
    print(costFunction(Wmat, createFeatures(xtest), ytest))
    plt.plot(xtrain, pred, label = "Predicted")
    #plt.legend(loc="best")
    windowmatrix = [[i,j] for i,j in zip(xtrain.tolist(), pred.tolist())] #list of normalized epochs and their normalized predicted values
    """
    #print(weightDf)
    #print(xmat.dot(weightDf))
    """
    """
    #creating a matrix where I am averaging *windowsize* epochs at a time, 1 -> first windowsize epochs, 2 -> second windowsize epochs (no overlap)
    windowmatrix = []
    numcount = 0
    total = 0
    windowsize = 200
    epochanddollas = zip(xvals.tolist(), yvals.tolist())
    lengthXvals = len(xvals.tolist())
    for counter, i in enumerate(epochanddollas, 1):
        epoch = i[0]
        dollars = i[1]
        if numcount >= windowsize or counter == lengthXvals:
            windowmatrix[-1].append(total/numcount)
            total = 0
            numcount = 0
        if numcount == 0 and counter != lengthXvals:
            windowmatrix.append([counter])
        total += dollars
        numcount += 1

    """

    listOfIncrDecrIntervals = []
    if windowmatrix[1][1] - windowmatrix[0][1] < 0:
        decr, incr = True, False
    else:
        decr, incr = False, True
    listOfIncrDecrIntervals.append([windowmatrix[0][0]])
    #decr,incr = True, False if windowmatrix[1][0] - windowmatrix[0][0] < 0 else False, True
    for counter, epochanddollars in enumerate(windowmatrix):
        if decr and counter:
            if windowmatrix[counter-1][1] < windowmatrix[counter][1]:
                listOfIncrDecrIntervals[-1].append(windowmatrix[counter-1][0])
                listOfIncrDecrIntervals[-1].append("decr")
                listOfIncrDecrIntervals.append([windowmatrix[counter][0]])
                decr,incr = False, True
        elif incr and counter:
            if windowmatrix[counter-1][1] > windowmatrix[counter][1]:
                listOfIncrDecrIntervals[-1].append(windowmatrix[counter-1][0])
                listOfIncrDecrIntervals[-1].append("incr")
                listOfIncrDecrIntervals.append([windowmatrix[counter][0]])
                decr,incr = True, False
    listOfIncrDecrIntervals[-1].append(windowmatrix[-1][0])
    listOfIncrDecrIntervals[-1].append("incr" if incr else "decr")
    #print(listOfIncrDecrIntervals)
    for i in listOfIncrDecrIntervals:
        plt.axvline(x=i[0])
 
    xlst = []
    ylst = []
    #left inclusive, right exclusive
    for i in listOfIncrDecrIntervals:
        size = i[1] - i[0]
        print(size)
        startEpoch = i[0] + (minEpoch - 1) #denormalize these values)
        endEpoch = i[1] + (minEpoch - 1)
        reducedSize = round(size * 0.8) #reduce amount of values by 30%
        values = avgPrice[(epoch >= startEpoch) & (epoch < endEpoch)]
        values -= minAvgPrice
        valList = sorted(values.tolist())
        y = OptimalSubsampleNew.optimalSubsample(valList, reducedSize)
        if (i[2] == "decr"):
            y = y[::-1]
        ylst.extend(y)
        xlst.extend(np.linspace(i[0], i[1], reducedSize))
    xrarr = np.array(xlst)
    yrarr = np.array(ylst)
    #print(xlst)
    #print(ylst)
    if len(xlst) == len(ylst):
        print("Yay!")
    else:
        print("No!")
    plt.plot(xrarr, yrarr, label="Reduced")
    plt.legend(loc="best")
    plt.show()

    redW = solveForMinW(createFeatures(xrarr), yrarr)
    print("Reduced Training Cost: ", end = "")
    print(costFunction(redW, createFeatures(xtrain), ytrain))
    print("Reduced Testing Cost: ", end = "")
    print(costFunction(redW, createFeatures(xtest), ytest))



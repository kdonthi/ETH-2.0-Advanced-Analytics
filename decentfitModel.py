import csv 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rand
import time

def costFunction(W, X, y):
    diff = (X.dot(W) - y)
    diffsq = diff * diff
    return (diffsq.sum(axis = 0))

def gradientDescent(W, X, y, alpha, m):
    xT = x.T
    errorMat = (X.dot(W) - y)
    dCostdW = (1/m) * (xT.dot(errorMat))
    W = W - (alpha * dCostdW)
    return (W)


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
    epochSubset = epoch[epoch > 500]
    avgpriceSubset = avgPrice[epoch > 500]
    #plt.plot(epochSubset, avgpriceSubset)
    #plt.xlabel("Epoch Number")
    #plt.ylabel("Avg. Price")
    #plt.title("Avg. Price Over Epoch Number")
    #plt.show()

    iterations = 0
    #Hypothesis is going to be of form (W_0)(1) + (W_1)(x) + (W_2)(x ** 2) + (W_3)(sin(x)) = h(x)
    #Training data is going to be epochs 5000 to 16000
    minEpoch = epoch.min()
    minAvgPrice = avgPrice.min()
    xvals = epoch[(epoch >= 5000) & (epoch <= 16000)]
    xvals = xvals - (minEpoch - 1) #normalizing the epoch values
    yvals = avgPrice[(epoch >= 5000) & (epoch <= 16000)]
    yvals = yvals - minAvgPrice #normalizing the avg price values

    plt.plot(xvals, yvals, label = "Actual")
    onesList = []
    for i in range(xvals.shape[0]): #size doesn't count 0 index??
        onesList.append(1)
    oneArr = np.array(onesList)
    print(oneArr.size)
    print(xvals.shape)
    print(xvals[0:3])
    x = xvals
    m = x.shape[0]
    xsq = x * x
    xlogx = np.log(x) * x
    sinx = np.sin(x)
    xmattuple = (oneArr, x, xsq, sinx)
    xmat = np.column_stack(xmattuple)
    print(xmat[0:3])
    
    weightlist = []
    for i in range(xmat.shape[1]):
        weightlist.append(rand.randint(-1,1)) #how to randomly initialize?
    weightArr = np.array(weightlist)
    alpha = 10 ** -13
#alpha = 10 ** -16
    iterList = []
    costList = []
    for i in range(1,10**5):
        costList.append(costFunction(weightArr, xmat, yvals))
        iterList.append(i)
        weightArr = gradientDescent(weightArr, xmat, yvals, alpha, m)
    iterArr = np.array(iterList)
    print(len(iterList), len(costList))
    costArr = np.array(costList)
    #pred = xmat.dot(weightArr)
    print(iterArr)
    print(costArr)
    print(weightArr)
    #plt.plot(iterArr, costArr, label="cost over iterations")
    pred = xmat.dot(weightArr)
    plt.plot(xvals, pred, label = "predicted")
    plt.legend(loc="best")
    plt.show()
    """
    #print(weightDf)
    #print(xmat.dot(weightDf))
    """

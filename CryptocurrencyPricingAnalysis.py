import csv
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rand
import time
import math
from datetime import datetime
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

def forwardProp(X1, W1, W2):
    X2 = (W1.T).dot(X1)
    return ((W2.T).dot(X2))

def fp2(X1, W1_2, W2_3):
    X2 = X1.dot(W1_2)
    X3 = X2.dot(W2_3)
    return(X2, X3)

def RELU(x):
    x[(x < 0)] = 0
    return (x)
    
def backProp(Xmat, Ymat, W1_2, W2_3, alpha):
    #X2 = (W1.T).dot(X1.T) #X is m x n1 originally and W1 is n1 * n2 originally
    for i in range(1, Xmat.shape[0]):
        Xvec = Xmat[i,:]
        Xvec = Xvec.reshape((-1,1))
        X2 = (W1_2.T).dot(Xvec)
        X3 = (W2_3.T).dot(RELU(X2))
        delta = (RELU(X3) - Ymat[i,0]) #W2 is n2*n3 orignally X2 is n2 * m (n3 = 1) (does order matter?)
        dCostdW2 = X2 * delta #Havermand product
        dCostdW1 = (Xvec*delta).dot(W2_3.T)
        W2_3 = W2_3 - alpha * dCostdW2
        W1_2 = W1_2 - alpha * dCostdW1
    return (W2_3, W1_2)

def neuralNetwork(X, y, N, alpha):
    #3 layered NN with input units the size of N, hidden layer size of N+1, and output layer size of 1; linear activation function
    W1_2 = 2*np.random.random((X.shape[1], N)) - 1 #size X features * size(hidden layer), 2 * [0,1) - 1 ==> [-1,1)
    W2_3 = 2*np.random.random((N, 1)) - 1 #size (hidden layer) * (1)
    y = y.reshape((-1,1)) #neat way to turn row vector into column vector
    for i in range(50):
        print("Iteration: " + str(i))
        W2_3, W1_2 = backProp(X, y, W1_2, W2_3, alpha)
    print("Cost: ")
    print((0.5 * (fp2(X, W1_2, W2_3)[1] - y) ** 2).mean())
    print("FINISHED")
    return (fp2(X, W1_2, W2_3)[1])

def createFeatures(X, weekday): 
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
    wkd = weekday
    wkd2 = weekday * weekday
    xmattuple =  ([1] * X.shape[0], mMS(logx), mMS(x), mMS(x2), mMS(x3), mMS(x4), mMS(x5), mMS(x6), mMS(x7), mMS(x8), mMS(x9), mMS(x10), mMS(wkd), mMS(wkd2)) #tuple of features 
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
    try:
        reducePercent = float(sys.argv[1])
        if reducePercent > 0.95 or reducePercent < 0:
            print("This program works best when amount of data to reduce is >= 0.2 and <= 0.95 and only if there is one argument.")
            exit()
        if len(sys.argv) != 2:
            raise Exception
    except Exception as e:
        print("Your first argument is a decimal representing the fraction of data to reduce in the reduced model. This value can be from 0.2 <= x <= 0.95.")
        exit()

    epoch = np.array(priceDict["Epoch"])
    avgPrice = np.array(priceDict["Avg. Price"])
    startInt = np.array(priceDict["Start Interval"])
    for i in (range(startInt.shape[0])):
        num = (datetime.strptime(startInt[i],"%Y-%m-%dT%H:%M:%SZ").weekday())
        startInt[i] = num
    startInt = startInt.astype("int32")

    startInt -= 5 #4 is "Friday"
    startInt = np.square(startInt) #calculating distance in days from Friday squared
    avgPrice = avgPrice[epoch > 0] 
    startInt = startInt[epoch > 0]
    epoch = epoch[epoch > 0] #removed 0 value to make normalizing epoch easier
    plt.title("Avg. Price Over Epoch Number")

    iterations = 0
    #Hypothesis is going to be of form (W_0)(1) + (W_1)(x) + (W_2)(x ** 2) + (W_3)(sin(x)) = h(x)
    #Training data is going to be epochs 5000 to 17000
    minEpoch = epoch.min()
    minAvgPrice = avgPrice.min()
    xtrain = epoch[(epoch >= 5000) & (epoch <= 17000)]
    xtrain -= (minEpoch - 1) #normalizing the epoch values
    weekdayTrain = startInt[(epoch >= 5000) & (epoch <= 17000)]
    xtest = epoch[(epoch > 17000)]
    xtest -= (minEpoch - 1)
    weekdayTest = startInt[(epoch > 17000)]
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
    xmat = createFeatures(xtrain, weekdayTrain)
    weightlist = [rand.randint(0,0) for i in range(xmat.shape[1])]
    weightArr = np.array(weightlist)
    alpha = 0.1
    iterList = [] #list of all iterations
    costList = [] #list of cost at each iteration
    for i in range(1,10**5):
        costList.append(costFunction(weightArr, xmat, ytrain))
        iterList.append(i)
        weightArr = gradientDescent(weightArr, xmat, ytrain, alpha, m)
    iterArr = np.array(iterList)
    costArr = np.array(costList)
    Wmat = solveForMinW(xmat, ytrain)
    pred = xmat.dot(Wmat)
    print("Full Data Training cost: ", end = "")
    print(costFunction(Wmat, createFeatures(xtrain, weekdayTrain), ytrain))
    print("Full Data Testing cost: ", end = "")
    print(costFunction(Wmat, createFeatures(xtest, weekdayTest), ytest))
    #nnwpred = neuralNetwork(xmat, ytrain, xmat.shape[1] + 7, 0.0001) #a neural network method to find line of fit - was too straight for some reason
    plt.plot(xtrain, pred, label = "Full Data") #change pred to nnwpred to see neural network and uncomment next two lines of code
    #plt.show()
    #exit()
    windowmatrix = [[i,j] for i,j in zip(xtrain.tolist(), pred.tolist())] #list of normalized epochs and their normalized predicted values
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
    daylst = []
    #left inclusive, right exclusive
    for i in listOfIncrDecrIntervals:
        size = i[1] - i[0]
        startEpoch = i[0] + (minEpoch - 1) #denormalize these values)
        endEpoch = i[1] + (minEpoch - 1)
        #reducedSize = round(size * 0.8) #reduce amount of values by 30%
        values = avgPrice[(epoch >= startEpoch) & (epoch < endEpoch)]
        values -= minAvgPrice
        valList = sorted(values.tolist())
        reducedSize = round(len(valList) * (1 - reducePercent))
        if i[1] > i[0]:
            y = OptimalSubsampleNew.optimalSubsample(valList, reducedSize)
            if (i[2] == "decr"):
                y = y[::-1]
            ylst.extend(y)
            xinterval = (np.linspace(i[0], i[1], reducedSize))
            daylst.extend((startInt[(np.round(xinterval - epoch.min())).astype("int32")]).tolist())
            xlst.extend(xinterval)
    xrarr = np.array(xlst)
    yrarr = np.array(ylst)
    dayarr = np.array(daylst)
    if len(xlst) == len(ylst) and len(xlst) == len(daylst):
        print("Number of Values in Reduced X and Y and day vectors are same.")
    else:
        print("Number of Values in Reduced X and Y and day vectors are NOT the same. Please check the code for any errors.")
    xmat2 = createFeatures(xrarr, dayarr)
    redW = solveForMinW(xmat2, yrarr)
    print("Reduced Data Training Cost: ", end = "")
    print(costFunction(redW, createFeatures(xtrain, weekdayTrain), ytrain))
    print("Reduced Data Testing Cost: ", end = "")
    print(costFunction(redW, createFeatures(xtest, weekdayTest), ytest))
    pred2 = xmat2.dot(redW)
    plt.plot(xrarr, pred2, label="Reduced by {}".format(round(reducePercent, 2)))
    plt.legend(loc="best")
    plt.show()


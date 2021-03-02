import csv
import requests
import random
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

def plotfunc(validatorindex, plot=1):
    #Plots the avg. inclusion of the validator associated with the "validatorindex"; plot=0 ==> don't plot, just return avg inclusion distance; plot=1 ==> plot & return
    requrl = "https://beaconcha.in/api/v1/validator/{}/attestations".format(validatorindex) 
    output = requests.get(requrl)
    outputJson = output.json()
    totalIncDist = 0
    numepochs = 0
    while True:
        try:
            for i in outputJson["data"]:
                if i['status'] == 1:
                    totalIncDist += i['inclusionslot'] - i['attesterslot']
                    numepochs += 1
        except Exception as e:
            continue
        else:
            break
    if (numepochs):
        if plot:
            plt.axvline(x = (totalIncDist / numepochs))
        return (totalIncDist / numepochs)
    else:
        return (-1)

def plotHistogram(chooseVal, validatorIndex):
    #If you do not give any parameters, the default is that 10 randomly chosen validators are plotted and no validator is compared to the randomly chosen validators.
    #This function creates a histogram of the avg. inclusion distance over the last 100 epochs of the number of randomly chosen validators from all the possible validators given in "chooseVal" and compares the
    #avg inclusion distance of the validator in validatorIndex to the other validators. 
    base16list = []
    with open("indices.csv", "r") as fobj:
        lol = csv.reader(fobj)
        counter = 0
        for i in lol:
            base16list.append(i[1])

    dfdict = {"Inclusion Distance": []}
    numVal = len(base16list)
    #chooseVal = 10 #how many validators' data we want
    finishedVal = 0 #how many validators we have finished
    workingVal = 0 #how many validators have calls that are working
    valIndList = list(range(numVal)) #the list of the indices validators we have gone through
    valCounter = 0
    retryCall = 5
    while workingVal < chooseVal and finishedVal < numVal:
        #print(i)
        print("%i"  % workingVal)
        valCounter += 1
        i = random.randint(0, numVal - 1)
        reqURL = "https://beaconcha.in/api/v1/validator/%s/attestations" % base16list.pop(i)
        numVal -= 1
        tryCounter = 0
        epochs = 0 #amount of epochs we are getting info for
        totalID = 0 #total Inclusion Distance (ID)
        while True:
            boolendtry = 0
            try:
                get = (requests.get(reqURL)).json()
                for j in get["data"]:
                    if j["status"] == 1:
                        attesterslot = int(j["attesterslot"])
                        inclusionslot = int(j["inclusionslot"])
                        totalID += (inclusionslot - attesterslot)
                        epochs += 1
            except Exception as e:
                tryCounter += 1
                if (tryCounter >= retryCall): #set amount of times to try to get the information of a validator
                    break
            else:
                break
        if epochs != 0:
            dfdict["Inclusion Distance"].append(totalID / epochs)
            workingVal += 1 #working validator is one that doesn't return an error and has epoch we are getting info about
        finishedVal += 1
    if finishedVal == numVal:
        print("You are out of validators to pick; either reduce the number of people you want to choose, increase the number of times you want to retry a call, or if you are sure neither of those is the problem, just retry again..")

    df = pd.DataFrame(dfdict)
    incDistList = dfdict["Inclusion Distance"]
    hist = df["Inclusion Distance"].plot.hist(bins=10)
    plt.xlabel("Inclusion Distance")
    plt.title("Histogram of Inclusion Distance For Random %i Validators" % workingVal)
    avgvalue = plotfunc(validatorIndex)
    print(avgvalue)
    plt.show()

    numAbove = 0
    numEqorAbove = 0
    print(sorted(dfdict["Inclusion Distance"], reverse = True))
    if avgvalue != -1:
        for i in sorted(dfdict["Inclusion Distance"],reverse = True):
            if avgvalue < i:
                numAbove += 1
                numEqorAbove += 1
            if avgvalue == i:
                numEqorAbove += 1
        avgpercentiles = (((numAbove + numEqorAbove)/2)/chooseVal) * 100
        print("Validator {} is in the {}th percentile of {} randomly chosen people.".format(validatorIndex, round(avgpercentiles, 2), chooseVal)) #percentile is average of percentiles from percents of higher avg. inclusion distances and higher than or equal inclusion distances


def main(): #first argument is number of Validators and second argument is validator index
    arglen = len(sys.argv)
    assert(arglen == 3)
    numberOfRandVals = int(sys.argv[1])
    valIndex = sys.argv[2]
    plotHistogram(numberOfRandVals, valIndex)

main()
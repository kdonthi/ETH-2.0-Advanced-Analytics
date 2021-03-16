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
def avgInclusionDistance(reqURL, retryCall):
    totalID = 0
    epochs = 0
    tries = 0
    while True:
        try:
            output = requests.get(reqURL).json()
            #print(len(output["data"])) #use this to see how many data entries you get for each validator
            for j in output["data"]:
                if j["status"] == 1:
                    attesterslot = int(j["attesterslot"])
                    inclusionslot = int(j["inclusionslot"])
                    totalID += (inclusionslot - attesterslot)
                    epochs += 1
        except Exception as e:
            if (tries >= retryCall):
                return (-1)
            tries += 1
        else:
            if epochs:
                return (totalID / epochs)
            else:
                return (-1) #if number of epochs is 0
def plotHistogram(chooseVal, validatorIndex, retryCall=5):
    #If you do not give any parameters, the default is that 10 randomly chosen validators are plotted and no validator is compared to the randomly chosen validators.
    #This function creates a histogram of the avg. inclusion distance over the last 100 epochs of the number of randomly chosen validators from all the possible validators given in "chooseVal" and compares the avg inclusion distance of the validator in validatorIndex to the other validators. 
    
    base16list = [] #contains the validator indexes in the csv file we are parsing
    with open("indices.csv", "r") as fobj:
        lol = csv.reader(fobj)
        counter = 0
        for i in lol:
            base16list.append(i[1])
            if i[0] == (validatorIndex):
                validatorID = i[1]
    #print(base16list[:3])
    dfdict = {"Inclusion Distance": []}
    numVal = len(base16list)
    #chooseVal = 10 #how many validators' data we want
    finishedVal = 0 #how many validators we have finished
    workingVal = 0 #how many validators have calls that are working
    valCounter = 0
    while workingVal < chooseVal and finishedVal < numVal:
        print("%i"  % (workingVal + 1))
        valCounter += 1
        i = random.randint(0, numVal - 1)
        reqURL = "https://beaconcha.in/api/v1/validator/%s/attestations" % base16list.pop(i)
        numVal -= 1
        avgInclDist = avgInclusionDistance(reqURL, retryCall)
        if avgInclDist != -1:
            dfdict["Inclusion Distance"].append(avgInclDist)
            workingVal += 1 #working validator is one that doesn't return an error and has epoch we are getting info about
        finishedVal += 1

    if finishedVal == numVal:
        print("You are out of validators to pick; either reduce the number of people you want to choose, increase the number of times you want to retry a call, or if you are sure neither of those is the problem, just run the program again.")
    if validatorID in base16list:
        reqURL = "https://beaconcha.in/api/v1/validator/%s/attestations" % validatorIndex
        avgInclDist = avgInclusionDistance(reqURL, float("inf")) #don't stop calls until we get value for validatorIndex
        dfdict["Inclusion Distance"].append(avgInclDist)

    df = pd.DataFrame(dfdict)
    incDistList = dfdict["Inclusion Distance"]
    hist = df["Inclusion Distance"].plot.hist(bins=10)
    plt.xlabel("Inclusion Distance")
    plt.title("Histogram of Inclusion Distance For Random %i Validators" % workingVal)
    plt.ylim(0, workingVal + 1)
    avgvalue = plotfunc(validatorIndex)
    print("Average Inclusion Distance of Validator %s: " % validatorIndex +  str(avgvalue))
    plt.show()

    numAbove = 0
    numEqorAbove = 0
    #print(sorted(dfdict["Inclusion Distance"], reverse = True))
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
    begin = time.time()
    arglen = len(sys.argv)
    assert(arglen == 3 or arglen == 4)
    numberOfRandVals = int(sys.argv[1])
    valIndex = sys.argv[2]
    if arglen == 4:
             call = int(sys.argv[3])
    assert(numberOfRandVals >= 0 and numberOfRandVals <= 87750)
    assert(int(valIndex) >= 0 and int(valIndex) <= 87749)
    if arglen == 3:
        plotHistogram(numberOfRandVals, valIndex)
    elif arglen == 4:
        assert(call >= 1)
        plotHistogram(numberOfRandVals, valIndex, call)
    end = time.time()
    #print(end - begin)

main()

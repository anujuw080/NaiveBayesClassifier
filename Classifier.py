import csv
import math


def getDataFromCsv(fileName):

    tempRowList = []
    finalData = []
    # Retrieve data from CSV
    data = list(csv.reader(open(fileName)))
    rowsNumber = len(data)
    colNumber = len(data[0])
    for i in range(0, rowsNumber):
        for j in range(0, colNumber):
            tempRowList.append(int(data[i][j]))
        finalData.append(tempRowList)
        tempRowList = []

    return finalData


def learner(csvName, beta):
        # LEARNING PHASE STARTS HERE
    # Retrieve Data from csv
    finalData = getDataFromCsv(csvName)
    #print(finalData)

    probabilityList = []

    # START : Get the TOTAL number of words
    rows = len(finalData)
    cols = len(finalData[0])
    wordTotal = 0

    for i in range(0, rows):
        for j in range(0, cols):
            wordTotal = wordTotal + finalData[i][j]
    # END

    # Since there are 5822 distinct words in the vocabulary,
    # we can have a constant value for denominator
    probabiltyDenominator = wordTotal

    # START :Calculate probability of each word
    # , i.e. frequency of each word
    # print("PROBABILITIES!!")
    freqCount = 0
    for i in range(0, cols):
        for j in range(0, rows):
            freqCount = freqCount + finalData[j][i]
        wordProbability = math.log1p((freqCount + beta)/(probabiltyDenominator + 2*beta))
        probabilityList.append(wordProbability)
        freqCount = 0
    # END

    return probabilityList


def predictor(filename, probBaseBallList, probHocketList, probBaseBall, probHockey):
    # START  PREDICTION HERE
    baseballTestData = getDataFromCsv(filename)
    rows = len(baseballTestData)
    # rows = 10
    cols = len(baseballTestData[0])
    predictedBaseballList = []
    totalProbability = math.log1p(probBaseBall)
    for i in range(0, rows):
        for j in range(0, cols):
            totalProbability = totalProbability + baseballTestData[i][j]*(probBaseBallList[j])
        predictedBaseballList.append(totalProbability)
        totalProbability = math.log1p(probBaseBall)
    print(predictedBaseballList)
    print("-------------------------------------------------------------")
    # PART -2
    hockeyTestData = getDataFromCsv(filename)
    rows = len(hockeyTestData)
    # rows = 10
    cols = len(hockeyTestData[0])
    predictedHockeyList = []
    totalProbability2 = math.log1p(probHockey)
    for i in range(0, rows):
        for j in range(0, cols):
            totalProbability2 = totalProbability2 + hockeyTestData[i][j]*(probHocketList[j])
        predictedHockeyList.append(totalProbability2)
        totalProbability2 = math.log1p(probHockey)
    print(predictedHockeyList)
    print("-------------------------------------------------------------")

    
    numberOfDocs = len(predictedBaseballList)
    predictedClasses = []
    for i in range(0, numberOfDocs):
        if (predictedBaseballList[i] >= predictedHockeyList[i]):
            predictedClasses.append(1)
        else:
            predictedClasses.append(0)

    return predictedClasses


def classifier():

    # We use probabilities 0.5 since there are 50 cases for each
    probBaseBall = 0.5
    probHockey = 0.5

    # Halucinated value Beta
    beta = 4

    # Correct predictions
    correct1 = 0
    correct2 = 0
    probBaseBallList = learner("baseball_train_set.csv", beta)
    probHocketList = learner("hockey_train_set.csv", beta)
    predictedList = predictor("baseball_test_set.csv", probBaseBallList, probHocketList, probBaseBall, probHockey)
    size = len(predictedList)
    for i in range(0, size):
        if(predictedList[i] == 1):
            print("BASEBALL predicted")
            correct1 = correct1 + 1
        else:
            print("HOCKEY predicted")

    print("DONE WITH FIRST TEST SAMPLE")
    print("------------------------------------------")
    print("------------------------------------------")
    predictedList2 = predictor("hockey_test_set.csv", probBaseBallList, probHocketList, probBaseBall, probHockey)
    size = len(predictedList2)
    for i in range(0, size):
        if(predictedList2[i] == 1):
            print("BASEBALL predicted")
        else:
            print("HOCKEY predicted")
            correct2 = correct2 + 1
    print("DONE WITH FIRST SECOND SAMPLE")
    print("------------------------------------------")
    print("------------------------------------------")

    efficiency1 = (correct1 / 50) * 100
    efficiency2 = (correct2 / 50) * 100
    efficiency = (efficiency1 + efficiency2) / 2
    print("Efficiency is: " + str(efficiency1) + " AND " + str(efficiency2))


classifier()

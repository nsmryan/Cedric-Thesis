import numpy
import os
import math
from matplotlib import pyplot as plt
from CrayfishLib import *
import sys
import math


def recordingSessionLengths(savingLengths):
  outFileName = "recordingTime"
  shortestRecordingTime = 100000000

  for sessionName in sessionNames:
    if savingLengths:
      recordingTimeFile = open(outFileName + "_" + sessionName + ".txt", 'w')
      recordingTimeFile.write("Trial-CrayfishID, Samples, Recording Time (seconds)" + "\n")

    for trialName in trialNames:
      crayfishIndex = 1
      for crayfishIndex in range(0, numCrayfish):
        refinedData = retrieveData(trialName, sessionName, crayfishIndex)
        identifier = trialName + "-" + str(crayfishIndex+1)
        recordingTime = refinedData[-1].time
        shortestRecordingTime = min(shortestRecordingTime, recordingTime)
        
        if savingLengths:
          outLine = ",".join([identifier, str(len(refinedData)), str(recordingTime)])
          recordingTimeFile.write(outLine + "\n")

  return shortestRecordingTime

def retrieveData(trial, session, crayfish):
  path = ".\\output\\" + trial + "\\"
  dataFiles = [name for name in os.listdir(path) if (session + "_") in name and ("_" + str(crayfish)) in name]

  fileName = dataFiles[0]

  lines = list(open(path + fileName, 'r').read().split('\n'))
  lines = lines[1:]

  refinedData = [toRefined(line.split(',')) for line in lines if len(line) > 0]

  return refinedData

def toRefined(vals):
  floats = [float(val) for val in vals[0:-1]]
  location = vals[-1].strip()
  return Crayfish(floats[0], floats[1], floats[2], floats[3], floats[4], floats[5], floats[6], floats[7], floats[8], location)


def processInSegments(name, xLabel, yLabel, timeSegment, collapse):
  outDirectory = outDir + "\\" + name + "_" + str(timeSegment) + "\\"
  ensureDir(outDirectory)
  outFileName = outDirectory + name

  for sessionName in sessionNames:
    allDataOutFile = open(outFileName + "_" + sessionName, 'w')
    allDataOutFile.write(anovaHeader + name + "\n")

    for trialName in trialNames:
      trialOutFile = open(outFileName + "_" + trialName + "_" + sessionName, 'w')
      trialOutFile.write("0, 1, 2, 3, 4, 5, average\n")
      allMeasures = []

      for crayfishIndex in range(0, numCrayfish):
        crayfishMeasures = []
        if (trialName, sessionName, crayfishIndex) in ignoreCrayfish:
          print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n")
          continue

        headerText = "Processing " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n"
        print(headerText)

        refinedData = retrieveData(trialName, sessionName, crayfishIndex)
        endTime = max([sample.time for sample in refinedData])
        numBuckets = int(endTime / timeSegment) + 1
        sampleList = []
        [sampleList.append([]) for i in range(0, numBuckets)]
        for sample in refinedData:
          index = int(sample.time/timeSegment)
          sampleSummary = sample
          sampleList[index].append(sampleSummary)

        for (index, l) in zip(range(0, len(sampleList)), sampleList):
          if len(l) == 0:
            print("no data for " + str(index))

        summaries =  []
        for (index, sampleSegment) in zip(range(0, len(sampleList)), sampleList):
          #if index > 5:
          #  print("index = " + str(index))
          #  break
          segmentSummary = collapse(sampleSegment)
          summaries.append(segmentSummary)

          treatmentStr = "t_" + str(trialTreatments[trialName])
          timeStr = str(index)
          trialNameStr = trialName + "_" + str(crayfishIndex+1)
          segmentSummaryStr = str(segmentSummary) 
          allDataOutFile.write(treatmentStr + ", " + timeStr + ", " + trialNameStr + ", " + segmentSummaryStr + "\n")
          crayfishMeasures.append(segmentSummary)

        allMeasures.append(crayfishMeasures)
        pairs = list(zip(range(0, numBuckets), summaries))
        plotOverTime(trialName, sessionName, crayfishIndex, name, xLabel, yLabel, pairs)

      #write out summary data
      for measures in transpose(allMeasures):
        measures.append(safeAverage(measures))
        trialOutFile.write(", ".join(map(str, measures)))
        trialOutFile.write("\n")

def processOverAllSessions(name, xLabel, yLabel, collapse):
  outputDirectory = outDir + "\\" + name
  outFileName =  outputDirectory + "\\" + name + "_OverAll"
  ensureDir(outputDirectory)

  measures = []

  for sessionName in sessionNames:
    outFile = open(outFileName + "_" + sessionName, 'w')
    outFile.write("treatment, crayfishid, trial," + name + "\n")

    for trialName in trialNames:
      if trialName in ignoreTrials:
          print("Ignoring " + trialName + "\n")
          continue

      for crayfishIndex in range(0, numCrayfish):
        if (trialName, sessionName, crayfishIndex) in ignoreCrayfish:
          print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n")
          continue

        headerText = "Processing " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n"
        print(headerText)

        refinedData = retrieveData(trialName, sessionName, crayfishIndex)
        crayfishSummary = collapse(refinedData)
        #TODO match up with an id for the plot
        measures.append((str(trialName) + str(crayfishIndex+1), crayfishSummary))
        outFile.write("t_" + str(trialTreatments[trialName]) + ", " + trialName + "_" + str(crayfishIndex+1) + ", " + trialName + ", " + str(crayfishSummary) + "\n")
    #plot all values with their id

  plt.bar(range(len(measures)), [measure[1] for measure in measures], align="center")
  plt.xticks(range(len(measures)), [measure[0] for measure in measures], size="small")
  plt.xlabel("Crayfish Label")
  plt.ylabel("Average Speed")
  plt.title("Average Speed for all Crayfish")

  fig = plt.figure(1)
  fig.tight_layout()
  fig.set_size_inches(36, 24)
  plt.savefig(outFileName + "_all_avg_speeds.png")
  plt.close(fig)
  plt.clf()





def averageSpeed(samples):
  return safeAverage([sample.speed for sample in samples])

def percentStill(samples):
  numSamples = len(samples)

  if numSamples == 0:
    return 0

  numStill = 0
  for sample in samples:
    if sample.xVel == 0 and sample.yVel == 0:
      numStill += 1

  return numStill / numSamples

def percentMiddle(samples):
  numSamples = len(samples)

  if numSamples == 0:
    return 0

  numMiddle = 0
  for sample in samples:
    if "middle" in sample.location:
      numMiddle += 1

  return numMiddle / numSamples

def averageSpeedLocation(locationName):
  def averageSpeedNamed(samples):
    filteredSamples = [sample for sample in samples if sample.location == locationName]
    return safeAverage([sample.speed for sample in filteredSamples])

  return averageSpeedNamed

def intoIncrementsOf(samples, f, incrementDuration):
  if len(samples) == 0:return []
  endTime = max([sample.time for sample in samples])
  numBuckets = int(endTime / incrementDuration) + 1
  sampleList = []
  [sampleList.append([]) for i in range(0, numBuckets)]

  for sample in samples:
    index = int(sample.time/incrementDuration)
    sampleList[index].append(sample)

  for (index, l) in zip(range(0, len(sampleList)), sampleList):
    if len(l) == 0:
      print("no data for " + str(index))

  return list(map(f, sampleList))

def makeIncrementDataSet(name, timeIncrement, summarizeIncrement, combineIncrements):
  outDirectory = "datasets\\" + name + "\\"
  ensureDir(outDirectory)
  outFileName = outDirectory + name

  for location in allLocations:

    for sessionName in sessionNames:
      allDataOutFile = open(outFileName + "_incrementsOf" + str(timeIncrement) + "_seconds_" + sessionName + ".csv", 'w')
      allDataOutFile.write(name + " 0.0, " + name + " 0.5, " + name + " 5.0, " + name + " 50.0" + "\n")

      sessionData = []

      for treatmentName in treatmentNames:
        treatmentData = []

        for trialName in treatmentTrials[treatmentName]:

          for crayfishIndex in range(0, numCrayfish):
            if (trialName, sessionName, crayfishIndex) in ignoreCrayfish:
              print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n")
              continue

            refinedData = retrieveData(trialName, sessionName, crayfishIndex)
            dataSet = filterByLocation(location, refinedData)
            incrementValues = intoIncrementsOf(dataSet, summarizeIncrement, timeIncrement)
            treatmentData.append(incrementValues)

        incrementData = list(map(combineIncrements, transpose(treatmentData)))
        sessionData.append(incrementData)

      transposedData = transpose(sessionData)
      fileData = transposedData 
      for row in fileData:
        allDataOutFile.write((",".join(map(str, row))) + "\n")

def splitAtTime(samples, timeCutoff):
  return [[sample for sample in samples if  sample.time < timeCutoff],
          [sample for sample in samples if sample.time >= timeCutoff and sample.time < (timeCutoff * 2)]]

def dataRow(trialName, crayfishIndex, val, session = None, splitIndex = None):
    dataStr  = "t_" + str(trialTreatments[trialName])
    if splitIndex != None: dataStr += "_part_" + str(splitIndex)
    dataStr += ", " + trialName + "_" + str(crayfishIndex+1)
    #dataStr += ", " + trialName
    dataStr += ", " + str(val) + "\n"
    return dataStr

def dataHeader(name):
    return "treatment, crayfishid, " + name + "\n"

def makeDataSets(fileName, f, proj, timeCutoff = None):
  outDir = "datasets\\" + fileName + "\\"
  outPath = outDir + fileName
  ensureDir(outDir)
  experimentFile = open(outPath + "_all_samples.csv", 'w')
  experimentFile.write(dataHeader(fileName))

  for location in allLocations:

    for sessionName in sessionNames:

      if location != "all":
        outFileName = outPath + "_" + location + "_" + sessionName + ".csv"
      else:
        outFileName = outPath + "_" + sessionName + ".csv"
      outFile = open(outFileName, 'w')
      sessionFile = open(outPath + "_all_samples_session_" + sessionName + ".csv", 'w')
      sessionFile.write(dataHeader(fileName))

      if (timeCutoff == None or 'a' in sessionName):
        header = "crayfish index (0.0), 0.0, crayfish index (0.5), 0.5, crayfish index (5.0), 5.0, crayfish index (50.0), 50.0\n"
      else:
        header = "crayfish index (0.0), 0.0 (first part), 0.0 (second part), crayfish index (0.5), 0.5 (first part), 0.5 (second part), crayfish index (5.0), 5.0 (first part), 5.0 (second part), crayfish index (50.0), 50.0 (first part), 50.0 (second part)\n"
      outFile.write(header)

      allData = []
      for treatmentName in treatmentNames:
        treatmentData = []
        treatmentDataSecondPart = []
        crayfishIdentifiers = []
        population = []
        populationSecondPart = []

        for trialName in treatmentTrials[treatmentName]:
          trialData = []
          trialDataSecondPart = []
          if trialName in ignoreTrials:
              print("Ignoring " + trialName + "\n")
              continue

          for crayfishIndex in range(0, numCrayfish):
            if (trialName, sessionName, crayfishIndex) in ignoreCrayfish:
              print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n")
              continue

            refinedData = retrieveData(trialName, sessionName, crayfishIndex)
            dataSet = filterByLocation(location, refinedData)
            if (timeCutoff == None):
              extracted = proj(dataSet)
              val = f(extracted)
              sampleStr = dataRow(trialName, crayfishIndex, val)
              experimentFile.write(sampleStr)
              sessionFile.write(sampleStr)
              trialData.append(val)
              population += extracted
            else:
              splitDataSets = splitAtTime(dataSet, timeCutoff)
              extracted = list(map(proj, splitDataSets))
              vals = list(map(f, extracted))

              sampleStr  = dataRow(trialName, crayfishIndex, vals[0], 0)
              sampleStr2 = dataRow(trialName, crayfishIndex, vals[1], 1)

              experimentFile.write(sampleStr)
              experimentFile.write(sampleStr2)
              sessionFile.write(sampleStr)
              sessionFile.write(sampleStr2)

              trialData.append(vals[0])
              treatmentDataSecondPart.append(vals[1])
              population += extracted[0]
              populationSecondPart += extracted[1]

          identifiers = [trialName + "-" + str(ix) for ix in indexRange]
          crayfishIdentifiers += identifiers
          treatmentData += trialData
          if (timeCutoff != None): treatmentDataSecondPart += trialDataSecondPart

        # add stderr
        treatmentData.append(numpy.std(population)/math.sqrt(len(population)))
        if (timeCutoff != None):
          treatmentDataSecondPart.append(numpy.std(populationSecondPart)/math.sqrt(populationSecondPart))
        crayfishIdentifiers.append("sterr")

        # add min
        treatmentData.append(min(population))
        if (timeCutoff != None):
          treatmentDataSecondPart.append(min(populationSecondPart))
        crayfishIdentifiers.append("min")

        # add max
        treatmentData.append(max(population))
        if (timeCutoff != None):
          treatmentDataSecondPart.append(max(populationSecondPart))
        crayfishIdentifiers.append("max")

        allData.append(crayfishIdentifiers)
        allData.append(treatmentData)
        if (timeCutoff != None):allData.append(treatmentDataSecondPart)

      transposedData = transpose(allData)
      fileData = transposedData
      for row in fileData:
        outFile.write((",".join(map(str, row))) + "\n")

def makeLocationDataSets(fileName, f):
  outDir = "datasets\\"
  outPath = outDir + fileName
  ensureDir(outDir)

  sessionData = []

  for sessionName in sessionNames:
    outFile = open(outPath + "_" + sessionName + ".csv", 'w')
    header = "0.0, 0.5, 5.0, 50.0\n"
    outFile.write(header)

    for location in locationNames:
      treatmentData = []
      for treatmentName in treatmentNames:
        crayfishData = []
        for trialName in treatmentTrials[treatmentName]:
          for crayfishIndex in range(0, numCrayfish):
            refinedData = retrieveData(trialName, sessionName, crayfishIndex)
            val = f(location, refinedData)
            crayfishData.append(val)
        treatmentData.append(safeAverage(crayfishData))

      outFile.write(location + ", " + (",".join(map(str, treatmentData))) + "\n")

def filterByLocation(location, dataSet):
  return list(filter(lambda sample : sample.location == location or location == "all", dataSet))

def avgSpeedLocation(location, crayfishData):
  return averageSpeed(filterByLocation(location, crayfishData))

def totalDistLocation(location, crayfishData):
  return calCTotalDistance(filterByLocation(location, crayfishData))

def timeSpentLocation(location, crayfishData):
  numSamples = len(crayfishData)

  if numSamples == 0:
    return 0

  numMiddle = 0
  for sample in crayfishData:
    if location in sample.location:
      numMiddle += 1

  return numMiddle / numSamples

def pauseDurations(samples):
  prevSample = samples[0]
  timePaused = 0
  pausing = False
  pausedTimeList = []

  for sample in samples[1:]:
    if location == "all":
      if sampleDist(prevSample, sample) < speedThreshold:
        pausing = True
        timePaused += sampleTimePassed(prevSample, sample)
      else:
        pausing = False
        if timePaused != 0:
          pausedTimeList.append(timePaused)
        timePaused = 0
    prevSample = sample

  #in case the crayfish ended the session pausing
  if timePaused != 0 and timePaused < pauseThreholdHigh: 
    pausedTimeList.append(timePaused)

  return pausedTimeList

def averageTimePaused(location, samples):
  return safeAverage(pauseDurations(samples, location))

def averageTimePausedLocation(location):
  def timePausedFunction(samples):
    return averageTimePaused(location, samples)
  return timePausedFunction

def timePausedLocation(location):
  def timePausedFunction(samples):
    return pauseDurations(samples, location)
  return timePausedFunction

def totalDistanceLocation(location):
  def totalDistance(samples):
    totalDistance = 0
    prevSample = samples[0]
    for sample in samples[1:]:
      if location == "all" or (sample.location == location and prevSample.location == location):
        totalDistance += sampleDist(prevSample, sample)
      prevSample = sample
    return totalDistance
  return totalDistance

def getSpeeds(samples):
  return [sample.speed for sample in samples]

def getSpeedsWalking(samples):
  return [sample.speed for sample in samples if sample.speed > speedThreshold]

def averageSpeedWalking(samples):
  return safeAverage(getSpeedsWalking(samples))

def getDistances(samples):
  return [sum([sampleDist(sample0, sample1) for (sample0, sample1) in zip(samples[0:-1], samples[1:])])]

def forwardDirectivenessRatio(samples):
  result = 0

  if (len(samples) == 0): return 0

  distanceWalked = calCTotalDistance(samples)
  distanceDisplaced = sampleDist(samples[0], samples[-1])

  if (distanceDisplaced > 0):
    result = distanceDisplaced/distanceWalked

  return result

# TODO make structure of data set information (name, proj, summaryFunction)
#map over them
#all locations to increment data sets
def postprocess():
  #Data sets for R statistics

  #processInSegments("AverageSpeed", "Time", "AverageSpeed", 60, averageSpeed)
  #processInSegments("Location", "Time", "Location", 60, percentMiddle)
  #processOverAll("LocationOverAll", "Crayfish ID", "Location", percentMiddle)
  
  #Average Time Paused
  #processOverAllSessions("AvgTimePausedOverAll",   "Crayfish ID", "AverageTimePaused", averageTimePausedLocation("all"))
  #processOverAllSessions("AvgTimePausedMiddle", "Crayfish ID", "AverageTimePaused", averageTimePausedLocation("middle"))
  #processOverAllSessions("AvgTimePausedEdge",   "Crayfish ID", "AverageTimePaused", averageTimePausedLocation("edge"))
  #processOverAllSessions("AvgTimePausedCorner", "Crayfish ID", "AverageTimePaused", averageTimePausedLocation("corner"))

  #distanceTraveledAllCrayfish()

  #Average Speed
  #processOverAllSessions("AverageSpeedOverAll", "Crayfish ID", "AverageSpeed", averageSpeed)
  #processOverAllSessions("AverageSpeedMid",    "Crayfish ID", "AverageSpeed", averageSpeedLocation("middle"))
  #processOverAllSessions("AverageSpeedEdge",   "Crayfish ID", "AverageSpeed", averageSpeedLocation("edge"))
  #processOverAllSessions("AverageSpeedCorner", "Crayfish ID", "AverageSpeed", averageSpeedLocation("corner"))

  #processInSegments("PercentStill", "Time", "PercentStill", 60, percentStill)

  #processOverAllSessions("TotalDistAll",    "Crayfish ID", "TotalDistance", totalDistanceLocation("all"))
  #processOverAllSessions("TotalDistMid",    "Crayfish ID", "TotalDistance", totalDistanceLocation("middle"))
  #processOverAllSessions("TotalDistEdge",   "Crayfish ID", "TotalDistance", totalDistanceLocation("edge"))
  #processOverAllSessions("TotalDistCorner", "Crayfish ID", "TotalDistance", totalDistanceLocation("corner"))

  # Full data set summary
  #shortestRecordingTime = recordingSessionLengths(False)

  #Data sets for graphing
  makeDataSets("avgSpeed",  safeAverage, getSpeeds)
  #makeDataSets("avgSpeedWalking",  safeAverage, getSpeedsWalking)
  #makeDataSets("averagePauseDuration_seconds",  safeAverage, pauseDurations)

  #not sure if this can be made to work
  #makeDataSets("averageForwardDirectiveness",  forwardDirectivenessRatio, distances)

  #makeDataSets("averageTimePaused", safeAverage, averageTimePaused("all"))
  #makeDataSets("totalDist_mm", sum, getDistances, shortestRecordingTime)


  #makeLocationDataSets("avgSpeedLocation", avgSpeedLocation)
  #makeLocationDataSets("totalDistLocation", totalDistLocation)
  #makeLocationDataSets("timeSpent", timeSpentLocation)

  #Data sets broken into increments
  #makeIncrementDataSet("averageSpeed_mm_per_second", 60,   averageSpeed, safeAverage)
  #makeIncrementDataSet("avgSpeedWalking", 60,   averageSpeedWalking, safeAverage)
  #makeIncrementDataSet("ForwardDirectiveness", 60,   forwardDirectiveness, safeAverage)

  #makeIncrementDataSet("avgSpeedLocation", 60*5, averageSpeed, safeAverage)
  #makeIncrementDataSet("timeSpent", 60,   timeSpentLocation)
  #makeIncrementDataSet("timeSpent", 60*5, timeSpentLocation)

if __name__ == "__main__":
  postprocess()

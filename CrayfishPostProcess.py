import numpy
import os
import math
from matplotlib import pyplot as plt
from CrayfishLib import *
import sys
import math


def recordingSessionLengths(savingLengths = False):
  outFileName = "recordingTime"
  shortestRecordingTime = 100000000
  lengthDict = {}

  for sessionName in sessionNames:
    if savingLengths:
      recordingTimeFile = open(outFileName + "_" + sessionName + ".txt", 'w')
      recordingTimeFile.write("Trial-CrayfishID, Samples, Recording Time (seconds)" + "\n")
    shortestInSession = 1000000000000

    for trialName in trialNames:
      crayfishIndex = 1
      for crayfishIndex in range(0, numCrayfish):
        refinedData = retrieveData(trialName, sessionName, crayfishIndex)
        identifier = trialName + "-" + str(crayfishIndex+1)
        recordingTime = refinedData[-1].time
        startTime = refinedData[0].time
        shortestRecordingTime = min(shortestRecordingTime, recordingTime)
        shortestInSession = min(shortestInSession, recordingTime)

        if savingLengths:
          outLine = ",".join([identifier, str(len(refinedData)), str(recordingTime - startTime), str(recordingTime)])
          recordingTimeFile.write(outLine + "\n")

    lengthDict[sessionName] = shortestInSession


  lengthDict["overall"] = shortestRecordingTime
  return lengthDict

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

def averageSpeed(samples):
  #return safeAverage([sample.speed for sample in samples])
  #print(getSpeeds(samples))
  #exit(0)
  return safeAverage(getSpeeds(samples))

def percentStill(samples):
  numSamples = len(samples)

  if numSamples == 0:
    return 0

  numStill = 0
  for sample in samples:
    if sample.xVel == 0 and sample.yVel == 0:
      numStill += 1

  return numStill / numSamples

def percentStillList(samples):
  return [percentStill(samples)]

def percentMiddle(samples):
  numSamples = len(samples)

  if numSamples == 0:
    return [0]

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

  #for (index, l) in zip(range(0, len(sampleList)), sampleList):
  #  if len(l) == 0:
  #    print("no data for " + str(index))

  return list(map(f, sampleList))

def splitAtTime(samples, timeCutoff):
  return [[sample for sample in samples if  sample.time < timeCutoff],
          [sample for sample in samples if sample.time >= timeCutoff and sample.time < (timeCutoff * 2)]]

def dataRow(trialName, crayfishIndex, val, session = None, splitIndex = None, length = None, increment = None, location = None):
  dataStr  = "t_" + str(trialTreatments[trialName])
  dataStr += ", " + trialName + "_" + str(crayfishIndex+1)
  dataStr += ", " + trialName
  dataStr += ", " + str(val)
  if session != None: dataStr += ", " + session
  if length != None: dataStr += ", " + str(length)
  if splitIndex != None: dataStr += ", part_" + str(splitIndex)
  if increment != None: dataStr += ", " + str(increment)
  if location != None: dataStr += ", " + location
  dataStr += "\n"

  return dataStr

def dataHeader(name, length = False, session = False, splitIndex = False, increments = False, location = False):
  header = "treatment, crayfishid, trial, " + name 
  if session: header += ", session"
  if length: header += ", length"
  if increments: header += ", increment"
  if splitIndex: header += ", sessionPart"
  if location: header += ", location"
  header += "\n"
  return header

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

def pauseDurations(samples, threshold=pauseThreholdHigh):
  if len(samples) == 0:
    return []

  prevSample = samples[0]
  timePaused = 0
  pausing = False
  pausedTimeList = []

  for sample in samples[1:]:
    if sampleDist(prevSample, sample) < speedThreshold:
      pausing = True
      timePaused += sampleTimePassed(prevSample, sample)
    else:
      pausing = False
      if timePaused != 0 and timePaused < pauseThreholdHigh: 
        pausedTimeList.append(timePaused)
      timePaused = 0
    prevSample = sample

  #in case the crayfish ended the session pausing
  if timePaused != 0 and timePaused < pauseThreholdHigh: 
    pausedTimeList.append(timePaused)

  return pausedTimeList

def pauseDurationWith(threshold):
  def l(samples):
    return pauseDurations(samples, threshold)
  return l

def averageTimePaused(samples):
  return safeAverage(pauseDurations(samples))

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
  #speedList = []
  #for (prevSample, sample) in zip(samples[:-1], samples[1:]):
  #  sp = sampleDist(prevSample, sample) / (sample.time - prevSample.time)
  #  speedList.append(sp)
  if len(samples) == 0:
    speedList = [0]
  else:
    speedList = [sample.speed for sample in samples]
  return speedList

def getSpeedsWalking(samples):
  speedList = []
  for (prevSample, sample) in zip(samples[:-1], samples[1:]):
    sp = sampleDist(prevSample, sample) / (sample.time - prevSample.time)
    if sp > speedThreshold:
      speedList.append(sp)
  if len(speedList) == 0:
    speedList = [0]
  #print("prev " + str(safeAverage([sample.speed for sample in samples if sample.speed > speedThreshold])))
  #print("new  " + str(safeAverage(speedList)))
  return speedList
  #print("higher = " + str(safeAverage([sample.speed for sample in samples if sample.speed > speedThreshold])))
  #print("middle = " + str(safeAverage([sample.speed for sample in samples])))
  #print("lower  = " + str(safeAverage([sample.speed for sample in samples if sample.speed <= speedThreshold])))
  #print("actual = " + str(safeAverage(speedList)))
  #print("\n")
  #return [sample.speed for sample in samples if sample.speed > speedThreshold]

def averageSpeedWalking(samples):
  return safeAverage(getSpeedsWalking(samples))

def forwardDirectivenessRatio(samples):
  result = 0

  if (len(samples) == 0): return 0

  distanceWalked = calCTotalDistance(samples)
  distanceDisplaced = sampleDist(samples[0], samples[-1])

  if (distanceDisplaced > 0):
    result = distanceDisplaced/distanceWalked

  return result

def identity(a):return a

def first(ls):
  return ls[0]

def returnList(a): return [a]

def percentMiddle(samples):
  return timeSpentLocation("middle", samples)

def percentMiddleList(samples):return [percentMiddle(samples)]

def filterByTime(time, samples):
  return [sample for sample in samples if sample.time < time]


def makeDataSets(fileName, combineProj, proj, summarizeIncrement = None, timeIncrement = 60, timeCutoffs = None, splitSessions = False, units=""):
  if splitSessions:
    outDir = "datasets\\" + fileName + "_split_sessions\\"
  else:
    outDir = "datasets\\" + fileName + "\\"
  outPath = outDir + fileName
  ensureDir(outDir)

  # full dataset, all samples
  experimentFile = open(outPath + "_all_samples.csv", 'w')
  experimentFile.write(dataHeader(fileName, splitIndex = splitSessions, session = True, length = True, location = True))

  # full dataset, all samples, in increments
  experimentIncrementFile = open(outPath + "_all_samples_increments.csv", 'w')
  experimentIncrementFile.write(dataHeader(fileName, splitIndex = splitSessions, session = True, length = True, increments = True, location = True))

  for locationName in allLocations:

    for sessionName in sessionNames:

      # open file for this session
      if locationName != "all":
        outFileName = outPath + "_" + locationName + "_" + sessionName + ".csv"
      else:
        outFileName = outPath + "_" + sessionName + ".csv"
      sessionSummaryFile = open(outFileName, 'w')
      sessionFile = open(outPath + "_all_samples_session_" + sessionName + ".csv", 'w')
      sessionFile.write(dataHeader(fileName, session=True, length=True, splitIndex = splitSessions, location = True))

      #session increment files aren't necessary if they are only for stats. The R program can just filter by session.
      #sessionIncrementsFile = open(outPath + "_all_samples_session_increments_" + sessionName + ".csv", 'w')
      #sessionIncrementsFile.write(dataHeader(fileName, session=True, length=True, splitIndex = timeCutoffs != None, increments = True))

      # write header for Cedric data files
      #if (not splitSessions or 'a' in sessionName):
      #  header = "crayfish index (0.0), " + fileName + "(" + units + ") treatment 0.0, crayfish index (0.5), " + fileName + "(" + units + ") treatment 0.5, crayfish index (5.0), " + fileName + "(" + units + ") treatment 5.0, crayfish index (50.0), " + fileName + "(" + units + ") treatment 50.0\n"
      #else:
      #  header = "crayfish index (0.0), " + fileName + "(" + units + ") treatment 0.0 (first part), " + fileName + "(" + units + ") treatment 0.0 (second part), crayfish index (0.5), " + fileName + "(" + units + ") treatment 0.5 (first part), " + fileName + "(" + units + ") treatment 0.5 (second part), crayfish index (5.0), " + fileName + "(" + units + ") treatment 5.0 (first part), " + fileName + "(" + units + ") treatment 5.0 (second part), crayfish index (50.0), " + fileName + "(" + units + ") treatment 50.0 (first part), " + fileName + "(" + units + ") treatment 50.0 (second part)\n"
      header = "crayfish index (0.0), " + fileName + "(" + units + ") treatment 0.0, crayfish index (0.5), " + fileName + "(" + units + ") treatment 0.5, crayfish index (5.0), " + fileName + "(" + units + ") treatment 5.0, crayfish index (50.0), " + fileName + "(" + units + ") treatment 50.0\n"
      sessionSummaryFile.write(header)


      allData = []
      for treatmentName in treatmentNames:
        treatmentData = []
        treatmentDataSecondPart = []
        treatmentIncrementData = []
        treatmentIncrementData2 = []
        crayfishIdentifiers = []
        population = []
        populationSecondPart = []

        incrementFile = open(outPath + "_increments_ " + str(timeIncrement) + "seconds_session_" + sessionName + "_treatment_" + str(treatmentName) + ".csv", 'w')
        header = ",".join(["crayfish " + str(index) + " " + trialName for index in indexRange for trialName in treatmentTrials[treatmentName]])
        #if splitSessions or 'a' in sessionName:
        #  header = ",".join(["crayfish " + str(index) + " " + trialName for index in indexRange for trialName in treatmentTrials[treatmentName]])
        #else:
        #  header = ",".join(["crayfish " + str(index) + " (" + part + " part) " for index in indexRange for part in ["first", "second"] for trialName in treatmentTrials[treatmentName]])
        incrementFile.write(header)
        incrementFile.write("\n")

        for trialName in treatmentTrials[treatmentName]:
          trialData = []
          trialDataSecondPart = []
          if trialName in ignoreCrayfish:
              print("Ignoring " + trialName + "\n")
              continue

          for crayfishIndex in range(0, numCrayfish):
            #print("trial = " + trialName + ", session = " + sessionName + ", treatment = " + str(treatmentName) + ", crayfish = " + str(crayfishIndex))
            ignoringCurrentCrayfish = (trialName, sessionName, crayfishIndex) in ignoreCrayfish

            # retrieve data from files
            refinedData = retrieveData(trialName, sessionName, crayfishIndex)
            dataSet = filterByLocation(locationName, refinedData)

            #dataSet = filterByTime(timeCutoffs[sessionName], dataSet)
            
            # processing full session
            if not splitSessions:
              #data summary file
              extracted = proj(dataSet)
              val = combineProj(extracted)

              if ignoringCurrentCrayfish:
                print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n")
                val = ""
                extracted = []

              sampleStr = dataRow(trialName, crayfishIndex, val)
              experimentFile.write(dataRow(trialName, crayfishIndex, val, session=sessionName, length=crayfishLengths[trialName][crayfishIndex], location=locationName))
              sessionFile.write(sampleStr)
              trialData.append(val)
              population += extracted

              #increment data
              if summarizeIncrement != None:
                incrementValues = intoIncrementsOf(dataSet, summarizeIncrement, timeIncrement)
                if ignoringCurrentCrayfish:
                  incrementValues = ["" for item in incrementValues]
                treatmentIncrementData.append(incrementValues)
                for (incrementIndex, value) in zip(range(0, len(incrementValues)-1), incrementValues):
                  incrementSampleStr = dataRow(trialName, crayfishIndex, value, session=sessionName, length=crayfishLengths[trialName][crayfishIndex], increment=incrementIndex, location=locationName)
                  experimentIncrementFile.write(incrementSampleStr)

            # processing evenly sized sessions
            else:
              dataSetIncr = splitAtTime(dataSet, timeCutoffs["overall"])
              extracted = list(map(proj, dataSetIncr))
              vals = list(map(combineProj, extracted))

              sampleStr  = dataRow(trialName, crayfishIndex, vals[0], splitIndex=0, session=sessionName, length=crayfishLengths[trialName][crayfishIndex], location=locationName)
              sampleStr2 = dataRow(trialName, crayfishIndex, vals[1], splitIndex=1, session=sessionName, length=crayfishLengths[trialName][crayfishIndex], location=locationName)

              experimentFile.write(dataRow(trialName, crayfishIndex, vals[0], splitIndex=0, session=sessionName, length=crayfishLengths[trialName][crayfishIndex], location=locationName))
              experimentFile.write(dataRow(trialName, crayfishIndex, vals[1], splitIndex=1, session=sessionName, length=crayfishLengths[trialName][crayfishIndex], location=locationName))
              sessionFile.write(sampleStr)
              sessionFile.write(sampleStr2)

              trialData.append(vals[0])
              treatmentDataSecondPart.append(vals[1])
              population += extracted[0]
              populationSecondPart += extracted[1]

              #increment data
              if summarizeIncrement != None:
                incrementValues = intoIncrementsOf(dataSet, summarizeIncrement, timeIncrement)
                #incrementValues = intoIncrementsOf(dataSetIncr[0], summarizeIncrement, timeIncrement)
                #incrementValues2 = intoIncrementsOf(dataSetIncr[1], summarizeIncrement, timeIncrement)
                treatmentIncrementData.append(incrementValues)
                #treatmentIncrementData2.append(incrementValues2)

                for (incrementIndex, value) in zip(range(0, len(incrementValues)-1), incrementValues):
                  incrementSampleStr = dataRow(trialName, crayfishIndex, value, session=sessionName, length=crayfishLengths[trialName][crayfishIndex], increment=incrementIndex, location=locationName)
                  experimentIncrementFile.write(incrementSampleStr)

                #for (incrementIndex, value) in zip(range(0, len(incrementValues)-1), incrementValues):
                #  incrementSampleStr = dataRow(trialName, crayfishIndex, value, splitIndex = 0, session=sessionName, length = crayfishLengths[trialName][crayfishIndex], increment = incrementIndex, location = locationName)
                #  experimentIncrementFile.write(incrementSampleStr)

                #for (incrementIndex, value) in zip(range(0, len(incrementValues2)-1), incrementValues2):
                #  incrementSampleStr2 = dataRow(trialName, crayfishIndex, value, splitIndex = 1, session=sessionName, length = crayfishLengths[trialName][crayfishIndex], increment = incrementIndex, location = locationName)
                #  experimentIncrementFile.write(incrementSampleStr2)

          identifiers = [trialName + "-" + str(ix) for ix in indexRange]
          crayfishIdentifiers += identifiers
          treatmentData += trialData
          if splitSessions: treatmentDataSecondPart += trialDataSecondPart

        if summarizeIncrement != None:
          incrementFile.write("\n".join([",".join(map(str, rowData)) for rowData in squareTranspose(treatmentIncrementData, "")]))
          #if not splitSessions:
          #  incrementFile.write("\n".join([",".join(map(str, rowData)) for rowData in transpose(treatmentIncrementData)]))
          #else:
          #  #incrementFile.write("\n".join([",".join(map(str, rowData)) for rowData in transpose(interleave(treatmentIncrementData, treatmentIncrementData2))]))

      #write out increment data
      #if summarizeIncrement != None and combineIncrements != None:
      #  transposedIncrementData = transpose(sessionIncrementData)
      #  fileIncrementData = transposedIncrementData 
      #  for row in fileIncrementData:
      #    sessionIncrementsFile.write((",".join(map(str, row))) + "\n")

      #transposedData = transpose(sessionData)
      #fileData = transposedData 
      #for row in fileData:
        #allDataOutFile.write((",".join(map(str, row))) + "\n")

        # Add extra data for Cedric- measure statistics

        # add stderr
        treatmentData.append(stderr(population))
        if splitSessions:
          if len(populationSecondPart) > 0:treatmentDataSecondPart.append(stderr(populationSecondPart))
          else: treatmentDataSecondPart.append("NA")
        crayfishIdentifiers.append("stderr")

        # add min
        treatmentData.append(min(population))
        if splitSessions:
          if len(populationSecondPart) > 0:treatmentDataSecondPart.append(min(populationSecondPart))
          else: treatmentDataSecondPart.append("NA")
        crayfishIdentifiers.append("min")

        # add max
        treatmentData.append(max(population))
        if splitSessions:
          if len(populationSecondPart) > 0:treatmentDataSecondPart.append(max(populationSecondPart))
          else: treatmentDataSecondPart.append("NA")
        crayfishIdentifiers.append("max")

        # add mean
        treatmentData.append(safeAverage(population))
        if splitSessions:
          if len(populationSecondPart) > 0:treatmentDataSecondPart.append(safeAverage(populationSecondPart))
          else: treatmentDataSecondPart.append("NA")
        crayfishIdentifiers.append("mean")

        # add first quartile
        treatmentData.append(numpy.percentile(population, 25))
        if splitSessions:
          if len(populationSecondPart) > 0:treatmentDataSecondPart.append(numpy.percentile(populationSecondPart, 25))
          else: treatmentDataSecondPart.append("NA")
        crayfishIdentifiers.append("first quartile")

        # add third quartile
        treatmentData.append(numpy.percentile(population, 75))
        if splitSessions:
          if len(populationSecondPart) > 0:treatmentDataSecondPart.append(numpy.percentile(populationSecondPart, 75))
          else: treatmentDataSecondPart.append("NA")
        crayfishIdentifiers.append("third quartile")

        # add mean (removing 0s)
        treatmentData.append(safeAverage(filterZeros(population)))
        if splitSessions:
          if len(populationSecondPart) > 0:treatmentDataSecondPart.append(safeAverage(filterZeros(populationSecondPart)))
          else: treatmentDataSecondPart.append("NA")
        crayfishIdentifiers.append("mean (without 0s)")

        allData.append(crayfishIdentifiers)
        allData.append(treatmentData)
        if splitSessions:allData.append(treatmentDataSecondPart)

      # write out dataset by transposing and combining accumulated data
      transposedData = transpose(allData)
      fileData = transposedData
      for row in fileData:
        sessionSummaryFile.write((",".join(map(str, row))) + "\n")

def interleave(ls, gs):
  result = []
  for (l, g) in zip(ls, gs):
    result.append(l)
    result.append(g)
  return result

def samplesCurveRatios(samples):
  ratios = [path.curveRatio() for path in Path.intoPaths(samples)]
  if len(ratios) == 0:
    ratios = [0]
  return ratios

def samplesCurveRatio(samples):
  return safeAverage(samplesCurveRatios(samples))

def postprocess():
  #Data sets for R statistics

  # Full data set summary
  lengthDict = recordingSessionLengths(True)
  print("shortestRecordingTime overall = " + str(lengthDict["overall"]))
  print("shortestRecordingTime a = " + str(lengthDict["a"]))
  print("shortestRecordingTime b = " + str(lengthDict["b"]))
  print("shortestRecordingTime c = " + str(lengthDict["c"]))

  #Data sets for graphing
  #TODO deal with including shortestRecordingTime 
  print("avgSpeed")
  makeDataSets("avgSpeed",  safeAverage, getSpeeds, summarizeIncrement = averageSpeed, timeCutoffs = lengthDict, splitSessions = False, units="mm/second")
  #print("avgSpeed split")
  #makeDataSets("avgSpeed",  safeAverage, getSpeeds, summarizeIncrement = averageSpeed, timeCutoffs = lengthDict, splitSessions = True, units="mm/second")

  print("avgSpeed walking")
  makeDataSets("avgSpeedWalking",  safeAverage, getSpeedsWalking, summarizeIncrement = averageSpeedWalking, timeCutoffs = lengthDict, splitSessions = False, units="mm/second")
  #print("avgSpeed walking split")
  #makeDataSets("avgSpeedWalking",  safeAverage, getSpeedsWalking, summarizeIncrement = averageSpeedWalking, timeCutoffs = lengthDict, splitSessions = True, units="mm/second")

  print("total distance")
  makeDataSets("totalDist_mm", sum, getDistances, summarizeIncrement = totalDistance, timeCutoffs = lengthDict, units="mm", splitSessions=False)
  #print("total distance split")
  #makeDataSets("totalDist_mm", sum, getDistances, summarizeIncrement = totalDistance, timeCutoffs = lengthDict, units="mm", splitSessions=True)

  #makeDataSets("straightness",  safeAverage, samplesCurveRatios, summarizeIncrement = samplesCurveRatio, timeCutoffs = lengthDict, splitSessions = False, units="ratio")
  makeDataSets("averagePauseDuration_" + str(30) + "seconds",  safeAverage, pauseDurationWith(30), summarizeIncrement = averageTimePaused, timeCutoffs = lengthDict, units="mm/second")
  makeDataSets("averagePauseDuration_" + str(60) + "seconds",  safeAverage, pauseDurationWith(60), summarizeIncrement = averageTimePaused, timeCutoffs = lengthDict, units="mm/second")
  #makeDataSets("percentstandingstill", first, percentStillList, summarizeIncrement = percentStill, timeCutoffs = lengthDict, units="percent")
  #makeDataSets("percentTimeMiddle", first, percentMiddleList, summarizeIncrement = percentMiddle, timeCutoffs = lengthDict, units="percent")

  #not sure if this can be made to work
  #makeDataSets("averageForwardDirectiveness",  forwardDirectivenessRatio, distances)

if __name__ == "__main__":
  postprocess()

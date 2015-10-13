import numpy
import os
import math
from matplotlib import pyplot as plt
from CrayfishLib import *

def processSession(session):
  """ Main processing function. This function processes one recording session """
  palette = ['#db5e0c', '#14660d', '#460C67', '#d40607', '#cb971a', '#0c5b67']
  plt.rc('axes', color_cycle = palette)

  volumeOverTime(session)

  xyOverTime(session)

  xyMovement(session)

  velOverTime(session)

  velHist(session, True)
  velHist(session, False)

  totalDistanceTraveled(session)

def totalDistanceTraveled(session):
  outPath = outputPath(session.trialName) + "distance_traveled\\"
  ensureDir(outPath)

  fig = plt.figure(1)

  distances = [calCTotalDistance(crayfish) for crayfish in [crayfishes for crayfishes in session.sampleSet]]

  fig, ax = plt.subplots()
  ax.bar(range(0, len(distances)), distances, 0.35, color='b')

  ax.set_xticklabels(list(map(str, list(range(0, len(distances))))))

  fig.tight_layout()
  fig.set_size_inches(36, 24)
  plt.savefig(outPath + "distance_traveled.png")
  plt.close(fig)
  plt.clf()

def calCTotalDistance(crayfishData):
  totalDistance = 0
  for (startSample, endSample) in zip(crayfishData, crayfishData[1:]):
    totalDistance += sampleDist(startSample, endSample)
  return totalDistance

def velOverTime(session):
  """ create a graph of the speed of all the crayfish over time in a recording session """
  outPath = outputPath(session.trialName) + "velocity\\"
  ensureDir(outPath)

  fig = plt.figure(1)

  for (index, crayfishes) in zip(range(0, len(session.sampleSet)), session.sampleSet):
    plotVelocities(fig, index, crayfishes)

  fig.tight_layout()
  fig.set_size_inches(36, 24)
  plt.savefig(outPath + session.sessionName + "_speeds.png")
  plt.close(fig)
  plt.clf()

def plotVelocities(figure, index, crayfishes):
  subplot = figure.add_subplot(6, 1, index)
  ms  = [crayfish.ms   for crayfish in crayfishes]
  xvs = [crayfish.xVel for crayfish in crayfishes]
  yvs = [crayfish.yVel for crayfish in crayfishes]
  speeds = [crayfish.speed for crayfish in crayfishes]
  plt.plot(ms, speeds)
  plt.xlabel("Time (seconds)")
  plt.ylabel("Speed (cm/second)")
  plt.title("Speed of crayfish " + str(index))


def volumeOverTime(session):
  """ create a graph of the volumne of all the crayfish over time in a recording session """
  outPath = outputPath(session.trialName) + "volume\\"
  ensureDir(outPath)

  fig = plt.figure(1)
  for (index, crayfishes) in zip(range(0, len(session.sampleSet)), session.sampleSet):
    plotVolume(fig, index, crayfishes)

  fig.set_size_inches(36, 24)
  plt.savefig(outPath + session.sessionName + "_volumes.png")
  plt.close(fig)
  plt.clf()

def plotVolume(figure, index, crayfishes):
  subplot = figure.add_subplot(6, 1, index)
  ms  = [crayfish.ms   for crayfish in crayfishes]
  volumes = [crayfish.volume for crayfish in crayfishes]
  plt.plot(ms, volumes)
  plt.xlabel("Time (seconds)")
  plt.ylabel("Volume (cm/second)")
  plt.title("Volume of crayfish " + str(index))

def velHist(session, noZeros):
  """ create a histogram of the speed of all the crayfish in a recording session """
  outPath = outputPath(session.trialName) + "velocity_histograms\\"
  ensureDir(outPath)

  fig = plt.figure(1)
  for (index, crayfishes) in zip(range(0, len(session.sampleSet)), session.sampleSet):
    plotVelHist(noZeros, fig, index, crayfishes)

  zerosStr = ""
  if noZeros:zerosStr = "_no0s"

  #fig.tight_layout()
  fig.set_size_inches(36, 36)
  plt.savefig(outPath + session.sessionName + "_speedhist" + zerosStr + ".png")
  plt.close(fig)
  plt.clf()

def plotVelHist(noZeros, figure, index, crayfishes):
  subplot = figure.add_subplot(6, 1, index)
  ms = [crayfish.ms for crayfish in crayfishes]
  speeds = [crayfish.speed for crayfish in crayfishes]
  if noZeros: speeds = [speed for speed in speeds if speed > speedThreshold]

  maxSpeed = max(speeds)
  bins = numpy.arange(0, maxSpeed, maxSpeed/100)

  plt.hist(speeds, bins)
  plt.xlabel("Speed")
  plt.ylabel("Frequency")
  plt.title("Speed Frequency for crayfish " + str(index))

def xyOverTime(session):
  """ create a graph of the x position a y position for each crayfish for each recording session """
  outPath = outputPath(session.trialName) + "xy\\"
  ensureDir(outPath)

  plt.close('all')
  plt.clf()

  for (index, samples) in zip(range(0, len(session.sampleSet)), session.sampleSet):
    plotXYs(session, index, samples)

  fig = plt.figure(1)
  #fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
  #fig.tight_layout()
  fig.set_size_inches(48, 24)

  plt.savefig(outPath + session.sessionName + "_xys.png")
  plt.close(fig)
  plt.clf()

def plotXYs(session, index, samples):
  fig = plt.figure(1)

  subplotX = plt.subplot2grid((6, 2), (index, 0))
  subplotY = plt.subplot2grid((6, 2), (index, 1))

  ms  = [sample.ms for sample in samples]
  xs = [sample.x for sample in samples]
  ys = [sample.y for sample in samples]

  subplotX.set_title("X Position of " + str(index))
  subplotX.set_xlabel("X Position")
  subplotX.set_ylabel("Time (seconds)")
  subplotX.plot(ms, xs)

  subplotY.set_title("Y Position of " + str(index))
  subplotY.set_xlabel("Y Position)")
  subplotY.set_ylabel("Time (seconds)")
  subplotY.plot(ms, ys)

def xyMovement(session):
  """ create a plot of the positions of all the crayfish in a recording session """
  outPath = outputPath(session.trialName) + "positions\\"
  ensureDir(outPath)

  lineStyles = {"dots" : '.', "lines" : '-'}

  for plotType in ["dots", "lines"]:
    for (index, crayfish) in zip(range(0, len(session.sampleSet)),session.sampleSet):
      plotMovement(index, crayfish, lineStyles[plotType])
    plt.title("X vs Y")
    fig = plt.figure(1)
    fig.set_size_inches(48, 24)
    plt.savefig(outPath + session.sessionName + "_positions_" + plotType + ".png")
    plt.clf()

def plotMovement(index, samples, lineStyle):
  xs = [sample.x for sample in samples]
  ys = [sample.y for sample in samples]
  plt.plot(xs, ys, lineStyle)
  plt.xlabel("X position for crayfish " + str(index))
  plt.ylabel("Y position for crayfish " + str(index))

def outputPath(trialName):
  """ This is a utility function for creating file names from session data """
  return outDir + "/" + trialName + "/"

def sessionStats(session):
  numSamples = len(session.sampleSet)
  avgSpeeds = [sum(sample.speed for sample in samples) / len(samples) for samples in session.sampleSet]
  return SessionStats(session.sessionName, getStage(session.sessionName), avgSpeeds)

def summarizeDataset():
  for trialName, trialDatas in trials.items():
    for session in trialDatas:
      print(trialName + ", " + session.sessionName + " avgSpeeds = " + str(session.avgSpeeds))
      plotAvgSpeed(session)

  avgSpeedByTreatment()

def plotAvgSpeed(session):
  #plt.plot(session.avgSpeeds)
  plt.xlabel("Crayfish Number")
  plt.ylabel("Average Speed (cm/second)")
  plt.title("Average Speed of crayfish during a Recording Session")
  fig, ax = plt.subplots()
  ax.bar(range(0, 6), session.avgSpeeds)
  plt.savefig(session.sessionName + "_avgSpeed" + ".png")
  plt.close(fig)
  plt.clf()

def avgSpeedByTreatment():
  for sessionType in "abc":
    plt.xlabel("Treatment Level")
    plt.ylabel("Average Speed (cm/second)")
    plt.title("Average Speed of Crayfish By Treatment Level")
    points = [(trialTreatments[trialName], avgSpeed)
              for (trialName, sessions) in trials.items()
              for session in sessions
              if session.sessionType == sessionType
              for avgSpeed in session.avgSpeeds]
    if len(points) > 0:
      plt.scatter(*zip(*points))
      plt.savefig("avgSpeedByTreatment_" + sessionType + ".png")
    plt.clf()

def toRefined(vals):
  floats = [float(val) for val in vals[0:-1]]
  location = vals[-1].strip()
  return Crayfish(floats[0], floats[1], floats[2], floats[3], floats[4], floats[5], floats[6], floats[7], floats[8], location)

def retrieveData(trial, session, crayfish):
  path = ".\\output\\" + trial + "\\"
  dataFiles = [name for name in os.listdir(path) if (session + "_") in name and ("_" + str(crayfish)) in name]

  print("retrieveData filenames = " + str(dataFiles))

  fileName = dataFiles[0]

  lines = list(open(path + fileName, 'r').read().split('\n'))
  lines = lines[1:]

  refinedData = [toRefined(line.split(',')) for line in lines if len(line) > 0]

  return refinedData

def plotOverTime(trial, session, crayfish, name, xLabel, yLabel, xys):
  outPath = outputPath(trial) + "\\" + name + "\\"
  outFile = outPath + (trial + "_" + session + "_" + name)
  ensureDir(outPath)

  fig = plt.figure(1)

  xs = [pair[0] for pair in xys]
  ys = [pair[1] for pair in xys]

  lineStyles = {"dots" : '.', "lines" : '-'}
  for lineStyle in lineStyles:
    plt.plot(xs, ys, lineStyles[lineStyle])
    plt.plot(xs, ys)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(name)

    fig.set_size_inches(24, 24)
    plt.savefig(outFile + "_" + lineStyle)
    plt.close(fig)
    plt.clf()

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
          print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex) + "\n")
          continue

        headerText = "Processing " + trialName + " " + sessionName + " " + str(crayfishIndex) + "\n"
        print(headerText)

        refinedData = retrieveData(trialName, sessionName, crayfishIndex)
        endTime = max([sample.ms for sample in refinedData])
        numBuckets = int(endTime / timeSegment) + 1
        sampleList = []
        [sampleList.append([]) for i in range(0, numBuckets)]
        for sample in refinedData:
          index = int(sample.ms/timeSegment)
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
          trialNameStr = trialName + "_" + str(crayfishIndex)
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

def processFullSessions(name, xLabel, yLabel, collapse):
  outputDirectory = outDir + "\\" + name
  outFileName =  outputDirectory + "\\" + name + "_full"
  ensureDir(outputDirectory)

  measures = []

  for sessionName in sessionNames:
    outFile = open(outFileName + "_" + sessionName, 'w')
    outFile.write("treatment, crayfishid," + name + "\n")

    for trialName in trialNames:
      if trialName in ignoreTrials:
          print("Ignoring " + trialName + "\n")
          continue

      for crayfishIndex in range(0, numCrayfish):
        if (trialName, sessionName, crayfishIndex) in ignoreCrayfish:
          print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex) + "\n")
          continue

        headerText = "Processing " + trialName + " " + sessionName + " " + str(crayfishIndex) + "\n"
        print(headerText)

        refinedData = retrieveData(trialName, sessionName, crayfishIndex)
        crayfishSummary = collapse(refinedData)
        #TODO match up with an id for the plot
        measures.append((str(trialName) + str(crayfishIndex), crayfishSummary))
        outFile.write("t_" + str(trialTreatments[trialName]) + ", " + trialName + "_" + str(crayfishIndex) + ", " + str(crayfishSummary) + "\n")
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



def distanceTraveledAllCrayfish():
  outFileName = "summary\\dist_all"
  ensureDir("summary\\")
  outFile = open(outFileName, 'w')
  barWidth = 0.1

  allDistances = []
  distMap = {}
  for treatmentName in treatmentNames:
    distMap[treatmentName] = []

  #process all crayfish, writing results to dist_all
  for sessionName in sessionNames:
    outFile = open(outFileName + "_" + sessionName + ".csv", 'w')
    outFile.write("treatment, crayfishid, totalDistance\n")

    for trialName in trialNames:
      for crayfishIndex in range(0, numCrayfish):
        if (trialName, sessionName, crayfishIndex) in ignoreCrayfish:
          print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex) + "\n")
          continue

        progressText = "Processing " + trialName + " " + sessionName + " " + str(crayfishIndex) + "\n"
        print(progressText)

        refinedData = retrieveData(trialName, sessionName, crayfishIndex)

        totalDistance = calCTotalDistance(refinedData)
        distMap[str(trialTreatments[trialName])].append(totalDistance)
        allDistances.append((trialName, crayfishIndex, totalDistance))

        outFile.write("t_" + str(trialTreatments[trialName]) + ", " + trialName + "_" + str(crayfishIndex) + ", " + str(totalDistance) + "\n")

  #create bar chart with total distance by treatment
  fig = plt.figure(1)

  fig, ax = plt.subplots()

  distLists = []
  for treatmentName in treatmentNames:
    distLists.append(distMap[treatmentName])
  offset = 0
  for vals in transpose(distLists):
    ax.bar([barWidth * offset + index for index in range(0, len(distMap))], vals, barWidth, color='b')
    offset += 1

  ax.set_xticklabels(treatmentNames)

  fig.tight_layout()
  fig.set_size_inches(36, 24)
  plt.savefig("summary//total_by_treatment_distance_traveled.png")
  plt.close(fig)
  plt.clf()

  #create bar chart for all total distances
  fig = plt.figure(1)

  fig, ax = plt.subplots()
  ax.bar(range(0, len(allDistances)), [sample[2] for sample in allDistances], barWidth, color='b')

  ax.set_xticklabels([str(sample[0]) + "_" + str(sample[1]) for sample in allDistances])

  fig.tight_layout()
  fig.set_size_inches(36, 24)
  plt.savefig("summary//distance_traveled.png")
  plt.close(fig)
  plt.clf()


def averageOverList(samples):
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

if __name__ == "__main__":
  #processInSegments("AverageSpeed", "Time", "AverageSpeed", 60, averageOverList)
  #processInSegments("Location", "Time", "Location", 60, percentMiddle)
  #processFullSessions("LocationFull", "Crayfish ID", "Location", percentMiddle)
  #distanceTraveledAllCrayfish()
  #processFullSessions("AverageSpeedFull", "Crayfish ID", "AverageSpeed", averageOverList)
  processFullSessions("AverageSpeedMid",    "Crayfish ID", "AverageSpeed", averageSpeedLocation("middle"))
  processFullSessions("AverageSpeedEdge",   "Crayfish ID", "AverageSpeed", averageSpeedLocation("edge"))
  processFullSessions("AverageSpeedCorner", "Crayfish ID", "AverageSpeed", averageSpeedLocation("corner"))
  #processInSegments("PercentStill", "Time", "PercentStill", 60, percentStill)

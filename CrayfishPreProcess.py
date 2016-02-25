import os
import string
import math
import numpy
import collections
import sys

from CrayfishLib import *
from CrayfishPostProcess import *


def ingest(inFile):
    """ Read the raw data in and split it by line and by field """
    # there are 3 bytes of header in these files
    #inFile.read(3)

    # Read in, remove newlines, and split on form feeds
    #lines = inFile.read().translate({"\n" : None}).split('\r')
    lines = list(inFile.read().split('\n'))

    #  The separator between fields is tab
    lines = [line.split('\t') for line in lines]

    # Filter rows with fewer fields then expected
    lineCount = len(lines)
    lines = [line for line in lines if len(line) == numColumns]
    finalLineCount = len(lines)
    if lineCount != finalLineCount:
        lineDifference = lineCount-finalLineCount
        print("some lines had too few columns. threw out: " +
              str(lineDifference))

    return lines

def parseDataSet(trial, stage, rawData):
    """ take raw data and turn it into a useable form """

    # remove lines that start with a -1
    rawData = [line for line in rawData if line[0] != -1]

    # parse out each line
    crayfishes = []
    for crayfish in rawData:
      crayfishes.append(parseLine(trial, stage, crayfish))

    # turn a list of rows into a list of columns
    crayfishes = transpose(crayfishes)

    # remove samples that seemed fishy during processing (resulted in None objects)
    #crayfishes = map(lambda crayfish : filter(lambda sample : sample != None, crayfish), crayfishes)
    crayfishes = [[sample for sample in samples if sample != None] for samples in crayfishes]

    #reindex data to use Cedric's indexing scheme
    reindex(crayfishes)

    return crayfishes

def parseLine(trial, stage, line):
    """ break out the contents of a single row of a raw data file """
    time = float(line.pop(0))/1000
    crayfish = [parseCrayFish(trial, stage, i, time, line[i*numFields:(i+1)*numFields])
                for i in range(0, numCrayfish)]
    return crayfish

def parseCrayFish(trial, stage, index, time, line):
    """ break out the contents of a single crayfish's data for a row """
    [x, y, crayfishID, rotation, height, width] = line[0:numFields]

    # if the data doesn't seem right, return None instead
    if int(x) == -1 or int(y) == -1:
        return None

    # create an object to store the data for one crayfish for one sample
    return RawSample(time,
                     index,
                     trial,
                     stage,
                     float(x),
                     float(y),
                     float(rotation),
                     float(height),
                     float(width))

def refineDataSet(summaryFile, dataset):
  """ Take the parsed data and create interesting structures from it """
  refined = []
  timeCap = 100000000

  for rawSamples in dataset:
    refinedSamples = []

    # Window
    windowX = collections.deque()
    windowY = collections.deque()

    totalLost = 0
    edgeLost = 0
    tooFastLost = 0

    prevX = rawSamples[0].x
    prevY = rawSamples[0].y
    prevTime = rawSamples[0].time

    index = rawSamples[0].index
    trial = rawSamples[0].trial

    # Camera
    camera = None
    if rawSamples[0].stage == 'a':
      camera = camera1
    else:
      camera = cameras[rawSamples[0].trial]
    cameraX = camera.boxes[index].location[0]
    cameraY = camera.boxes[index].location[1]
    innerBox = camera.innerBoxes[index]

    # Filtering
    for raw in rawSamples:
      nearEdgeX = abs(raw.x - cameraX) <= xErrorEdge or raw.x < cameraX
      nearEdgeY = abs(raw.y - cameraY) <= yErrorEdge or raw.y < cameraY
      needsFiltering = (raw.trial, raw.stage) not in cleanTrials

      if runFiltering and needsFiltering and (nearEdgeX or nearEdgeY):
        totalLost += 1
        edgeLost += 1
        raw.x = None
        raw.y = None
        continue

      timeDiff = raw.time - prevTime
      if timeDiff > 0 and runFiltering:
        if (abs(raw.x - prevX) / timeDiff) > speedCap or (abs(raw.y - prevY) / timeDiff) > speedCap:
          totalLost += 1
          tooFastLost += 1
          raw.x = prevX
          raw.y = prevY

      noMovementX = abs(raw.x - prevX) < xJitter
      noMovementY = abs(raw.y - prevY) < yJitter
      if runFiltering and noMovementX:
        raw.x = prevX
      if runFiltering and noMovementY:
        raw.y = prevY

      if len(windowX) >= filterWindow:
        windowX.pop()
        windowY.pop()
      windowX.appendleft(raw.x)
      windowY.appendleft(raw.y)

      prevX = raw.x
      prevY = raw.y

      if runFiltering: raw.x = safeAverage(windowX)
      if runFiltering: raw.y = safeAverage(windowY)

    timeCap = min(timeCap, raw.time)
    
    rawSamples = [sample for sample in rawSamples if sample.x != None]

    time = [raw.time for raw in  rawSamples]
    xs = [raw.x for raw in  rawSamples]
    ys = [raw.y for raw in  rawSamples]
    vxs = [diff(*quad) for quad in zip(xs, xs[1:], time, time[1:])]
    vys = [diff(*quad) for quad in zip(ys, ys[1:], time, time[1:])]
    moveAmounts = [dist(*quad) for quad in zip(xs, xs[1:], ys, ys[1:])]
    prevTime = time[0]
    totalSamples = len(rawSamples)
    sp = 0
    prevX = rawSamples[0].x * camera.pixelDims[0]
    prevY = rawSamples[0].y * camera.pixelDims[1]

    for (raw, vx, vy, moveAmount) in zip(rawSamples, vxs, vys, moveAmounts):
      location = innerBox.determineLocation(raw.x, raw.y) 
      raw.x *= camera.pixelDims[0]
      raw.y *= camera.pixelDims[1]
      raw.width *= camera.pixelDims[0]
      raw.height *= camera.pixelDims[1]
      if raw.time != prevTime:
        sp = (dist(prevX, prevY, raw.x, raw.y) / (raw.time-prevTime))
      else:
        sp = 0

      if sp > speedCapMM:
        continue

      prevTime = raw.time

      crayfish = Crayfish(raw.time, raw.x, raw.y, vx, vy, raw.rotation, raw.height, raw.width, sp, location)
      refinedSamples.append(crayfish)
      prevX = raw.x
      prevY = raw.y

    totalLostDataText = "percent lost = " + str(100.0 * (float(totalLost)/float(totalSamples)))
    edgeLostDataText = "percent near edge = " + str(100.0 * (float(edgeLost)/float(totalSamples)))
    fastLostDataText = "percent too fast = " + str(100.0 * (float(tooFastLost)/float(totalSamples)))
    summaryFile.write(rawSamples[0].trial + " " + rawSamples[0].stage + " " + str(rawSamples[0].index) + "\n")
    #print(totalLostDataText)
    #print(edgeLostDataText)
    #print(fastLostDataText)
    summaryFile.write(totalLostDataText + "\n")
    summaryFile.write(edgeLostDataText + "\n")
    summaryFile.write(fastLostDataText + "\n")
    refined.append(refinedSamples)

  filteredRefined = refined
  return filteredRefined

def crayfishCSV(crayfish):
    """ Turn a crayfish's data into CVS output """
    #sp = math.sqrt(crayfish.xVel*crayfish.xVel + crayfish.yVel*crayfish.yVel)
    formatParams = [crayfish.time, crayfish.x, crayfish.y, crayfish.xVel, crayfish.yVel, crayfish.rotation, crayfish.height, crayfish.width, crayfish.speed]
    return "{: 5.3f},  {: 5.3f},  {: 5.3f},  {: 5.3f},  {: 5.3f},  {: 5.3f},  {: 5.3f},  {: 5.3f},  {: 5.3f}".format(*formatParams) + ", " + crayfish.location

def outgest(session):
  """ Write out the results of parsing a session's worth of data """

  # for each crayfish
  for (index, crayfishes) in zip(range(0, 6), session.sampleSet):
    fileName = "\\".join([outDir, session.trialName, session.sessionName + "_" + str(index) + ".csv"])

    # open a file to write to
    with open(fileName, 'w') as outFile:
     
      # write out a little header line to explain the data
      outFile.write(crayfishHeader)

      # for each sample in the session
      for crayfish in crayfishes:

        # write out a CSV string of the sample
        outFile.write(crayfishCSV(crayfish))
        outFile.write("\n")


def outgestCrayfish(outFile, samples):
    """ Write out a file with a single crayfish's data from a recording session """
    # Write out cleaned up input file to output file
    outFile.write(crayfishHeader)
    for sample in samples:
        for crayfish in sample:
          outFile.write(crayFishCSV(crayfish))
          outFile.write(",")
        outFile.write("\n")

def allFiles(dir):
  """ Find all files in a directory, returning the path and file name """
  fileList = []
  for path, dirs, files in os.walk(dir):
      if len(files) > 0:
          splitPath = path.split("\\")
          if len(splitPath) > 1:
              subfolder = splitPath[1]
              fileList += [(subfolder, fileName) for fileName in files]
  return fileList

def processExperiment(trialsToRun, stagesToRun):
    """ This is the main function for the whole program. Start here """

    print("Starting Processing")

    if len(sys.argv) > 1:
      trialsToRun = [sys.argv[1]]
    else:
      trialsToRun = trialNames

    if len(sys.argv) > 2:
      stagesToRun = [sys.argv[2]]
    else:
      stagesToRun = "abc"

    if len(sys.argv) > 3:
      profiling = [sys.argv[3]]

    # Ensure the output directory exists
    ensureDir(outDir)

    # find all data files to process
    files = allFiles(inDir)

    dataSummaryFile = open("summary.txt", 'w')

    # for each file: read the file, clean up the data, create some records, and create graphs
    for (trialName, sessionName) in files:
        if trialName not in trialsToRun:continue

        if getStage(sessionName) not in stagesToRun:continue

        print("Processing " + trialName + ", " + sessionName)

        filePath = trialName + "\\" + sessionName


        # for each session (1 file)
        with open(inDir + "\\" + filePath, 'r') as inFile:
            # read from the file
            rawData = ingest(inFile)

            trialOutPath = outDir + "\\" + trialName
            trialOutFile = trialOutPath + "\\" + sessionName

            # ensure that there is a directory to record results in
            if not os.path.exists(trialOutPath): os.makedirs(trialOutPath)

            # open the file and perform processing
            print("trialOutFile = " + trialOutFile)
            with open(trialOutFile, 'w') as outFile:
                # break the data into records
                dataset = parseDataSet(trialName, getStage(sessionName), rawData)

                # create nicer data
                crayfishes = refineDataSet(dataSummaryFile, dataset)

                for (index, crayfishData) in zip(indexRange, crayfishes):
                  print("crayfish " + str(index) + " num records = " + str(len(crayfishData)))

                session = Session(trialName, sessionName, crayfishes)

                #save session data to the trial it is associated with
                trials[trialName].append(sessionStats(session))

                #save the resulting cleaned-up data to a file 
                if savingPreprocessResults:
                  outgest(session)

if __name__ == "__main__":
    if len(sys.argv) > 1:
      trialsToRun = [sys.argv[1]]
    else:
      trialsToRun = ["Trial 1", "Trial 2", "Trial 3", "Trial 4",
                     "Trial 5", "Trial 6", "Trial 7", "Trial 8",
                     "Trial 9", "Trial 10", "Trial 11", "Trial 12"]

    if len(sys.argv) > 2:
      stagesToRun = [sys.argv[2]]
    else:
      stagesToRun = "abc"

    processExperiment(trialsToRun, stagesToRun)

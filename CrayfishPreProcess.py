import os
import string
import math
import numpy
import collections

from CrayfishLib import *


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

    return crayfishes

def parseLine(trial, stage, line):
    """ break out the contents of a single row of a raw data file """
    ms = float(line.pop(0))/1000
    crayfish = [parseCrayFish(trial, stage, i, ms, line[i*numFields:(i+1)*numFields])
                for i in range(0, numCrayfish)]
    return crayfish

def parseCrayFish(trial, stage, index, ms, line):
    """ break out the contents of a single crayfish's data for a row """
    [x, y, crayfishID, rotation, height, width] = line[0:numFields]

    # if the data doesn't seem right, return None instead
    if int(x) == -1 or int(y) == -1:
        return None

    # create an object to store the data for one crayfish for one sample
    return RawSample(ms,
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
    prevMS = rawSamples[0].ms

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

      msDiff = raw.ms - prevMS
      if msDiff > 0 and runFiltering:
        if (abs(raw.x - prevX) / msDiff) > speedCap or (abs(raw.y - prevY) / msDiff) > speedCap:
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

    timeCap = min(timeCap, raw.ms)
    
    rawSamples = [sample for sample in rawSamples if sample.x != None]

    ms = [raw.ms for raw in  rawSamples]
    xs = [raw.x for raw in  rawSamples]
    ys = [raw.y for raw in  rawSamples]
    vxs = [diff(*quad) for quad in zip(xs, xs[1:], ms, ms[1:])]
    vys = [diff(*quad) for quad in zip(ys, ys[1:], ms, ms[1:])]
    moveAmounts = [dist(*quad) for quad in zip(xs, xs[1:], ys, ys[1:])]
    prevMS = ms[0]
    totalSamples = len(rawSamples)
    sp = 0
    prevX = rawSamples[0].x
    prevY = rawSamples[0].y

    for (raw, vx, vy, moveAmount) in zip(rawSamples, vxs, vys, moveAmounts):
      location = innerBox.determineLocation(raw.x, raw.y) 
      raw.x *= camera.pixelDims[0]
      raw.y *= camera.pixelDims[1]
      raw.width *= mmPerPixelX
      raw.height *= mmPerPixelY
      if raw.ms != prevMS:
        sp = (dist(raw.x, raw.y, prevX, prevY) / (raw.ms-prevMS))
      else:
        sp = 0

      prevMS = raw.ms

      crayfish = Crayfish(raw.ms, raw.x, raw.y, vx, vy, raw.rotation, raw.height, raw.width, sp, location)
      refinedSamples.append(crayfish)
      prevX = raw.x
      prevY = raw.y

    totalLostDataText = "percent lost = " + str(100.0 * (float(totalLost)/float(totalSamples)))
    edgeLostDataText = "percent near edge = " + str(100.0 * (float(edgeLost)/float(totalSamples)))
    fastLostDataText = "percent too fast = " + str(100.0 * (float(tooFastLost)/float(totalSamples)))
    summaryFile.write(rawSamples[0].trial + " " + rawSamples[0].stage + " " + str(rawSamples[0].index) + "\n")
    print(totalLostDataText)
    print(edgeLostDataText)
    print(fastLostDataText)
    summaryFile.write(totalLostDataText + "\n")
    summaryFile.write(edgeLostDataText + "\n")
    summaryFile.write(fastLostDataText + "\n")
    refined.append(refinedSamples)

  filteredRefined = refined
  return filteredRefined

def crayfishCSV(crayfish):
    """ Turn a crayfish's data into CVS output """
    sp = math.sqrt(crayfish.xVel*crayfish.xVel + crayfish.yVel*crayfish.yVel)
    formatParams = [crayfish.ms, crayfish.x, crayfish.y, crayfish.xVel, crayfish.yVel, sp, crayfish.rotation, crayfish.height, crayfish.width]
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


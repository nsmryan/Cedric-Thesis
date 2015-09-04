import os
import string
import math
import numpy

from CrayfishLib import *


def ingest(fileName, inFile):
    """ Read the raw data in and split it by line and by field """
    print("processing file" + fileName)

    # there are 3 bytes of header in these files
    inFile.read(3)

    # The new line character is form feed.
    lines = inFile.read().split('\r')

    # Some lines contain newline characters which must be filtered
    lines = map(lambda line: line.translate(None, "\n"), lines)

    #  The separator between fields is tab
    lines = map(lambda line: line.split('\t'), lines)

    # Filter rows with fewer fields then expected
    lineCount = len(lines)
    lines = filter(lambda line: len(line) == numColumns, lines)
    finalLineCount = len(lines)
    if lineCount != finalLineCount:
        lineDifference = lineCount-finalLineCount
        print("some lines had too few columns. threw out: " +
              str(lineDifference))

    return lines

def parseDataSet(trial, stage, rawData):
    """ take raw data and turn it into a useable form """

    # remove lines that start with a -1
    rawData = filter(lambda line : line[0] != -1, rawData)

    # parse out each line
    crayfishes = []
    for crayfish in rawData:
      crayfishes.append(parseLine(trial, stage, crayfish))

    # turn a list of rows into a list of columns
    crayfishes = transpose(crayfishes)

    # remove samples that seemed fishy during processing (resulted in None objects)
    crayfishes = map(lambda crayfish : filter(lambda sample : sample != None, crayfish), crayfishes)

    return crayfishes

def transpose(lists):
   """ take a list of rows and turn it into a list of columns """
   if not lists: return []
   return map(lambda *row: list(row), *lists)

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

def refineDataSet(dataset):
  """ Take the parsed data and create interesting structures from it """
  refined = []

  for rawSamples in dataset:
    refinedSamples = []
    ms = [raw.ms for raw in  rawSamples]
    xs = [raw.x for raw in  rawSamples]
    ys = [raw.y for raw in  rawSamples]
    vxs = [diff(*quad) for quad in zip(xs, xs[1:], ms, ms[1:])]
    vys = [diff(*quad) for quad in zip(ys, ys[1:], ms, ms[1:])]
    moveAmounts = [dist(*quad) for quad in zip(xs, xs[1:], ys, ys[1:])]
    prevX = xs[0]
    prevY = ys[0]
    prevMS = ms[0]
    runLost = 0
    totalLost = 0
    lastJump = 0
    longestRun = 0
    totalSamples = len(rawSamples)
    badSampleFlag = False
    sp = 0
    enterSp = 0
    camera = None
    if rawSamples[0].stage == 'a':
      camera = camera1
    else:
      camera = cameras[rawSamples[0].trial]
    cameraX = camera.boxes[raw.index].x
    cameraY = camera.boxes[raw.index].y

    for (raw, ms, vx, vy, moveAmount) in zip(rawSamples, ms, vxs, vys, moveAmounts):
      if (raw.trial, raw.stage) not in cleanTrials and (abs(raw.x - cameraX) <= 8 or abs(raw.y - cameraY) <= 5):
        totalLost += 1
        continue

      if ms != prevMS:
        sp = (dist(raw.x, raw.y, prevX, prevY) / (ms-prevMS))
      else:
        sp = 0

      prevX = raw.x
      prevY = raw.y
      prevMS = ms
      runLost = 0

      crayfish = Crayfish(ms, raw.x, raw.y, vx, vy, raw.rotation, raw.height, raw.width, sp)
      refinedSamples.append(crayfish)
    print("percent lost = " + str(100.0 * (float(totalLost)/float(totalSamples))))
    #print("longest run lost: " + str(longestRun))
    refined.append(refinedSamples)

  filteredRefined = refined
  return filteredRefined

def crayfishCSV(crayfish):
    """ Turn a crayfish's data into CVS output """
    sp = math.sqrt(crayfish.xVel*crayfish.xVel + crayfish.yVel*crayfish.yVel)
    return ",".join(map(str, [crayfish.ms, crayfish.x, crayfish.y, crayfish.xVel, crayfish.yVel, sp, crayfish.rotation, crayfish.height, crayfish.width]))

def outgest(session):
  """ Write out the results of parsing a session's worth of data """

  # for each crayfish
  for (index, crayfishes) in zip(range(0, 6), session.sampleSet):
    fileName = "/".join([outDir, session.trialName, session.sessionName + "_" + str(index) + ".csv"])

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
          splitPath = string.split(path, "/")
          if len(splitPath) > 1:
              subfolder = splitPath[2]
              fileList += map(lambda fileName : (subfolder, fileName), files)
  return fileList


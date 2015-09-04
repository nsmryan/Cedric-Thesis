import numpy
import os
import math
from matplotlib import pyplot as plt
from CrayfishLib import *

def processSession(session):
  """ Main processing function. This function processes one recording session """
  palette = ['#db5e0c', '#14660d', '#460C67', '#d40607', '#cb971a', '#0c5b67']
  rainbox = ['#ff0000', '#ff7f00', '#ffff00', '#00ff00', '#0000ff', '#4b0082', '#8f00ff']
  coolColor = ['#002447']
  plt.rc('axes', color_cycle = palette)

  xyMovement(session)

  velHist(session, True)
  velHist(session, False)

  velOverTime(session)

  #xyOverTime(session)

  #xyFreq(session)

def velOverTime(session):
  """ create a graph of the speed of all the crayfish over time in a recording session """
  fig = plt.figure(1)
  for (index, crayfishes) in zip(range(0, len(session.sampleSet)), session.sampleSet):
    plotVelocities(fig, index, crayfishes)

  fig.tight_layout()
  fig.set_size_inches(12, 12)
  plt.savefig(outputPath(session) + "_vels.png")
  plt.close(fig)
  plt.clf()

def plotVelocities(figure, index, crayfishes):
  subplot = figure.add_subplot(6, 1, index)
  ms = [crayfish.ms for crayfish in crayfishes]
  xvs = [crayfish.xVel for crayfish in crayfishes]
  yvs = [crayfish.yVel for crayfish in crayfishes]
  plt.plot(ms, map(lambda (x, y) : math.sqrt(x*x + y*y), zip(xvs, yvs)))
  plt.xlabel("Time (seconds)")
  plt.ylabel("Speed (cm/second)")
  plt.title("Speed of crayfish " + str(index))

def velHist(session, noZeros):
  """ create a histogram of the speed of all the crayfish in a recording session """
  fig = plt.figure(1)
  for (index, crayfishes) in zip(range(0, len(session.sampleSet)), session.sampleSet):
    plotVelHist(noZeros, fig, index, crayfishes)

  zerosStr = ""
  if noZeros:zerosStr = "_no0s"

  fig.tight_layout()
  fig.set_size_inches(12, 12)
  plt.savefig(outputPath(session) + "_speedhist" + zerosStr + ".png")
  plt.close(fig)
  plt.clf()

def plotVelHist(noZeros, figure, index, crayfishes):
  subplot = figure.add_subplot(6, 1, index)
  ms = [crayfish.ms for crayfish in crayfishes]
  xvs = [crayfish.xVel for crayfish in crayfishes]
  yvs = [crayfish.yVel for crayfish in crayfishes]
  bins = numpy.arange(0, 0.2, 0.001)
  speeds = map(lambda (x, y) : math.sqrt(x*x + y*y), zip(xvs, yvs))
  if noZeros: speeds = filter(lambda speed : speed > 0, speeds)
  plt.hist(speeds, bins)
  plt.xlabel("X Position")
  plt.ylabel("Prob")
  plt.title("X Frequency for crayfish " + str(index))

def xyOverTime(session):
  # position over time
  """ create a graph of the x position a y position for each crayfish for each recording session """
  for (index, crayfishes) in zip(range(0, len(session.sampleSet)), session.sampleSet):
    plotXYs(fig, index, crayfishes)

def plotXYs(figure, index, crayfishes):
  fig = plt.figure(1)
  for crayfish in crayfishes:
    subplotX = fig.add_subplot(6, 2, index * 6 + 0)
    subplotY = fig.add_subplot(6, 2, index * 6 + 1)
    ms  = [crayfish.ms for crayfish in crayfishes]
    xvs = [crayfish.xVel for crayfish in crayfishes]
    yvs = [crayfish.yVel for crayfish in crayfishes]
    plt.plot(ms, map(lambda (x, y) : math.sqrt(x*x + y*y), zip(xvs, yvs)))
    plt.xlabel("Time (seconds)")
    plt.ylabel("Speed (cm/second)")
    subplotX.title("X Position of " + str(index))
    subplotX.title("Y Position of " + str(index))
  plt.title("X and Y Positions of " + str(index))

  fig.tight_layout()
  fig.set_size_inches(12, 24)
  plt.savefig(outputPath(session) + "_xys.png")
  plt.close(fig)
  plt.clf()

def xyMovement(session):
  """ create a plot of the positions of all the crayfish in a recording session """
  for (index, crayfish) in zip(range(0, len(session.sampleSet)),session.sampleSet):
    plotMovement(index, crayfish)
  plt.title("X vs Y")
  fig = plt.figure(1)
  fig.set_size_inches(24, 24)
  plt.savefig(outputPath(session) + "_positions" + ".png")
  plt.clf()

def plotMovement(index, samples):
  xs = [sample.x for sample in samples]
  ys = [sample.y for sample in samples]
  plt.plot(xs, ys)
  plt.xlabel("X position for crayfish " + str(index))
  plt.ylabel("Y position for crayfish " + str(index))

def outputPath(session):
  """ This is a utility function for creating file names from session data """
  return outDir + "/" + session.trialName + "/" + session.sessionName

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



def sessionGraphs(session):
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
  time  = [crayfish.time   for crayfish in crayfishes]
  xvs = [crayfish.xVel for crayfish in crayfishes]
  yvs = [crayfish.yVel for crayfish in crayfishes]
  speeds = [crayfish.speed for crayfish in crayfishes]
  plt.plot(time, speeds)
  plt.xlabel("Time (seconds)")
  plt.ylabel("Speed (cm/second)")
  plt.title("Speed of crayfish " + str(index+1))


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
  time  = [crayfish.time   for crayfish in crayfishes]
  volumes = [crayfish.volume for crayfish in crayfishes]
  plt.plot(time, volumes)
  plt.xlabel("Time (seconds)")
  plt.ylabel("Volume (cm/second)")
  plt.title("Volume of crayfish " + str(index+1))

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
  time = [crayfish.time for crayfish in crayfishes]
  speeds = [crayfish.speed for crayfish in crayfishes]
  if noZeros: speeds = [speed for speed in speeds if speed > speedThreshold]

  maxSpeed = max(speeds)
  bins = numpy.arange(0, maxSpeed, maxSpeed/100)

  plt.hist(speeds, bins)
  plt.xlabel("Speed")
  plt.ylabel("Frequency")
  plt.title("Speed Frequency for crayfish " + str(index+1))

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

  time  = [sample.time for sample in samples]
  xs = [sample.x for sample in samples]
  ys = [sample.y for sample in samples]

  subplotX.set_title("X Position of " + str(index+1))
  subplotX.set_xlabel("X Position")
  subplotX.set_ylabel("Time (seconds)")
  subplotX.plot(time, xs)

  subplotY.set_title("Y Position of " + str(index+1))
  subplotY.set_xlabel("Y Position)")
  subplotY.set_ylabel("Time (seconds)")
  subplotY.plot(time, ys)

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
  plt.xlabel("X position for crayfish " + str(index+1))
  plt.ylabel("Y position for crayfish " + str(index+1))

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
          print("Ignoring " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n")
          continue

        progressText = "Processing " + trialName + " " + sessionName + " " + str(crayfishIndex+1) + "\n"
        print(progressText)

        refinedData = retrieveData(trialName, sessionName, crayfishIndex)

        totalDistance = calCTotalDistance(refinedData)
        distMap[trialTreatments[trialName]].append(totalDistance)
        allDistances.append((trialName, crayfishIndex, totalDistance))

        outFile.write("t_" + str(trialTreatments[trialName]) + ", " + trialName + "_" + str(crayfishIndex+1) + ", " + str(totalDistance) + "\n")

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

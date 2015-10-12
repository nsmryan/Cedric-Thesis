
from CrayfishLib import *
from CrayfishPreProcess import *
from CrayfishPostProcess import *
import sys

#import cProfile
import profile
import re


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
            with open(trialOutFile, 'w') as outFile:
                # break the data into records
                dataset = parseDataSet(trialName, getStage(sessionName), rawData)

                # create nicer data
                crayfishes = refineDataSet(dataSummaryFile, dataset)

                # perform the main processing
                session = Session(trialName, sessionName, crayfishes)

                #save session data to the trial it is associated with
                trials[trialName].append(sessionStats(session))

                processSession(session)

                #save the resulting cleaned-up data to a file 
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

    if len(sys.argv) > 3:
      profiling = [sys.argv[3]] == "p"
    else:
      profiling = False

    if not profiling:
      processExperiment(trialsToRun, stagesToRun)
    else:
      print("Profiling\n")
      profile.run('processExperiment(trialsToRun, stagesToRun);print')

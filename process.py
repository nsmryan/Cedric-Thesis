
from CrayfishLib import *
from preprocess import *
from postprocess import *
import sys


def processExperiment():
    """ This is the main function for the whole program. Start here """

    print("Starting Processing")

    if len(sys.argv) > 1:
      trialsToRun = [sys.argv[1]]
    else:
      trialsToRun = ["Trial 1", "Trial 2", "Trial 3", "Trial 4",
                "Trial 5", "Trial 6", "Trial 7", "Trial 8",
                "Trial 9", "Trial 11", "Trial 11", "Trial 12"]

    if len(sys.argv) > 2:
      stagesToRun = [sys.argv[2]]
    else:
      stagesToRun = "abc"

    # Ensure the output directory exists
    if not os.path.exists(outDir): os.makedirs(outDir)

    # find all data files to process
    files = allFiles(inDir)

    # for each file: read the file, clean up the data, create some records, and create graphs
    for (path, sessionName) in files:
        if path not in trialsToRun:continue

        if getStage(sessionName) not in stagesToRun:continue

        filePath = path + "/" + sessionName

        # for each session (1 file)
        with open(inDir + "/" + filePath, 'r') as inFile:
            trialOutPath = outDir + "/" + path
            trialOutFile = trialOutPath + "/" + sessionName

            # ensure that there is a directory to record results in
            if not os.path.exists(trialOutPath): os.makedirs(trialOutPath)

            # open the file and perform processing
            with open(trialOutFile, 'w') as outFile:
                # read from the file
                rawData = ingest(trialOutFile, inFile)

                # break the data into records
                dataset = parseDataSet(path, getStage(sessionName), rawData)

                # create nicer data
                crayfishes = refineDataSet(dataset)

                # perform the main processing
                session = Session(path, sessionName, crayfishes)

                #save session data to the trial it is associated with
                trials[path].append(sessionStats(session))

                processSession(session)

                #save the resulting cleaned-up data to a file 
                outgest(session)
    summarizeDataset()

if __name__ == "__main__":
  processExperiment()

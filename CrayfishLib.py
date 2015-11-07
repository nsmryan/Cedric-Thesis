import math
import os
from enum import Enum

outDir = "output"
inDir = "input"

ignoreTrials = []
ignoreCrayfish = []

runFiltering = True

numColumns = 37 # ms plus 6 records of 6 fields each

numFields = 6 # 6 fields per crayfish

numCrayfish = 6 # 6 crayfish per dataset

crayfishHeader = "time (seconds), x (mm), y (mm), x velocity (mm/second), y velocity (mm/second), speed (mm/second), rotation (degrees), length (mm), width (mm), location\n"

#the trial name is part of the crayfish id
anovaHeader = "treatment, time, crayfishid, " # add on name of numerical attribute at end

speedThreshold = 1

mmPerPixelX = 127/276
mmPerPixelY = 76/164

#xErrorEdge = 8
#yErrorEdge = 5
xErrorEdge = 7
yErrorEdge = 5

xJitter = 2
yJitter = 2

speedCap = 100000

filterWindow = 5

graphing = False

speedCapMM = 70

cedricIndices = [0, 2, 4, 1, 3, 5]
indexRange = range(1, 7)

# a box holding one crayfish
class Box:
  def __init__(self, boxLocation, boxExtents):
        self.location = boxLocation
        self.extents = boxExtents

  def determineLocation(self, x, y):
    leftRight = False
    topBottom = False

    if x <= self.location[0] or x >= (self.location[0] + self.extents[0]):
      leftRight = True

    if y <= self.location[1] or y >= (self.location[1] + self.extents[1]):
      topBottom = True

    if not leftRight and not topBottom:
      location = "middle"
    elif (leftRight or topBottom) and (not leftRight or not topBottom):
      location = "edge"
    elif leftRight and topBottom:
      location = "corner"
    else:
      print("location could not be determined")

    #print("(x, y) = " + str((x, y)))
    #print("locations = " + str(self.location))
    #print("extents = " + str(self.extents))
    #print("location = " + str(location))
    #print("\n\n")

    return location 


# an camera contains 6 boxes in view during the session
class Camera:
    def __init__(self, boxes, innerBoxes, pixelDims):
        self.boxes = boxes
        self.innerBoxes = innerBoxes
        self.pixelDims = pixelDims

# a sample from the raw data
class Sample:
    def __init__(self, time, crayfish):
      self.time = time
      self.crayfish = crayfish

# a crayfish's raw data sample
class RawSample:
    def __init__(self, time, index, trial, stage, xPos, yPos, rotation, height, width):
        self.time = time
        self.index = index
        self.trial = trial
        self.stage = stage
        self.x = xPos
        self.y = yPos
        self.rotation = rotation 
        self.height = height
        self.width = width

# a crayfishes cleaned-up data sample
class Crayfish:
    def __init__(self, time, xPos, yPos, xVel, yVel, rotation, height, width, speed, location):
        self.time = time
        self.x = xPos
        self.y = yPos
        self.xVel = xVel
        self.yVel = yVel
        self.rotation = rotation 
        self.height = height
        self.width = width
        self.speed = speed
        self.volume = width * height
        self.location = location

# All data associated with a single crayfish
class CrayfishData:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

# Summary statistics
class SessionStats:
  def __init__(self, sessionName, sessionType, avgSpeeds):
    self.sessionName = sessionName
    self.sessionType = sessionType
    self.avgSpeeds = avgSpeeds

# a recording session of the camera
class Session:
  def __init__(self, trialName, sessionName, sampleSet):
    self.trialName = trialName
    self.sessionName = sessionName
    self.sampleSet = sampleSet

# a full trial with all recording sessions
class Trial:
  def __init__(self, trialName, sessions):
    self.trialName = trialName
    self.sessions = sessions

def transpose(lists):
   """ take a list of rows and turn it into a list of columns """
   if not lists: return []
   return list(map(lambda *row: list(row), *lists))

def diff(first, second, startTime, endTime):
  return (second - first) / (endTime - startTime)

def dervs(vs, times):
    return map(lambda v : diff(*v), zip(vs, vs[1:], times, times[0:]))

def sampleDist(sampleA, sampleB):
  return dist(sampleA.x, sampleA.y, sampleB.x, sampleB.y)

def sampleTimePassed(sample0, sample1):
  return (sample1.time - sample0.time)

def dist(a, b, aprime, bprime):
  return math.sqrt(pow(a - aprime, 2) + pow(b - bprime, 2))

def getStage(fileName):
  for letter in "abc":
    if letter in fileName:
      return letter
  print("could not determine stage of " + fileName)
  exit(1)

def ensureDir(dirName):
  if not os.path.exists(dirName): os.makedirs(dirName)

def safeAverage(nums):
  if len(nums) == 0:return 0
  return sum(nums)/len(nums)

def joinLists(lls):
  l = []
  for ls in lls:
    l = l + ls
  return l

def interlace(first, second):
  l = []
  for pair in zip(first, second):
    l.append(pair[0])
    l.append(pair[1])
  return l

def reindex(ls):
  return [ls[ix] for ix in cedricIndices]

# from the original Java program...
# for session a always use camera 1

camera1 = Camera([Box((629,  327),  (226,212)),
                  Box((865,  327),  (228,212)),
                  Box((1097, 327),  (229,212)),
                  Box((629,  540),  (226,214)),
                  Box((865,  540),  (228,214)),
                  Box((1097, 540),  (229,214))],
                 #inner boxes
                 [Box((679,	 372), (151, 132)),
                  Box((903,	 372), (151, 132)),
                  Box((1128, 372), (155, 132)),
                  Box((679,	 581), (151, 130)),
                  Box((903,	 581), (151, 130)),
                  Box((1128, 581), (155, 130))],
                 (0.457496, 0.456814))

camera2 = Camera([Box((608,  320), (237, 217)),
                  Box((846,  320), (225, 217)),
                  Box((1072, 320), (239, 217)),
                  Box((608,  538), (237, 215)),
                  Box((846,  538), (225, 215)),
                  Box((1072, 538), (239, 215))],
                 #inner boxes
                 [Box((663,  366), (148, 132)),
                  Box((885,  366), (146, 132)),
                  Box((1105, 366), (148, 132)),
                  Box((663,  574), (148, 130)),
                  Box((885,  574), (146, 130)),
                  Box((1105, 574), (148, 130))],
                 (0.4625, 0.464844))

camera3 = Camera([Box((600,  307), (238, 221)),
                  Box((837,  307), (228, 221)),
                  Box((1066, 307), (238, 221)),
                  Box((600,  529), (238, 216)),
                  Box((837,  529), (228, 216)),
                  Box((1066, 529), (238, 216))],
                 #inner boxes
                 [Box((654,  363), (146, 135)),
                  Box((874,  363), (148, 135)),
                  Box((1096, 363), (148, 135)),
                  Box((654,  572), (146, 130)),
                  Box((874,  572), (148, 130)),
                  Box((1096, 572), (148, 130))],
                 (0.460342, 0.463938))

#oldCamera2 = Camera([Box((600,307),  (238,221)),
#                     Box((837,307),  (228,221)),
#                     Box((1066,307), (238,221)),
#                     Box((600,529),  (238,216)),
#                     Box((837,529),  (228,216)),
#                     Box((1066,529), (238,216))],
#                     (0.4625, 0.464844))

cameras = {"Trial 1"  : camera3,
           "Trial 2"  : camera2,
           "Trial 3"  : camera3,
           "Trial 4"  : camera2,
           "Trial 5"  : camera3,
           "Trial 6"  : camera2,
           "Trial 7"  : camera3,
           "Trial 8"  : camera2,
           "Trial 9"  : camera2,
           "Trial 10" : camera3,
           "Trial 11" : camera2,
           "Trial 12" : camera3}

crayfishLengths = {"Trial 1"  : [1.5, 1.6, 1.8, 1.5, 1.5, 1.4],
                   "Trial 2"  : [1.4, 1.8, 1.6, 1.6, 1.5, 1.5],
                   "Trial 3"  : [1.6, 1.5, 1.5, 1.5, 1.6, 1.8],
                   "Trial 4"  : [1.5, 1.6, 1.4, 1.5, 1.6, 1.6],
                   "Trial 5"  : [1.6, 1.3, 1.6, 1.4, 1.6, 1.4],
                   "Trial 6"  : [1.8, 1.5, 1.6, 1.4, 1.4, 1.5],
                   "Trial 7"  : [1.6, 1.8, 1.5, 1.7, 1.6, 1.8],
                   "Trial 8"  : [1.5, 1.6, 1.8, 1.8, 1.8, 1.6],
                   "Trial 9"  : [2.1, 2.3, 2.3, 2.8, 2.9, 2.7],
                   "Trial 10" : [2.5, 2.4, 2.0, 2.3, 2.5, 2.7],
                   "Trial 11" : [2.4, 2.2, 2.3, 2.3, 2.3, 2.5],
                   "Trial 12" : [2.4, 2.1, 2.1, 2.3, 2.3, 2.3]}

motherIds = [5, 8, 11]

crayfishMothers = {"Trial 1"  : [5, 5, 5, 5,  5,  5],
                   "Trial 2"  : [5, 5, 5, 5,  5,  5],
                   "Trial 3"  : [5, 5, 5, 5,  5,  5],
                   "Trial 4"  : [5, 5, 5, 5,  5,  5],
                   "Trial 5"  : [5, 5, 5, 5,  5,  5],
                   "Trial 6"  : [5, 5, 5, 5,  5,  5],
                   "Trial 7"  : [5, 5, 5, 5,  5,  5],
                   "Trial 8"  : [5, 5, 5, 5,  5,  5],
                   "Trial 9"  : [8, 8, 8, 11, 11, 11],
                   "Trial 10" : [8, 8, 8, 11, 11, 11],
                   "Trial 11" : [8, 8, 8, 11, 11, 11],
                   "Trial 12" : [8, 8, 8, 11, 11, 11]}

# Treatment levels, as a dictionary
treatments = {0.0 : [], 0.5 : [], 5.0 : [], 50.0 : []}

treatmentNames = [0.0, 0.5, 5.0, 50.0]
trialNames  = ["Trial 1", "Trial 2", "Trial 3", "Trial 4", "Trial 5", "Trial 6", "Trial 7", "Trial 8", "Trial 9", "Trial 10", "Trial 11", "Trial 12"]
sessionNames = ['a', 'b', 'c']

trials = {"Trial 1"  : [],
          "Trial 2"  : [],
          "Trial 3"  : [],
          "Trial 4"  : [],
          "Trial 5"  : [],
          "Trial 7"  : [],
          "Trial 6"  : [],
          "Trial 8"  : [],
          "Trial 9"  : [],
          "Trial 10" : [],
          "Trial 11" : [],
          "Trial 12" : []}

trialTreatments = {"Trial 1"  : 0.0,
                   "Trial 2"  : 0.5,
                   "Trial 3"  : 5.0,
                   "Trial 4"  : 50.0,
                   "Trial 5"  : 0.0,
                   "Trial 6"  : 5.0,
                   "Trial 7"  : 50.0,
                   "Trial 8"  : 0.5,
                   "Trial 9"  : 0.5,
                   "Trial 10" : 0.0,
                   "Trial 11" : 50.0,
                   "Trial 12" : 5.0}

treatmentTrials = {0.0  : ["Trial 1", "Trial 5", "Trial 10"],
                   0.5  : ["Trial 2", "Trial 8", "Trial 9"],
                   5.0  : ["Trial 3", "Trial 6", "Trial 12"],
                   50.0 : ["Trial 4", "Trial 7", "Trial 11"]}
                   

cleanTrials = [("Trial 1", 'b'),
               ("Trial 1", 'c'),
               ("Trial 8",  'c'),
               ("Trial 9",  'b'),
               ("Trial 9",  'c'),
               ("Trial 10",  'b'),
               ("Trial 10",  'c'),
               ("Trial 11",  'b'),
               ("Trial 11",  'c'),
               ("Trial 12",  'b'),
               ("Trial 12",  'c')]

locationNames = ["edge", "corner", "middle"]

#ignoreTrials = ["Trial 9",
#                "Trial 10",
#                "Trial 11",
#                "Trial 12"]
#ignoreCrayfish = [("Trial 6", "b", 2),
#                  ("Trial 4", "b", 1),
#                  ("Trial 4", "c", 1),
#                  ("Trial 5", "b", 5)]
#ignoreCrayfish = [("Trial 4", "a", 4),
#                  ("Trial 6", "a", 1),
#                  ("Trial 6", "a", 5),
#                  ("Trial 7", "a", 2),
#                  ("Trial 5", "b", 5),
#                  ("Trial 6", "b", 1),
#                  ("Trial 6", "b", 5),
#                  ("Trial 7", "b", 2),
#                  ("Trial 4", "c", 4),
#                  ("Trial 6", "c", 1),
#                  ("Trial 6", "c", 5),
#                  ("Trial 6", "c", 2)]

import math

outDir = "./output"
inDir = "./input"

numColumns = 37 # ms plus 6 records of 6 fields each

numFields = 6 # 6 fields per crayfish

numCrayfish = 6 # 6 crayfish per dataset
crayfishHeader = "time (seconds), x, y, x velocity, y velocity, speed, rotation, length, width\n"

# a box holding one crayfish
class Box:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

# an camera contains 6 boxes in view during the session
class Camera:
    def __init__(self, boxes):
        self.boxes = boxes

# a sample from the raw data
class Sample:
    def __init__(self, ms, crayfish):
      self.ms = ms
      self.crayfish = crayfish

# a crayfish's raw data sample
class RawSample:
    def __init__(self, ms, index, trial, stage, xPos, yPos, rotation, height, width):
        self.ms = ms
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
    def __init__(self, ms, xPos, yPos, xVel, yVel, rotation, height, width, speed):
        self.ms = ms
        self.x = xPos
        self.y = yPos
        self.xVel = xVel
        self.yVel = yVel
        self.rotation = rotation 
        self.height = height
        self.width = width
        self.speed = speed

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

def diff(first, second, startTime, endTime):
  return (second - first) / (endTime - startTime)

def dervs(vs, times):
    return map(lambda v : diff(*v), zip(vs, vs[1:], times, times[0:]))

def dist(a, b, aprime, bprime):
  return math.sqrt(pow(a - aprime, 2) + pow(b - bprime, 2))

def getStage(fileName):
  for letter in "abc":
    if letter in fileName:
      return letter
  print("could not determine stage of " + fileName)
  exit(1)

# from the original Java program...
# for acclication always camera 1

camera1 = Camera([Box(629,327,226,212),
                  Box(865,327,228,212),
                  Box(1097,327,229,212),
                  Box(629,540,226,214),
                  Box(865,540,228,214),
                  Box(1097,540,229,214)])

camera2 = Camera([Box(608,320,237,217),
                  Box(846,320,225,217),
                  Box(1072,320,239,217),
                  Box(608,538,237,215),
                  Box(846,538,225,215),
                  Box(1072,538,239,215)])

camera3 = Camera([Box(600,307,238,221),
                  Box(837,307,228,221),
                  Box(1066,307,238,221),
                  Box(600,529,238,216),
                  Box(837,529,228,216),
                  Box(1066,529,238,216)])

oldCamera2 = Camera([Box(600,307,238,221),
                      Box(837,307,228,221),
                      Box(1066,307,238,221),
                      Box(600,529,238,216),
                      Box(837,529,228,216),
                      Box(1066,529,238,216)])

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

# Treatment levels, as a dictionary
treatments = {"0.0" : [], "0.5" : [], "5.0" : [], "50.0" : []}

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


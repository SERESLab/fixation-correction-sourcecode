import math


class Distance(object):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.distance = (math.sqrt(math.pow(self.point2.x-self.point1.x, 2)))


class Aoi(object):
    def __init__(self, kind, name, x, y, width, height):
        self.kind = kind
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def containsPoint(self, pointx, pointy):
        if pointx > self.x and pointx < (self.x + self.width):
            if pointy > self.y and pointy < (self.y + self.width):
                return True
        return False
#    def contains_point(self, point):



class Point(object):
    def __init__(self, x, y, duration, startTime, endTime, aoi, xCorrected, yCorrected, filename):
        self.x = x
        self.y = y
        self.duration = duration
        self.startTime = startTime
        self.endTime = endTime
        self.aoi = aoi
        self.xCorrected = xCorrected
        self.yCorrected = yCorrected
        self.filename = filename
        self.autoxCorrected = None
        self.autoyCorrected = None

    def xCorrectionCoefficient(self):
        if not self.autoxCorrected:
            return (self.autoxCorrected-self.x)/(self.xCorrected-self.y)
        else:
            return False

    def yCorrectionCoeffieient(self):
        if not self.autoyCorrected:
            return (self.autoyCorrected-self.y)/(self.yCorrected-self.y)
        else:
            return False


class SessionsOfPoints:
    def __init__(self):
        self.listOfFiles = {}

    def add_session(self, session, filename):
        self.listOfFiles[filename] = session

    def get_session(self, filename):
        return self.listOfFiles[filename]

    def get_number_of_sessions(self):
        return len(self.listOfFiles)


class FileOfClusters:
    def __init__(self):
        self.clusterDict = {}

    def add_cluster(self, cluster, filename):
        self.clusterDict[filename] = cluster

    def get_cluster(self, filename):
        return self.clusterDict[filename]

    def get_number_of_clusters(self):
        #number_of_clusters = 0
        #for key in self.clusterDict:
        #    for i in self.clusterDict[key]:
        #        number_of_clusters += 1
        #return number_of_clusters
        number_of_clusters = 0
        for i in self.clusterDict:
            number_of_clusters += len(i)
        return number_of_clusters / len(self.clusterDict)

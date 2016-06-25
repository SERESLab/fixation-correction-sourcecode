"""
This file is part of Fixation-Correction-Sourcecode.

Fixation-Correction-Sourcecode is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Fixation-Correction-Sourcecode is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Fixation-Correction-Sourcecode.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2015
Author: Chris Palmer
"""

import math


class Distance(object):
    """
    <class_name> (<constructor params>)
    CONSTRUCTION:

    METHOD(S):
    <estimated return type> <method name> (<params>)
    PRECONDITION(S):
    POSTCONDITION(S):

    MEMBER VARIABLE(S):
    <name> <unit (optional)>
    PURPOSE:
    """
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.distance = (math.sqrt(math.pow(self.point2.x-self.point1.x, 2)))


class Aoi(object):
    """
    <class_name> (<constructor params>)
    CONSTRUCTION:

    METHOD(S):
    <estimated return type> <method name> (<params>)
    PRECONDITION(S):
    POSTCONDITION(S):

    MEMBER VARIABLE(S):
    <name> <unit (optional)>
    PURPOSE:
    """
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
    """
    <class_name> (<constructor params>)
    CONSTRUCTION:

    METHOD(S):
    <estimated return type> <method name> (<params>)
    PRECONDITION(S):
    POSTCONDITION(S):

    MEMBER VARIABLE(S):
    <name> <unit (optional)>
    PURPOSE:
    """
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
    """
    <class_name> (<constructor params>)
    CONSTRUCTION:

    METHOD(S):
    <estimated return type> <method name> (<params>)
    PRECONDITION(S):
    POSTCONDITION(S):

    MEMBER VARIABLE(S):
    <name> <unit (optional)>
    PURPOSE:
    """
    def __init__(self):
        self.listOfFiles = {}

    def add_session(self, session, filename):
        self.listOfFiles[filename] = session

    def get_session(self, filename):
        return self.listOfFiles[filename]

    def get_number_of_sessions(self):
        return len(self.listOfFiles)


class FileOfClusters:
    """
    <class_name> (<constructor params>)
    CONSTRUCTION:

    METHOD(S):
    <estimated return type> <method name> (<params>)
    PRECONDITION(S):
    POSTCONDITION(S):

    MEMBER VARIABLE(S):
    <name> <unit (optional)>
    PURPOSE:
    """
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

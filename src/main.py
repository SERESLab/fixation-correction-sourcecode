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

import make_points
import make_cluster
import aoi_import
import correct_clusters
import math
import csv


def find_number_of_corrected_points(list_of_clusters):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    count = 0
    for cluster in list_of_clusters:
        for pointInCluster in cluster:
            if pointInCluster.autoxCorrected is not None and pointInCluster.autoyCorrected is not None:
                count += 1
    return count


def find_number_of_points(list_of_clusters):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    count = 0
    for cluster in list_of_clusters:
        for pointInCluster in cluster:
            count += 1
    return count


def find_autocorrected_distance(point):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    return math.sqrt(math.pow(int(point.autoxCorrected - point.xCorrected), 2) +
                     math.pow(int(point.autoyCorrected - point.yCorrected), 2))


def find_corrected_distance(point):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    return math.sqrt(math.pow(int(point.xCorrected - point.x), 2) +
                     math.pow(int(point.yCorrected - point.y), 2))


def accuracy_by_aoi(list_of_aois, list_of_clusters):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    numberOfAccuratePoints = 0
    number_of_points = 0
    for cluster in list_of_clusters:
        for point in cluster:
            number_of_points += 1
            for aoi in list_of_aois:
                if aoi.containsPoint(point.xCorrected, point.yCorrected) and aoi.containsPoint(point.autoxCorrected, point.autoyCorrected):
                    numberOfAccuratePoints += 1
                    break
    if number_of_points == 0:
        if numberOfAccuratePoints > 0:
            return 'WTF?'
        else:
            return 'No points'
    else:
        return float(numberOfAccuratePoints) / float(number_of_points)


# -------------------Main structure----------------------------

clustersbyFile = {}
aoi_dict = {}
output = open('test.txt', 'w')
outputClusters = open('cluster.txt', 'w')
fileOfPoints = make_points.make_points()

# todo functionalize these loops

for filename in fileOfPoints:
    aoi_dict[filename] = aoi_import.get_aoi(filename)
    # plot_points.plot_points(fileOfPoints[filename], filename)
    output.write(filename+'\n')
    for point in fileOfPoints[filename]:
        output.write(str(point.startTime)+'\n')
    if len(fileOfPoints[filename]) < 1:
        print filename
        print "error"
        continue
    # do the normal cluster thing
    clustersbyFile[filename] = make_cluster.make_cluster_refactor(fileOfPoints[filename])
    # return one cluster for entire file
    #clustersbyFile[filename] = make_cluster.make_one_cluster_per_file(fileOfPoints[filename])
    # return one cluster for each point * this one performs better. or at least makes better numbers
    #clustersbyFile[filename] = make_cluster.make_one_cluster_per_point(fileOfPoints[filename])

for aoifilename in aoi_dict:
    correct_clusters.correct_cluster(clustersbyFile[aoifilename], aoi_dict[aoifilename])

for file_name in clustersbyFile:
    outputClusters.write(file_name+'\n')
    for listOfPoints in clustersbyFile[file_name]:
        outputClusters.write('------------------------------------------\n')
        outputClusters.write(str(len(listOfPoints))+'\n')
        for point in listOfPoints:
            if point.autoxCorrected != point.x or point.autoyCorrected != point.y:
                if find_corrected_distance(point) == 0:
                    outputClusters.write("SHOULD NOT HAVE BEEN CORRECTED\n")
                outputClusters.write('improvement ' + str(find_corrected_distance(point) - find_autocorrected_distance(point)) + '\n')
            else:
                outputClusters.write("should've been corrected " + str(find_corrected_distance(point))+'\n')

with open('correction_ratio.txt', 'w+') as aoi_accuracy:
    for filename in clustersbyFile:
        aoi_accuracy.write(filename + ',' + str(accuracy_by_aoi(aoi_dict[filename], clustersbyFile[filename])) + ',' + str(find_number_of_corrected_points(clustersbyFile[filename])) + ','+ str(find_number_of_points(clustersbyFile[filename])) + '\n')

for filename in clustersbyFile:
    with open('corrected-aoi/'+filename, 'w+') as data_csv_file:
        fieldnames = ['start-time', 'end-time','aoi','x','y','x-man-cor','y-man-cor','x-auto-cor','y-auto-cor', 'x-improvement', 'y-improvement']
        writer = csv.DictWriter(data_csv_file, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
        writer.writeheader()
        for listOfPoints in clustersbyFile[filename]:
            for point in listOfPoints:
                writer.writerow({'start-time': point.startTime,
                                 'end-time': point.endTime,
                                 'aoi': point.aoi,
                                 'x': point.x,
                                 'y': point.y,
                                 'x-man-cor': point.xCorrected,
                                 'y-man-cor': point.yCorrected,
                                 'x-auto-cor': point.autoxCorrected,
                                 'y-auto-cor': point.autoyCorrected,
                                 'x-improvement': abs(int(point.x - point.autoxCorrected)-int(point.x - point.xCorrected)),
                                 'y-improvement': abs(int(point.y - point.autoyCorrected)-int(point.y - point.yCorrected))})
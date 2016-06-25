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


def correct_cluster(listofclusters, listofaois):
    """
    None correct_cluster(list[list[point]], list[AOI])
    PRECONDITION(S):
        given a list[list[point]] (list of clusters) and a list of AOIs
        Point has the properties:
            -autoxCorrected - the x coordinate of a point that has been corrected automatically
            -autoyCorrected - the y coordinate of a point that has been corrected automatically

            -x - original x coordinate of a point
            -y - original y coordinate of a point

    POSTCONDITION(S):
        all autoCorrect points in the list[list[point]] are set to the value of their original points
        if a cluster in the list[list[]] scores 0 from the scoring function
            the cluster is moved toward the nearest aoi

        hillclimb is called on the current state of each cluster

        note: all passes are done by reference
    """
    for cluster in listofclusters:
        for point in cluster:
            point.autoxCorrected = point.x
            point.autoyCorrected = point.y
        if find_score_multi_aoi(cluster, listofaois) == 0:
            move_cluster_toward_aoi(cluster, listofaois)

        hillclimb(cluster, listofaois)


def find_score_multi_aoi(cluster, listofaois):
    """
    float find_score_multi_aoi (list[point], list[AOI])
    PRECONDITION(S):
        given a list of points and a list of AOIs
        Point has the properties:

        AOI has the properties:
    POSTCONDITION(S):
    """
    list_of_points_in_aoi = []
    debug_points = []
    for point in cluster:
        if debug_points.count(point) > 0:
            # todo throw an exception?
            print "point repeat error"
        debug_points.append(point)
        for aoi in listofaois:
            if point_in_aoi(point, aoi):
                if list_of_points_in_aoi.count(point) == 0:
                    list_of_points_in_aoi.append(point)
    return float(len(list_of_points_in_aoi))/float(len(cluster))


def point_in_aoi(point, aoi):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    if point.autoxCorrected >= aoi.x and point.autoxCorrected <= (aoi.x + aoi.width):
        if point.autoyCorrected >= aoi.y and point.autoyCorrected <= (aoi.y + aoi.height):
            return True
        else:
            return False
    return False
# def find_score_single_aoi(cluster, aoi):


def hillclimb(cluster, listofaois):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    movevertdistance = get_maxY(cluster) - get_minY(cluster)
    movehordistance = get_maxX(cluster) - get_minX(cluster)
    hillclimbloop = 0
    shift_dir(cluster, 'left', movehordistance)
    left = find_score_multi_aoi(cluster, listofaois)
    shift_dir(cluster, 'right', movehordistance)
    shift_dir(cluster, 'right', movehordistance)
    right = find_score_multi_aoi(cluster, listofaois)
    shift_dir(cluster, 'left', movehordistance)
    shift_dir(cluster, 'up', movevertdistance)
    up = find_score_multi_aoi(cluster, listofaois)
    shift_dir(cluster, 'down', movevertdistance)
    shift_dir(cluster, 'down', movevertdistance)
    down = find_score_multi_aoi(cluster, listofaois)
    shift_dir(cluster, 'up', movevertdistance)
    current = find_score_multi_aoi(cluster, listofaois)
    while movevertdistance >= 1 or movehordistance >= 1:
        while current < left or current < right or current < up or current < down:
            hillclimbloop += 1
            print("hillclimb loop " + str(hillclimbloop))
            if left > current:
                shift_dir(cluster, 'left', movehordistance)
            elif right > current:
                shift_dir(cluster, 'right', movehordistance)
            elif up > current:
                shift_dir(cluster, 'up', movevertdistance)
            elif down > current:
                shift_dir(cluster, 'down', movevertdistance)

            shift_dir(cluster, 'left', movehordistance)
            left = find_score_multi_aoi(cluster, listofaois)
            shift_dir(cluster, 'right', movehordistance)
            shift_dir(cluster, 'right', movehordistance)
            right = find_score_multi_aoi(cluster, listofaois)
            shift_dir(cluster, 'left', movehordistance)
            shift_dir(cluster, 'up', movevertdistance)
            up = find_score_multi_aoi(cluster, listofaois)
            shift_dir(cluster, 'down', movevertdistance)
            shift_dir(cluster, 'down', movevertdistance)
            down = find_score_multi_aoi(cluster, listofaois)
            shift_dir(cluster, 'up', movevertdistance)
            current = find_score_multi_aoi(cluster, listofaois)
        movevertdistance = int(movevertdistance/2)
        movehordistance = int(movehordistance/2)
    return


def shift_dir(cluster, direction, distance):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    if direction == 'left':
        for point in cluster:
            point.autoxCorrected -= distance
    if direction == 'right':
        for point in cluster:
            point.autoxCorrected += distance
    if direction == 'up':
        for point in cluster:
            point.autoyCorrected -= distance
    if direction == 'down':
        for point in cluster:
            point.autoyCorrected += distance

    return


def move_cluster_toward_aoi(cluster, listofaois):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    nearestaoi = find_nearest_aoi(cluster, listofaois)
    while find_score_multi_aoi(cluster, listofaois) == 0:
        moved = False
        if nearestaoi.x < get_minX(cluster):
            #print('left')
            shift_dir(cluster, 'left', 1)
            moved = True
        elif nearestaoi.x > get_minX(cluster):
            #print('right')
            shift_dir(cluster, 'right', 1)
            moved = True
        if nearestaoi.y < get_minY(cluster):
            #print('up')
            shift_dir(cluster, 'up', 1)
            moved = True
        elif nearestaoi.y > get_minY(cluster):
            #print('down')
            shift_dir(cluster, 'down', 1)
            moved = True
        if moved:
            break


def get_maxX(cluster):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    maxX = 0
    for point in cluster:
        if point.autoxCorrected > maxX:
            maxX = point.autoxCorrected
    return maxX


def get_maxY(cluster):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    maxY = 0
    for point in cluster:
        if point.autoyCorrected > maxY:
            maxY = point.autoyCorrected
    return maxY

def get_minX(cluster):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    minX = cluster[0].x
    for point in cluster:
        if point.autoxCorrected < minX:
            minX = point.autoxCorrected
    return minX


def get_minY(cluster):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    minY = cluster[0].y
    for point in cluster:
        if point.autoyCorrected < minY:
            minY = point.autoyCorrected
    return minY


def find_nearest_aoi(cluster, listofaois):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    maxX = get_maxX(cluster)
    maxY = get_maxY(cluster)
    minX = get_minX(cluster)
    minY = get_minY(cluster)
    nearestaoi = listofaois[0]
    for i in range(1, len(listofaois)):
        if abs(listofaois[i].x - minX) < abs(nearestaoi.x - minX) and abs(listofaois[i].y - minY) < abs(nearestaoi.y - minY):
            nearestaoi = listofaois[i]

    return nearestaoi
import objects
import math
import numpy
import globalVariables

# global variable(s)

NUMBER_OF_ELEMENTS_TO_REMOVE = 0

# function to check if object exists in list

def make_one_cluster_per_file(listOfPoints):
    returnList = []
    returnList.append(listOfPoints)
    return returnList


def make_one_cluster_per_point(listOfPoints):
    returnList = []
    for point in listOfPoints:
        returnList.append([point])

    return returnList

def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


f = globalVariables.files

def median(lst):
    return numpy.median(numpy.array(lst))

def create_cluster(sessionpoints):
    # sessionpoints is a list of points
    print("create cluster method")


# Take list of points
# Return list of clusters
def make_cluster_refactor(listOfPoints):
    # variables
    # lookbackQueue[0]  = oldest element
    # lookbackQueue[-1] = newest element
    lookbackQueue = []
    listOfClusters = []
    totalMedian = find_median(listOfPoints)
    lookbackQueueInitialized = False
    firstLoop = True
    output = open('overflowlog.txt', 'w')

    for point in listOfPoints:
        # Initialize the queue as full
        if not lookbackQueueInitialized:
            if firstLoop:
                lookbackQueue.append(point)
                firstLoop = False

            else:
                lookbackQueue.append(point)
                if lookbackQueue[-1].startTime - lookbackQueue[0].startTime < globalVariables.LOOKBACK_SIZE_MS:
                    continue
                else:
                    lookbackQueueInitialized = True

        # todo ponder the questionable nature of possibly losing a point
        # maybe check for clusters during initalization
        else:
            while lookbackQueue[-1].startTime - lookbackQueue[0].startTime > globalVariables.LOOKBACK_SIZE_MS:
                lookbackQueue.pop(0)
            if check_if_cluster_too_big(lookbackQueue, totalMedian):
                # todo ouput to log file
                for each in lookbackQueue:
                    output.write(str(each.startTime) + '\n')
                output.write('\n')
                if find_distance(lookbackQueue[-1], lookbackQueue[-2]) >= totalMedian:
                    # clear the queue except for the newest point
                    for i in range(0, len(lookbackQueue)-1):
                        lookbackQueue.pop(i)
                else:
                    lookbackQueue = []
                    lookbackQueueInitialized = False

            elif check_for_cluster(lookbackQueue, totalMedian):
                cluster = extract_cluster(lookbackQueue, totalMedian)
                if cluster is not None:
                    listOfClusters.append(cluster)

                for i in range(0, NUMBER_OF_ELEMENTS_TO_REMOVE):
                    if i < len(lookbackQueue):
                        lookbackQueue.pop(i)
                # lookbackQueue = [] #todo correct this to only remove the cluster points
                lookbackQueueInitialized = False

            # else there is a cluster in progress. Do nothing. Move along. These aren't the droids you're looking for

    return listOfClusters



    # this is pseudocode
    #
    # find the    median distance between all points
    # for point in listOfPoints
    # {
    #   push points to lookback queue
    #   keep queue appropriate size
    #   if not clusteroverflow
    #     {
    #     if there is a cluster(group of temporally neighboring points with distance < median) in the queue
    #         {
    #             extract the cluster and clear any older points
    #             append cluster to list of clusters
    #             clear cluster
    #         }
    #     else if the cluster was too big
    #         {
    #         set clusteroverflow flag
    #         }
    #   else if clusteroverflow flag is set
    #     {
    #         if distance between newest and 2nd newest points >= median
    #             clear queue except for newest point
    #             unset clusteroverflow flag
    #     }
    # }


# refactor using find_distance()
def find_median(listOfPoints):
    pointDistances = []

    for i in range(1, len(listOfPoints)):
        point1x = int(listOfPoints[i].x)
        point1y = int(listOfPoints[i].y)
        point2x = int(listOfPoints[i-1].x)
        point2y = int(listOfPoints[i-1].y)

        distance = math.sqrt(math.pow(point2x-point1x, 2) +
                             math.pow(point2y-point1y, 2))

        pointDistances.append(distance)
    minimum = min(pointDistances)
    maximum = max(pointDistances)

    if globalVariables.MEDIAN_OFFSET > 0:
        return numpy.median(numpy.array(pointDistances)) + (globalVariables.MEDIAN_OFFSET * (maximum - numpy.median(numpy.array(pointDistances))))
    elif globalVariables.MEDIAN_OFFSET < 0:
        return numpy.median(numpy.array(pointDistances)) - (globalVariables.MEDIAN_OFFSET * (numpy.median(numpy.array(pointDistances)) - minimum))
    else:
        return numpy.median(numpy.array(pointDistances))


def find_distance(point1, point2):
    return math.sqrt(math.pow(int(point2.x - point1.x), 2) +
                     math.pow(int(point2.y - point1.y), 2))


# take queue and median distance as parameter and return boolean of whether or not there is a cluster in the queue
# only return true if there is an extractable cluster
def check_for_cluster(lookbackQueue, totalMedian):
    clusterSize = 0
    for i in range(1, len(lookbackQueue)):
        if i == len(lookbackQueue):
            if find_distance(lookbackQueue[i], lookbackQueue[i-1]) < totalMedian:
                return False
        if find_distance(lookbackQueue[i], lookbackQueue[i-1]) < totalMedian:
            clusterSize += 1
        else:
            if clusterSize >= globalVariables.MINIMUM_CLUSTER_SIZE:
                return True
            else:
                clusterSize = 0

    return False


# take queue as input return cluster from inside the queue
def extract_cluster(lookbackQueue, totalMedian): # todo reread this
    global NUMBER_OF_ELEMENTS_TO_REMOVE
    NUMBER_OF_ELEMENTS_TO_REMOVE = 0
    cluster = []
    firstLoop = True
    for i in range(1, len(lookbackQueue)):
        if lookbackQueue[i].startTime - lookbackQueue[i-1].startTime < totalMedian:
            if firstLoop:
                cluster.append(lookbackQueue[i-1])
                cluster.append(lookbackQueue[i])
                firstLoop = False
            else:
                cluster.append(lookbackQueue[i])

    if len(cluster) >= globalVariables.MINIMUM_CLUSTER_SIZE:
        NUMBER_OF_ELEMENTS_TO_REMOVE = len(cluster)
        return cluster
    return


# if all the points are less than median distance apart return, if so return true
def check_if_cluster_too_big(lookbackQueue, totalMedian):
    tooBig = True
    for i in range(1, len(lookbackQueue)):
        if lookbackQueue[i].startTime - lookbackQueue[i-1].startTime >= totalMedian:
            tooBig = False
    if tooBig:
        print("too big")
    return tooBig

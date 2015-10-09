import numpy
import matplotlib
import matplotlib.pyplot as plt
import pylab
from matplotlib.patches import Rectangle
import globalVariables


def plot_points(listofpoints, filename, listofaois):
    for point in listofpoints:
        plt.plot(point.x, -point.y, 'bo', label=filename)
    plt.savefig('point-plots/'+filename+'.png')


def plot_aois(listofaois, filename, list_of_clusters):
    numerOfAois = 0
    print globalVariables.AOI_FILES[filename]
    for aoi in listofaois:
        for cluster in list_of_clusters:
            for point in cluster:
                plt.plot(point.x, -point.y, 'bo')
        rectangle = Rectangle((aoi.x, -aoi.y), aoi.width, aoi.height, fc='r')
        numerOfAois += 1
        plt.gca().add_patch(rectangle)
    print(str(numerOfAois) + ' aois')

    period = filename.rfind('.')
    filename = filename[:-(len(filename)-period)]

    print(str(len(list_of_clusters)) + ' clusters')
    if len(list_of_clusters) > 0:
        plt.savefig('aoi-plots/' + filename)
    plt.clf()
    plt.close('all')
    #----------------------------------------------------------------------------------
    numerOfAois = 0
    autocorrected = False
    for cluster in list_of_clusters:
        for point in cluster:
            if point.x != point.autoxCorrected or point.y != point.autoyCorrected:
                autocorrected = True
    if autocorrected:
        for aoi in listofaois:
            for cluster in list_of_clusters:
                for point in cluster:
                    plt.plot(point.autoxCorrected, -point.autoyCorrected, 'ro')
            rectangle = Rectangle((aoi.x, -aoi.y), aoi.width, aoi.height, fc='g')
            numerOfAois += 1
            plt.gca().add_patch(rectangle)
        print(str(numerOfAois) + ' aois')

        print(str(len(list_of_clusters)) + ' clusters')
        if len(list_of_clusters) > 0:
            plt.savefig('aoi-plots/' + filename+"_autocorrected")
        plt.clf()
        plt.close('all')
    return len(list_of_clusters)
    # plt.show()

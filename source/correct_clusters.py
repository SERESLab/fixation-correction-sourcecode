
def correct_cluster(listofclusters, listofaois):
    for cluster in listofclusters:
        for point in cluster:
            point.autoxCorrected = point.x
            point.autoyCorrected = point.y
        if find_score_multi_aoi(cluster, listofaois) == 0:
            #print("toward a northern light")
            move_cluster_toward_aoi(cluster, listofaois)

        print("hillclimber")
        hillclimb(cluster, listofaois)


def find_score_multi_aoi(cluster, listofaois):
    list_of_points_in_aoi = []
    debug_points = []
    for point in cluster:
        if debug_points.count(point) > 0:
            print "point repeat error"
        debug_points.append(point)
        #print "outer loop"
        for aoi in listofaois:
            if point_in_aoi(point, aoi):
                if list_of_points_in_aoi.count(point) == 0:
                    list_of_points_in_aoi.append(point)
    #print(str(len(list_of_points_in_aoi))+'/'+str(len(cluster)))
    return float(len(list_of_points_in_aoi))/float(len(cluster))


def point_in_aoi(point, aoi):
    if point.autoxCorrected >= aoi.x and point.autoxCorrected <= (aoi.x + aoi.width):
        if point.autoyCorrected >= aoi.y and point.autoyCorrected <= (aoi.y + aoi.height):
            return True
        else:
            return False
    return False
# def find_score_single_aoi(cluster, aoi):


def hillclimb(cluster, listofaois):
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
    #print("current " + str(current))
    #print("left " + str(left))
    #print("right " + str(right))
    #print("up " + str(up))
    #print("down " + str(down))
    while movevertdistance >= 1 or movehordistance >= 1:
        #print("vert dist " + str(movevertdistance))
        #print("hor dist " + str(movehordistance))
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

# def hillclimb_single(cluster, aoi):

# def find_cluster_area(cluster):


def move_cluster_toward_aoi(cluster, listofaois):
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
    maxX = 0
    for point in cluster:
        if point.autoxCorrected > maxX:
            maxX = point.autoxCorrected
    return maxX


def get_maxY(cluster):
    maxY = 0
    for point in cluster:
        if point.autoyCorrected > maxY:
            maxY = point.autoyCorrected
    return maxY

def get_minX(cluster):
    minX = cluster[0].x
    for point in cluster:
        if point.autoxCorrected < minX:
            minX = point.autoxCorrected
    return minX


def get_minY(cluster):
    minY = cluster[0].y
    for point in cluster:
        if point.autoyCorrected < minY:
            minY = point.autoyCorrected
    return minY


def find_nearest_aoi(cluster, listofaois):
    maxX = get_maxX(cluster)
    maxY = get_maxY(cluster)
    minX = get_minX(cluster)
    minY = get_minY(cluster)
    nearestaoi = listofaois[0]
    for i in range(1, len(listofaois)):
        if abs(listofaois[i].x - minX) < abs(nearestaoi.x - minX) and abs(listofaois[i].y - minY) < abs(nearestaoi.y - minY):
            nearestaoi = listofaois[i]

    return nearestaoi
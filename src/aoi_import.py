import csv
import objects
import globalVariables

def get_aoi(filename):
    aoi_list = []
    aoi_filename = get_aoi_filename(filename)
    globalVariables.AOI_FILES[filename] = aoi_filename
    with open('aoi-data/aoi-csv/' + aoi_filename) as aoi_csv:
        reader = csv.DictReader(aoi_csv)
        for row in reader:
            aoi_list.append(objects.Aoi(str(row['kind']), str(row['name']), int(row['x']),
                                        int(row['y']),    int(row['width']), int(row['height'])))
        return aoi_list


def get_aoi_filename(filename):
    underscore = filename.rfind('_')
    filename = filename[:-(len(filename)-underscore)]
    filename += '_aoi.csv'
    return filename

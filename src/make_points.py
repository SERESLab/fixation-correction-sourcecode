import objects
import globalVariables
import csv


def make_points():
    dict_of_points = {}

    for filename in globalVariables.files:
        dict_of_points[filename] = create_list_of_points(filename)

    return dict_of_points


def create_list_of_points(filename):
    # variables
    point_list = []
    data_folder = "eye-tracking-data/"
    filename_path = data_folder+filename

    with open(filename_path) as data_csv_file:
        reader = csv.DictReader(data_csv_file)

        for row in reader:
            point_list.append(objects.Point(int(row['fix_x_original']),           int(row['fix_y_original']),           int(row['duration_ms']),
                                            int(row['start_ms']),        int(row['end_ms']),          str(row['aoi_sub.line']),
                                            int(row['fix_x']), int(row['fix_y']), filename))

    return point_list

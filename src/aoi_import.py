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

import csv
import objects
import globalVariables


def get_aoi(filename):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
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
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    underscore = filename.rfind('_')
    filename = filename[:-(len(filename)-underscore)]
    filename += '_aoi.csv'
    return filename

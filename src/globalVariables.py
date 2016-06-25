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

import os
import read_files

current_directory = os.path.dirname(os.path.realpath(__file__))+"/eye-tracking-data"
LOOKBACK_SIZE_MS = 15000
MINIMUM_CLUSTER_SIZE = 3
AOI_FILES = {}

# between -1 and 1
MEDIAN_OFFSET = .175
files = read_files.read(current_directory)

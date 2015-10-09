import os
import read_files

current_directory = os.path.dirname(os.path.realpath(__file__))+"/eye-tracking-data"
LOOKBACK_SIZE_MS = 15000
MINIMUM_CLUSTER_SIZE = 3
AOI_FILES = {}

# between -1 and 1
MEDIAN_OFFSET = .175
files = read_files.read(current_directory)

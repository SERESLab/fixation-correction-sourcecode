from os import walk
files = []
def read(directory_of_files):
    for (dirpath, dirnames, filenames) in walk(directory_of_files):
        files.extend(filenames)
        break
    for name in files:
        if ".csv" not in name:
            files.remove(name)
    return files
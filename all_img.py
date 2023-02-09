import glob
import os

def list_files(dir_path):
    for file in glob.glob(f"{dir_path}/*"):
        print(file)

# Call the function with the path of the directory you want to list
list_files('Default')
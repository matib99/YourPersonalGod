import os
import sys
import random
import shutil

path_to_data = "./data/god_dataset"
output_path = "./ars_electronica"
k = sys.argv[1]  # Number of gods for interpolation

if __name__ == "__main__":
    assert len(os.listdir(output_path)) == 0, "Output path should be empty"
    assert int(k) > 0, "Number of gods should be greater than zero."

    filenames = os.listdir(path_to_data)
    filenames.sort()
    gods = random.sample(filenames, int(k))
    for god in gods:
        shutil.copy(os.path.join(path_to_data, god), os.path.join(output_path, god))

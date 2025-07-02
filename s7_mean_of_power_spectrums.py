import numpy as np
from shutil import copy2
import os

def main() -> None:
    PATH_TO_PREPARED_DATA = ""
    SAMPLE_ID = "R798D"
    PATH_TO_PS_MEAN_DATA = ""

    os.makedirs(PATH_TO_PS_MEAN_DATA, exist_ok=True)

    NUM_OF_FILES = 5
    NUM_OF_ROWS = len(np.loadtxt(f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}001.dat"))
    print(NUM_OF_ROWS)

    mean_of_data = np.zeros(NUM_OF_ROWS)

    for counter in range(1, NUM_OF_FILES + 1, 1):
        path_to_prepared_data_file = f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}{counter:03d}.dat"
        
        data_read = np.loadtxt(path_to_prepared_data_file, dtype=np.float128)
        
        contributing_data = data_read / NUM_OF_FILES

        mean_of_data += contributing_data

        print(counter, contributing_data)

    np.savetxt(fname=f"{PATH_TO_PS_MEAN_DATA}{SAMPLE_ID}_mean.dat", X=mean_of_data, fmt='%.8e')

if __name__ == "__main__":
    main()
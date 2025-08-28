import numpy as np
import shutil
import os

def main() -> None:
    PATH_TO_PREPARED_DATA = "/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_0.2704s_0.2706s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs"
    SAMPLE_ID = "R798D"
    PATH_TO_MEAN_DATA = "/home/paulo/Scripts/barkhausen-noise-analysis/Mean_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"

    os.makedirs(PATH_TO_MEAN_DATA, exist_ok=True)

    NUM_OF_FILES = 212
    NUM_OF_ROWS = len(np.loadtxt(f"{PATH_TO_PREPARED_DATA}/{SAMPLE_ID}001.dat"))
    print(NUM_OF_ROWS)

    mean_of_data = np.zeros(NUM_OF_ROWS)

    for counter in range(1, NUM_OF_FILES + 1, 1):
        path_to_prepared_data_file = f"{PATH_TO_PREPARED_DATA}/{SAMPLE_ID}{counter:03d}.dat"
        
        data_read = np.loadtxt(path_to_prepared_data_file, dtype=np.float128)
        
        contributing_data = data_read / NUM_OF_FILES

        mean_of_data += contributing_data

        print(counter, contributing_data)

    np.savetxt(fname=f"{PATH_TO_MEAN_DATA}{SAMPLE_ID}_Prepared_Selected_mean.dat", X=mean_of_data, fmt='%.8e')
    shutil.copy2(f"{PATH_TO_PREPARED_DATA}/{SAMPLE_ID}_t.dat", f"{PATH_TO_MEAN_DATA}{SAMPLE_ID}_t.dat")

if __name__ == "__main__":
    main()
import numpy as np
import shutil

def main() -> None:
    PATH_TO_PREPARED_DATA = "/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
    SAMPLE_ID = "R798D"

    PATH_TO_MEAN_DATA = "/home/paulo/Scripts/barkhausen-noise-analysis/Mean_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"

    NUM_OF_FILES = 5
    NUM_OF_ROWS = len(np.loadtxt(f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}001.dat"))
    print(NUM_OF_ROWS)

    meanOfData = np.zeros(NUM_OF_ROWS)

    for counter in range(1, NUM_OF_FILES+1, 1):

        pathToPreparedDataFile = f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}{counter:03d}.dat"

        dataRead = np.loadtxt(pathToPreparedDataFile)

        getContributingData = dataRead / NUM_OF_FILES

        meanOfData += getContributingData

        print(counter, getContributingData)

    np.savetxt(fname=f"{PATH_TO_MEAN_DATA}{SAMPLE_ID}_mean.dat", X=meanOfData)
    shutil.copy2(f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}_t.dat", f"{PATH_TO_MEAN_DATA}{SAMPLE_ID}_t.dat" )

if __name__ == "__main__":
    main()
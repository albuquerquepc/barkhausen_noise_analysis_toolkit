import pandas as pd
import shutil

def main() -> None:
    #Selecting the orignal data files do be read
    PATH_TO_ORIGINAL_DATA = f"/home/paulo/Scripts/barkhausen-noise-analysis/Original_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
    SAMPLE_ID = "R798D"

    #Setting final destination to save the prepared files
    PATH_TO_PREPARED_DAT = "/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
    
    NUM_OF_FILES = 5

    NUM_OF_COIL_TURNS = 400
    GAIN = 50000
    SAMPLE_RATE = 4000000
    
    OFFSET_INTERVAL_IN_MILLISSECONDS = 50

    NUM_OF_POINTS_TO_CHECK_OFFSET = int(SAMPLE_RATE * (OFFSET_INTERVAL_IN_MILLISSECONDS/1000))

    for counter in range(1, NUM_OF_FILES+1, 1):

        originalFileName = f"{PATH_TO_ORIGINAL_DATA}{SAMPLE_ID}{counter:03}.dat"
        dataRead = pd.read_csv(originalFileName, header=None)

        rawOffset = dataRead.head(NUM_OF_POINTS_TO_CHECK_OFFSET)
        offsetMean = rawOffset.mean()


        preparedDataFileName = f"{PATH_TO_PREPARED_DAT}{SAMPLE_ID}{counter:03}.dat"

        preparedData = ((dataRead-offsetMean)/(GAIN*NUM_OF_COIL_TURNS))
        
        preparedData.to_csv(path_or_buf=preparedDataFileName, columns=preparedData, header=False, index=False)
    
    shutil.copy2(f"{PATH_TO_ORIGINAL_DATA}{SAMPLE_ID}_t.dat", f"{PATH_TO_PREPARED_DAT}{SAMPLE_ID}_t.dat" )
if __name__ == "__main__":
    main()
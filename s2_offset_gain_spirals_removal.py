import numpy as np
import shutil
import os 

def main() -> None:
    PATH_TO_ORIGINAL_DATA = f"/home/paulo/Scripts/barkhausen-noise-analysis/Original_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
    SAMPLE_ID = "R798D"

    PATH_TO_PREPARED_DATA = "/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
    
    os.makedirs(PATH_TO_PREPARED_DATA, exist_ok=True)
    
    NUM_OF_FILES = 5

    NUM_OF_COIL_TURNS = 400
    GAIN = 50000
    SAMPLE_RATE = 4000000
    
    OFFSET_INTERVAL_IN_MILLISSECONDS = 50

    NUM_OF_POINTS_TO_CHECK_OFFSET = int(SAMPLE_RATE * (OFFSET_INTERVAL_IN_MILLISSECONDS/1000))

    for counter in range(1, NUM_OF_FILES+1, 1):

        original_file_name = f"{PATH_TO_ORIGINAL_DATA}{SAMPLE_ID}{counter:03}.dat"
        data_read = np.loadtxt(original_file_name, dtype=np.float128)

        raw_offset = data_read[:NUM_OF_POINTS_TO_CHECK_OFFSET]
        offset_mean = raw_offset.mean()

        prepared_data_fileName = f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}{counter:03}.dat"

        prepared_data = (data_read - offset_mean) / (GAIN * NUM_OF_COIL_TURNS)
        

        np.savetxt(prepared_data_fileName, X=prepared_data, fmt='%.8e')
    
    shutil.copy2(f"{PATH_TO_ORIGINAL_DATA}{SAMPLE_ID}_t.dat", f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}_t.dat" )

if __name__ == "__main__":
    main()
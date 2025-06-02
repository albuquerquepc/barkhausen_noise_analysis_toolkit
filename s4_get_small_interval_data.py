import numpy as np
import os
from s0_constants_and_pathing import PATH_TO_PREPARED_DATA, SAMPLE_ID, SAMPLING_RATE, NUM_OF_FILES

def main() -> None:
    INTERVAL_START_IN_SECONDS = 0.2198
    INTERVAL_END_IN_SECONDS = 0.2200
    
    FIRST_POINT_OF_INTERVAL = int(INTERVAL_START_IN_SECONDS * SAMPLING_RATE)
    LAST_POINT_OF_INTERVAL = int(INTERVAL_END_IN_SECONDS * SAMPLING_RATE)
    
    os.makedirs(f"Prepared_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs", exist_ok=True)
    
    
    LOAD_TIMINGS = np.loadtxt(f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}_t.dat")
    new_timings = LOAD_TIMINGS[FIRST_POINT_OF_INTERVAL:LAST_POINT_OF_INTERVAL+1]
    new_timings -= INTERVAL_START_IN_SECONDS
    

    np.savetxt(fname=f"/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}_t.dat", X=new_timings)


    for counter in range(1, NUM_OF_FILES+1, 1):
        prepared_file_name = f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}{counter:03}.dat"
        data_read = np.loadtxt(prepared_file_name)
        
        slicing_data_inside_interval = data_read[FIRST_POINT_OF_INTERVAL:(LAST_POINT_OF_INTERVAL+1)]

        np.savetxt(fname=f"/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}{counter:03}.dat", X=slicing_data_inside_interval)


if __name__ == "__main__":
    main()
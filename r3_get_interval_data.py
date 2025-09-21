global INTERVAL_START_IN_SECONDS, INTERVAL_END_IN_SECONDS

import numpy as np
import os
from constants_and_pathing import MAIN_DATA_DIRECTORY, PATH_TO_PREPARED_DATA, SAMPLE_ID, SAMPLING_RATE, NUM_OF_FILES

INTERVAL_START_IN_SECONDS = 0.17
INTERVAL_END_IN_SECONDS = 0.22

def main():
  FIRST_POINT_OF_INTERVAL = int(INTERVAL_START_IN_SECONDS * SAMPLING_RATE)
  LAST_POINT_OF_INTERVAL = int(INTERVAL_END_IN_SECONDS * SAMPLING_RATE)
  
  os.makedirs(f"{MAIN_DATA_DIRECTORY}Prepared_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_{SAMPLE_ID}_0.05Hz_100kHz_4MSs", exist_ok=True)

  time = np.arange(0, (INTERVAL_END_IN_SECONDS-INTERVAL_START_IN_SECONDS), 1/SAMPLING_RATE, dtype=np.float128)

  np.savetxt(fname=f"/{MAIN_DATA_DIRECTORY}Prepared_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}_t.dat", X=time, fmt='%.8e')


  for counter in range(1, NUM_OF_FILES+1, 1):
      prepared_file_name = f"{PATH_TO_PREPARED_DATA}{SAMPLE_ID}{counter:03}.dat"
      data_read = np.loadtxt(prepared_file_name, dtype=np.float128)
      
      slicing_data_inside_interval = data_read[FIRST_POINT_OF_INTERVAL:(LAST_POINT_OF_INTERVAL+1)]

      np.savetxt(fname=f"{MAIN_DATA_DIRECTORY}Prepared_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}{counter:03}.dat", X=slicing_data_inside_interval, fmt='%.8e')

      print(f"{counter}/{NUM_OF_FILES}")


if __name__ == "__main__":
    main()
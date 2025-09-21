from constants_and_pathing import MAIN_DATA_DIRECTORY, PATH_TO_PREPARED_DATA,NUM_OF_FILES, SAMPLE_ID, SAMPLING_RATE
from s4_get_small_interval_data import INTERVAL_START_IN_SECONDS, INTERVAL_END_IN_SECONDS

import numpy as np
from math import log2, ceil
import os

def main():
  PATH_TO_PREPARED_SELECTED_DATA = f"{PATH_TO_PREPARED_DATA}"

  data_read = np.loadtxt(f"{PATH_TO_PREPARED_SELECTED_DATA}/{SAMPLE_ID}001.dat", dtype=np.float128)
  array_length = np.size(data_read)

  rounded_up_int = ceil(log2(array_length))
  empty_array_lenght = 2**rounded_up_int

  get_new_delta_padded_time_vector = empty_array_lenght / SAMPLING_RATE

  padded_time_for_fft = np.arange(0,  get_new_delta_padded_time_vector, 1/SAMPLING_RATE,dtype=np.float128)

  os.makedirs(f"{MAIN_DATA_DIRECTORY}Padded_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/", exist_ok=True)

  np.savetxt(fname=f"{MAIN_DATA_DIRECTORY}Padded_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}_t.dat", X=padded_time_for_fft, fmt='%.8e')

  for counter in range(84, NUM_OF_FILES+1, 1):
      data_array = np.zeros(empty_array_lenght, dtype=np.float128)
      prepared_file_name = f"{PATH_TO_PREPARED_SELECTED_DATA}/{SAMPLE_ID}{counter:03}.dat"

      data_read = np.loadtxt(prepared_file_name, dtype=np.float128)
      
      data_array[0:array_length] = data_read
      print(f"{counter}/{NUM_OF_FILES}: {data_array}")

      np.savetxt(fname=f"{MAIN_DATA_DIRECTORY}Padded_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}{counter:03}.dat", X=data_array, fmt='%.8e')

if __name__ == "__main__":
  main()
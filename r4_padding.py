import numpy as np
import os
from math import log2, ceil

from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample
from r3_get_interval_data import interval, directory_for_interval


def main() -> None:

  data_read = np.loadtxt(f"{directory_for_interval}/{sample.sample_id()}001.dat", dtype=np.float128)
  array_length = np.size(data_read)

  rounded_up_int = ceil(log2(array_length))
  empty_array_lenght = 2**rounded_up_int

  get_new_delta_padded_time_vector = empty_array_lenght / sample.sampling_rate()

  padded_time_for_fft = np.arange(0,  get_new_delta_padded_time_vector, 1/sample.sampling_rate(),dtype=np.float128)


  
  os.makedirs(directory_for_padded, exist_ok=True)


  np.savetxt(fname=f"{directory_for_padded}{sample.sample_id()}_t.dat", X=padded_time_for_fft, fmt='%.8e')

  for counter in range(1, 6+1, 1):

      data_array = np.zeros(empty_array_lenght, dtype=np.float128)
      prepared_file_name = f"{directory_for_interval}/{sample.sample_id()}{counter:03}.dat"

      data_read = np.loadtxt(prepared_file_name, dtype=np.float128)
      
      data_array[0:array_length] = data_read
      print(f"{counter}/{sample.num_of_files()}: {data_array}")

      


      np.savetxt(fname=f"{directory_for_padded}{sample.sample_id()}{counter:03}.dat", X=data_array, fmt='%.8e')

global directory_for_padded
directory_for_padded: str = f"{path.main()}Padded_{interval.start()}s_{interval.end()}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
print(directory_for_padded)

if __name__ == "__main__":
  main()
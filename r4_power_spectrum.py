import numpy as np
import os
from math import log2, ceil
import matplotlib.pyplot as plt

from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample
from r3_get_interval_data import interval, directory_for_interval


def main() -> None:

  path_for_1st_selected_file: str = f"{directory_for_interval}/{sample.sample_id()}001.dat"
  data_read_1st_selected_file: np.ndarray = np.loadtxt(path_for_1st_selected_file, dtype=np.float128)
  prepared_array_length: int = np.size(data_read_1st_selected_file)
  rounded_up_int: int = ceil(log2(prepared_array_length))
  padded_array_lenght: int = 2**rounded_up_int
  power_spectrum_mean: np.ndarray = np.zeros(int((padded_array_lenght/2)+1))
  print(padded_array_lenght)

  window = np.bartlett(padded_array_lenght)
  
  get_frequencies = np.fft.rfftfreq(padded_array_lenght, d=1/sample.sampling_rate())
  
  for counter in range(1, 5+1, 1):

    selected_file_name = f"{directory_for_interval}{sample.sample_id()}{counter:03}.dat"
    prepared_data_read = np.loadtxt(selected_file_name, dtype=np.float128)
    padded_array: np.ndarray = np.zeros(int(padded_array_lenght))
    padded_array[0:prepared_array_length] = prepared_data_read

    signal_through_window: np.ndarray = padded_array * window
    
    signal_transform: np.ndarray = np.fft.rfft(signal_through_window)

    signal_abs: np.ndarray = np.abs(signal_transform)

    signal_abs_squared: np.ndarray = np.square(signal_abs)

    power_spectrum: np.ndarray = signal_abs_squared/((rounded_up_int)**2)

    power_spectrum_mean += (power_spectrum / sample.num_of_files())


    print(f"{counter}/{sample.num_of_files()}: {power_spectrum_mean}")

  np.savetxt(fname=f"{directory_for_powerspectrum}Power_Spectrum_{interval.start()}s_{interval.end()}s.dat", X=power_spectrum_mean, fmt='%.8e')
  np.savetxt(fname=f"{directory_for_powerspectrum}Frequencies_{interval.start()}s_{interval.end()}s.dat", X=get_frequencies, fmt='%.8e')

  plt.loglog(get_frequencies, power_spectrum_mean, linestyle="none", marker='o', ms=1, color="black")
  plt.show()

global directory_for_powerspectrum
directory_for_powerspectrum: str = f"{path.main()}Power_Spectrum_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
os.makedirs(directory_for_powerspectrum, exist_ok=True)

if __name__ == "__main__":
  main()
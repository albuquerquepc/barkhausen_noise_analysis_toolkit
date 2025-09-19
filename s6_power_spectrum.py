from constants_and_pathing import MAIN_DATA_DIRECTORY, PATH_TO_MEAN_DATA, NUM_OF_FILES, SAMPLE_ID, SAMPLING_RATE
from s4_get_small_interval_data import INTERVAL_START_IN_SECONDS, INTERVAL_END_IN_SECONDS

import numpy as np
import os
import matplotlib.pyplot as plt


def main():
  PATH_TO_PADDED_DATA = f"/home/paulo/Documents/ic_gmag/scripts/barkhausen_noises_analysis_tools_library/Padded_Py_1000nm_R798D_0.05Hz_100kHz_4MSs"
  
  os.makedirs(f"{MAIN_DATA_DIRECTORY}Power_Spectrum_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/", exist_ok=True)

  prepared_fft_1st_file_name = f"{PATH_TO_PADDED_DATA}/{SAMPLE_ID}001.dat"
  len_of_1st_file = len(np.loadtxt(prepared_fft_1st_file_name))
  
  window = np.bartlett(len_of_1st_file)

  #get_frequencies1 = np.fft.fftfreq(len_of_1st_file, 1/SAMPLING_RATE)
  #get_frequencies2 = np.arange(0, (SAMPLING_RATE/2)+1/SAMPLING_RATE, (SAMPLING_RATE/2)/(len_of_1st_file/2))

  frequencies_spectrum_length = int(len_of_1st_file/2+1)
  get_frequencies = np.linspace(0, int(SAMPLING_RATE/2), frequencies_spectrum_length)


  power_spectrum_mean = np.zeros(len_of_1st_file)

  np.savetxt(fname=f"{PATH_TO_MEAN_DATA}{SAMPLE_ID}_Frequencies.dat", X=get_frequencies, fmt='%.8e')

  for counter in range(1, NUM_OF_FILES+1, 1):
    prepared_fft_file_name = f"{PATH_TO_PADDED_DATA}/{SAMPLE_ID}{counter:03}.dat"
    data_read = np.loadtxt(prepared_fft_file_name, dtype=np.float128)

    signal_through_window = data_read * window

    signal_fft = np.fft.fft(signal_through_window)

    power_spectrum = signal_fft * np.conj(signal_fft)
    power_spectrum_real = power_spectrum.real / (len_of_1st_file**2)
    power_spectrum_mean += (power_spectrum_real / NUM_OF_FILES)

    print(f"{counter}/{NUM_OF_FILES}: {power_spectrum_mean}")

  np.savetxt(fname=f"{PATH_TO_MEAN_DATA}{SAMPLE_ID}_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Power_Spectrum.dat", X=power_spectrum_mean[0:frequencies_spectrum_length], fmt='%.8e')

  plt.loglog(get_frequencies, power_spectrum_mean[0:frequencies_spectrum_length])
  plt.show()

if __name__ == "__main__":
  main()
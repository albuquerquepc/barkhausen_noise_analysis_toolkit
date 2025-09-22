import numpy as np
import os
import matplotlib.pyplot as plt

from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample
from r3_get_interval_data import interval
from r4_padding import directory_for_padded



def main() -> None:

  os.makedirs(directory_for_powerspectrum, exist_ok=True)

  prepared_fft_1st_file_name = f"{directory_for_padded}/{sample.sample_id()}001.dat"
  len_of_1st_file = len(np.loadtxt(prepared_fft_1st_file_name))
  
  window = np.bartlett(len_of_1st_file)

  #get_frequencies1 = np.fft.fftfreq(len_of_1st_file, 1/sample.sampling_rate)
  #get_frequencies2 = np.arange(0, (sample.sampling_rate/2)+1/sample.sampling_rate, (Ssample.sampling_rate/2)/(len_of_1st_file/2))

  frequencies_spectrum_length = int(len_of_1st_file/2+1)
  get_frequencies = np.linspace(0, int(sample.sampling_rate()/2), frequencies_spectrum_length)

  #get_frequencies = np.fft.rfftfreq(len_of_1st_file/2, d=1/sample.sampling_rate())

  power_spectrum_mean = np.zeros(len_of_1st_file)

  for counter in range(1, sample.num_of_files()+1, 1):
    prepared_fft_file_name = f"{directory_for_padded}{sample.sample_id()}{counter:03}.dat"
    data_read = np.loadtxt(prepared_fft_file_name, dtype=np.float128)

    signal_through_window = data_read * window

    signal_fft = np.fft.fft(signal_through_window)
    power_spectrum = signal_fft * np.conj(signal_fft)

    #as linha acima isso podem ser substituidas pela linha

    #power_spectrum = np.fft.rfft(signal_through_window)
    

    power_spectrum_real = power_spectrum.real / (len_of_1st_file**2)
    power_spectrum_mean += (power_spectrum_real / sample.num_of_files())

    print(f"{counter}/{sample.num_of_files()}: {power_spectrum_mean}")

  np.savetxt(fname=f"{directory_for_powerspectrum}Power_Spectrum.dat", X=power_spectrum_mean[0:frequencies_spectrum_length], fmt='%.8e')
  np.savetxt(fname=f"{directory_for_powerspectrum}Frequencies.dat", X=get_frequencies[0:frequencies_spectrum_length], fmt='%.8e')

  plt.loglog(get_frequencies, power_spectrum_mean[0:frequencies_spectrum_length], linestyle="none", marker='o', ms=1, color="black")
  plt.show()

global directory_for_powerspectrum
directory_for_powerspectrum: str = f"{path.main()}Power_Spectrum_{interval.start()}s_{interval.end()}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"

if __name__ == "__main__":
  main()
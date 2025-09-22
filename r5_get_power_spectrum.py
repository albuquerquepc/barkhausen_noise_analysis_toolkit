import numpy as np
import os
import matplotlib.pyplot as plt

from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample
from r3_get_interval_data import interval
from r4_padding import directory_for_padded



def main() -> None:

  os.makedirs(directory_for_powerspectrum, exist_ok=True)

  prepared_fft_1st_file_name = f"/home/paulo/Documentos/ic_gmag/medidas/Py(1000nm)/Barkhausen/Padded_0.17s_0.22s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/R798D001.dat"
  len_of_1st_file = len(np.loadtxt(prepared_fft_1st_file_name))
  
  window = np.bartlett(len_of_1st_file)

  get_frequencies = np.fft.rfftfreq(len_of_1st_file, d=1/sample.sampling_rate())

  power_spectrum_mean: np.ndarray = np.zeros(int((len_of_1st_file/2)+1))

  for counter in range(1, 5+1, 1):
    prepared_fft_file_name = f"{directory_for_padded}{sample.sample_id()}{counter:03}.dat"
    data_read = np.loadtxt(prepared_fft_file_name, dtype=np.float128)

    signal_through_window: np.ndarray = data_read * window
    
    signal_transform: np.ndarray = np.fft.rfft(signal_through_window)

    signal_abs: np.ndarray = np.abs(signal_transform)

    signal_abs_squared: np.ndarray = np.square(signal_abs)

    power_spectrum: np.ndarray = signal_abs_squared/((len_of_1st_file)**2)

    power_spectrum_mean += (power_spectrum / sample.num_of_files())

    print(f"{counter}/{sample.num_of_files()}: {power_spectrum_mean}")

  np.savetxt(fname=f"{directory_for_powerspectrum}Power_Spectrum.dat", X=power_spectrum_mean, fmt='%.8e')
  np.savetxt(fname=f"{directory_for_powerspectrum}Frequencies.dat", X=get_frequencies, fmt='%.8e')

  plt.loglog(get_frequencies, power_spectrum_mean, linestyle="none", marker='o', ms=1, color="black")
  plt.show()

global directory_for_powerspectrum
directory_for_powerspectrum: str = f"{path.main()}Power_Spectrum_{interval.start()}s_{interval.end()}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"

if __name__ == "__main__":
  main()
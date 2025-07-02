from s0_constants_and_pathing import NUM_OF_FILES, SAMPLE_ID, SAMPLING_RATE
from s4_get_small_interval_data import INTERVAL_START_IN_SECONDS, INTERVAL_END_IN_SECONDS
import numpy as np
import os


def main() -> None:
    PATH_TO_PREPARED_FFT_DATA = f"/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_FFT_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs"
    
    os.makedirs(f"/home/paulo/Scripts/barkhausen-noise-analysis/Power_Spectrum_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/", exist_ok=True)

    prepared_fft_1st_file_name = f"{PATH_TO_PREPARED_FFT_DATA}/{SAMPLE_ID}001.dat"
    len_of_1st_file = len(np.loadtxt(prepared_fft_1st_file_name))
    
    window = np.bartlett(len_of_1st_file)

    get_frequencies = np.fft.fftfreq(len_of_1st_file, 1/SAMPLING_RATE)

    np.savetxt(fname=f"/home/paulo/Scripts/barkhausen-noise-analysis/Power_Spectrum_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}_f.dat", X=get_frequencies, fmt='%.8e')

    for counter in range(1, NUM_OF_FILES+1, 1):
        prepared_fft_file_name = f"{PATH_TO_PREPARED_FFT_DATA}/{SAMPLE_ID}{counter:03}.dat"
        data_read = np.loadtxt(prepared_fft_file_name, dtype=np.float128)

        signal_through_window = data_read * window

        signal_fft = np.fft.fft(signal_through_window)

        power_spectrum = signal_fft * np.conj(signal_fft)

        get_frequencies = np.fft.fftfreq(len_of_1st_file, 1/SAMPLING_RATE)

        np.savetxt(fname=f"/home/paulo/Scripts/barkhausen-noise-analysis/Power_Spectrum_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}{counter:03}.dat", X=power_spectrum, fmt='%.8e')

        
if __name__ == "__main__":
        main()
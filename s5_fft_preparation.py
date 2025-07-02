from s0_constants_and_pathing import NUM_OF_FILES, SAMPLE_ID, SAMPLING_RATE
from s4_get_small_interval_data import INTERVAL_START_IN_SECONDS, INTERVAL_END_IN_SECONDS
import numpy as np
from math import log2, ceil
import os

def main() -> None:
    PATH_TO_PREPARED_SELECTED_DATA = f"//home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs"

    os.makedirs(PATH_TO_PREPARED_SELECTED_DATA, exist_ok=True)

    data_read = np.loadtxt(f"{PATH_TO_PREPARED_SELECTED_DATA}/{SAMPLE_ID}001.dat", dtype=np.float128)
    array_length = np.size(data_read)

    rounded_up_int = ceil(log2(array_length))
    empty_array_lenght = 2**rounded_up_int

    get_new_delta_padded_time_vector = empty_array_lenght / SAMPLING_RATE

    padded_time_for_fft = np.arange(0,  get_new_delta_padded_time_vector, 1/SAMPLING_RATE,dtype=np.float128)

    os.makedirs(f"/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_FFT_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/", exist_ok=True)

    np.savetxt(fname=f"/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_FFT_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}_t.dat", X=padded_time_for_fft, fmt='%.8e')



    for counter in range(1, NUM_OF_FILES+1, 1):
        data_array = np.zeros(empty_array_lenght, dtype=np.float128)
        prepared_file_name = f"{PATH_TO_PREPARED_SELECTED_DATA}/{SAMPLE_ID}{counter:03}.dat"

        data_read = np.loadtxt(prepared_file_name, dtype=np.float128)
        
        data_array[0:array_length] = data_read

        np.savetxt(fname=f"/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_FFT_{INTERVAL_START_IN_SECONDS}s_{INTERVAL_END_IN_SECONDS}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/{SAMPLE_ID}{counter:03}.dat", X=data_array, fmt='%.8e')

if __name__ == "__main__":
    main()
import numpy as np
import os
import matplotlib.pyplot as plt


from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample

class Threshold:
  def __init__(self, voltage_input: float) -> None:
    self.voltage_assign = voltage_input

  def get(self) -> float:
    return self.voltage_assign

clip: Threshold = Threshold(1e-6)

time_readout = np.loadtxt(f"{path.prepared()}{sample.sample_id()}_t.dat")

def main() -> None:
    prepared_file_name: str = f"{path.prepared()}{sample.sample_id()}{1:03}.dat"
    print(prepared_file_name)
    data_read: np.ndarray = np.loadtxt(prepared_file_name)
    
    data_read[data_read < clip.get()] = 0

    shift_down_value: float = np.min(data_read[(data_read > 0)])
    print(np.min(data_read[data_read > 0]))
    data_read[data_read != 0] += -(shift_down_value)
    print(np.min(data_read[data_read > 0]))

    plt.plot(time_readout, data_read, linestyle="none", marker='o', ms=1, color="black")
    plt.xlim(0.223, 0.224)
    plt.show()
    
if __name__ == "__main__":
  main()
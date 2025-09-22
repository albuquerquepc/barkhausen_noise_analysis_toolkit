import numpy as np
import os
from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample

class IntervalInSeconds:
  def __init__(self, instant1: float, instant2: float) -> None:
    self.start_assign: float = instant1
    self.end_assign: float = instant2

  def start(self) -> float:
    return self.start_assign

  def end(self) -> float:
    return self.end_assign

class IntervalToPoints:
  def __init__(self, start_input: float, end_input: float) -> None:
    self.start_point: int = int(start_input * sample.sampling_rate())
    self.end_point: int = int(end_input * sample.sampling_rate())

  def start(self) -> int:
    return self.start_point
  
  def end(self) -> int:
    return self.end_point


def main() -> None:  
  
  os.makedirs(directory_for_interval, exist_ok=True)

  time = np.arange(0, (interval.end()-interval.start()), 1/sample.sampling_rate(), dtype=np.float128)

  np.savetxt(f"d{irectory_for_interval}/{sample.sample_id()}_t.dat", X=time, fmt='%.8e')


  for counter in range(1, sample.num_of_files()+1, 1):
    prepared_file_name: str = f"{path.prepared()}{sample.sample_id()}{counter:03}.dat"
    data_read: np.ndarray = np.loadtxt(prepared_file_name, dtype=np.float128)
    
    slicing_data_inside_interval: np.ndarray = data_read[points.start():(points.end()+1)]

    file_name: str = f"{directory_for_interval}{sample.sample_id()}{counter:03}.dat"
    np.savetxt(fname=f"{file_name}", X=slicing_data_inside_interval, fmt='%.8e')

    print(f"{counter:03}/{sample.num_of_files()}: Intervalo de {interval.start()} a {interval.end()} salvo em {file_name}")

interval: IntervalInSeconds = IntervalInSeconds(0.17, 0.22)
points: IntervalToPoints = IntervalToPoints(interval.start(), interval.end())
global directory_for_interval
directory_for_interval: str = f"{path.main()}Prepared_Selected_{interval.start()}s_{interval.end()}s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"

if __name__ == "__main__":
    main()
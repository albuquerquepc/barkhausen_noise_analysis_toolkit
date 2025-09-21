import numpy as np
import shutil
import os
from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample

def main() -> None:

  os.makedirs(path.mean(), exist_ok=True)

  NUM_OF_ROWS: int = len(np.loadtxt(f"{path.prepared()}/{sample.sample_id()}001.dat"))
  print(NUM_OF_ROWS)

  mean_of_data = np.zeros(NUM_OF_ROWS)

  for counter in range(1, sample.num_of_files() + 1, 1):
      path_to_prepared_data_file: str= f"{path.prepared()}/{sample.sample_id()}{counter:03d}.dat"
      
      data_read: np.ndarray = np.loadtxt(path_to_prepared_data_file, dtype=np.float128)
      
      contributing_data: ndarray = data_read / sample.num_of_files()

      mean_of_data += contributing_data

      print(counter, contributing_data)

  np.savetxt(fname=f"{path.mean()}{sample.sample_id()}_Prepared_Selected_mean.dat", X=mean_of_data, fmt='%.8e')
  shutil.copy2(f"{path.prepared()}/{sample.sample_id()}_t.dat", f"{path.mean()}{sample.sample_id()}_t.dat")

if __name__ == "__main__":
  main()
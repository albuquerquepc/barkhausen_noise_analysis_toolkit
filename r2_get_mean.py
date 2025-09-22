import numpy as np
import os
import shutil

from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample

def add_contributing_data(data_mean: np.ndarray,data_input: np.ndarray, sample_size_input: int) -> np.ndarray:
  contributing_data: np.ndarray = data_input / sample_size_input
  data_mean += contributing_data
  return data_mean

def main() -> None:

  os.makedirs(path.mean(), exist_ok=True)
  FIRST_FILE_PATH: str = f"{path.prepared()}/{sample.sample_id()}001.dat"
  FIRST_FILE_READ: np.ndarray = np.loadtxt(FIRST_FILE_PATH)
  NUM_OF_ROWS: int = len(FIRST_FILE)

  mean_of_data: np.ndarray = np.zeros(NUM_OF_ROWS)

  for counter in range(1, sample.num_of_files() + 1, 1):
    path_to_prepared_data_file: str= f"{path.prepared()}/{sample.sample_id()}{counter:03d}.dat"
    data_read: np.ndarray = np.loadtxt(path_to_prepared_data_file, dtype=np.float128)
    mean_of_data = add_contributing_data(mean_of_data, data_read, sample.num_of_files() + 1)

    print(f"{counter:03}/{sample.num_of_files()}: Adicionado.")


  np.savetxt(fname=f"{path.mean()}{sample.sample_id()}_Prepared_Selected_mean.dat", X=mean_of_data, fmt='%.8e')
  shutil.copy2(f"{path.prepared()}/{sample.sample_id()}_t.dat", f"{path.mean()}{sample.sample_id()}_t.dat")
  print(f"Array da média salvo em: {path.mean()}{sample.sample_id()}_Prepared_Selected_mean.dat")
  print(f"Arquivo de tempo copiado para: {path.mean()}{sample.sample_id()}_t.dat")

if __name__ == "__main__":
  main()
import numpy as np
import os
import shutil
from modules.paths import r798d_data_path as path
from modules.sample_info import r798d_info as sample

def main() -> None:
   
  os.makedirs(path.prepared(), exist_ok=True)
  
  OFFSET_INTERVAL_IN_MILLISSECONDS = 50

  NUM_OF_POINTS_TO_CHECK_OFFSET = int(sample.sampling_rate() * (OFFSET_INTERVAL_IN_MILLISSECONDS/1e3))

  for counter in range(1, sample.num_of_files()+1, 1):

    original_file_name = f"{path.original()}{sample.sample_id()}{counter:03}.dat"
    data_read = np.loadtxt(original_file_name, dtype=np.float128)

    raw_offset = data_read[:NUM_OF_POINTS_TO_CHECK_OFFSET]
    offset_mean = raw_offset.mean()

    prepared_data_file_name = f"{path.prepared()}{sample.sample_id()}{counter:03}.dat"

    prepared_data = (data_read - offset_mean) / (sample.gain() * sample.sensing_coil_turns())

    np.savetxt(prepared_data_file_name, X=prepared_data, fmt='%.8e')
    print(f"{counter:03}/{sample.num_of_files():03}: salvo em {prepared_data_file_name}")
  
  print(f"Dados preparados salvos no diretório: {path.prepared()}")
  shutil.copy2(f"{path.original()}{sample.sample_id()}_t.dat", f"{path.prepared()}{sample.sample_id()}_t.dat" )
  print(f"Arquivo de tempo copiado para: {path.prepared()}_t.dat")

if __name__ == "__main__":
  main()
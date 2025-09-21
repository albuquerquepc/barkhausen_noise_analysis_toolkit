class Paths:
  """
  Used for easier managment of data and it's location(s). Using the paths module, it's possible to easily work with multiple samples.

  :param str path_input: Path to main directory, one steo above where the original data resides.
  :param str original_input_suffix: Path to original data, with raw .dat files.
  :param str prepared_input_suffix: Path to preapared data, with .dat files containing the real voltage after treatament.
  :parram str mean_input_suffix: General directory where mean of datasets resides.
  """
  def __init__(self, path_input: str, original_input_suffix, prepared_input_suffix, mean_input_suffix) -> None:
    self.main_path_assign: str = path_input
    self.original_path_assign_suffix: str = self.main_path_assign + original_input_suffix
    self.prepared_path_assign_suffix: str= self.main_path_assign + prepared_input_suffix
    self.mean_path_assign_suffix: str = self.main_path_assign + mean_input_suffix


  def main(self) -> str:
    return self.main_path_assign

  def original(self) -> str:
    return self.original_path_assign

  def prepared(self) -> str:
    return self.prepared_path_assign
  
  def mean(self) -> str:
    return self.mean_path_assign

r798d_data_path: Paths = Paths("/home/paulo/Documentos/ic_gmag/medidas/Py(1000nm)/Barkhausen/", "Original_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/", "Prepared_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/", "Means_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/")

if __name__ == "__main__":
  print(r798d_data_path.main())

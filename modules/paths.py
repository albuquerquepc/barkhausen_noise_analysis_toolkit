class Paths:
  def __init__(self, path_input: str) -> None:
    self.main_path_assign = path_input
    self.original_path_assign = f"{self.main_path_assign}Original_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
    self.prepared_path_assign = f"{self.main_path_assign}Prepared_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"
    self.mean_path_assign = f"{self.main_path_assign}Means_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/"


  def main(self) -> str:
    return self.main_path_assign

  def original(self) -> str:
    return self.original_path_assign

  def prepared(self) -> str:
    return self.prepared_path_assign
  
  def mean(self) -> str:
    return self.mean_path_assign

r798d_data_path: Paths = Paths("/home/paulo/Documentos/ic_gmag/medidas/Py(1000nm)/Barkhausen/")

if __name__ == "__main__":
  print(r798d_data_path.main())

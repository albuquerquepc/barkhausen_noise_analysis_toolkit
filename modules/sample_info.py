class Sample:
  """
  Template to fill in the sample information.
  :param str sample_id_input: Documented unique sample id.
  :param str description_input: Desciption of the sample general structure (composition, thickness, etc.)
  :param int num_of_files_input: int: Number of data files to be work with for this sample
  :param int sampling_rate_input = int: Rate in which the data points for each data file where collected for this sample.
  """
  def __init__(self, sample_id_input: str, description_input: str, num_of_files_input: int, sampling_rate_input: int, sensing_coil_turns_input: int, gain_input: int) -> None:
    self.sample_id_assign: str = sample_id_input
    self.description_assign: str = description_input
    self.num_of_files_assign: int = num_of_files_input
    self.sampling_rate_assign: int = sampling_rate_input
    self.sensing_coil_turns_assign: int = sensing_coil_turns_input
    self.gain_assign: int = gain_input

  def sample_id(self) -> str:
    return self.sample_id_assign

  def description(self) -> str:
    return self.description_assign


  def num_of_files(self) -> int:
    return self.num_of_files_assign

  def sampling_rate(self) -> int:
    return self.sampling_rate_assign

  def sensing_coil_turns(self) -> int:
    return self.sensing_coil_turns_assign

  def gain(self) -> int:
    return self.gain_assign


r798d_info: Sample = Sample(sample_id_input="R798D", description_input=f"Py(1000nm)", num_of_files_input=212, sampling_rate_input=4e6, sensing_coil_turns_input=400, gain_input=400)

if __name__ == "__main__":
  print(r798d_info.sample_id(), r798d_info.description())
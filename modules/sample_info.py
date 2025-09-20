class Sample:
  def __init__(self, sample_id_input: str, description_input: str, num_of_files_input: int, sampling_rate_input = int) -> None:
    self.sample_id_assign = sample_id_input
    self.description_assign = description_input
    self.num_of_files_assign = num_of_files_input
    self.sampling_rate_assign = sampling_rate_input

  def sample_id(self) -> str:
    return self.sample_id_assign

  def description(self) -> str:
    return self.description_assign


  def num_of_files(self) -> int:
    return self.num_of_files_assign

  def sampling_rate(self) -> int:
    return sampling_rate_assign

r798d_info: Sample = Sample(sample_id_input="R798D", description_input=f"Py(1000nm)", num_of_files_input=212, sampling_rate_input=4e6)

if __name__ == "__main__":
  print(r798d_info.sample_id(), r798d_info.description())
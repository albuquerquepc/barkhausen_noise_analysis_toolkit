class Paths:
    def __init__(self, path_string: str) -> None:
        self.get_path = path_string

    def path(self) -> str:
        return self.get_path

MAIN_DATA_DIRECTORY: Paths = Paths(f"/home/paulo/Documentos/ic_gmag/medidas/Py(1000nm)/")

ORIGINAL_DATA: Paths = Paths(f"{MAIN_DATA_DIRECTORY.path()}Original_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/")

PREPARED_DATA: Paths = Paths(f"{MAIN_DATA_DIRECTORY.path()}Prepared_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/")

MEAN_DATA: Paths = Paths(f"{MAIN_DATA_DIRECTORY.path()}Means_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/")

import os  # Library to manipulate system files
# Library to manipulate raw data (similar to numpy, personal preference)
import pandas as pd
import pyqtgraph  # Library to generate native gpu-accelerated graphs


class FileWorkers():  # In this class, we deal with input processing and file name retrieaval

    def __init__(self) -> None:
        super().__init__()

    # This collects the path to the folder that cointains all the data files and the keyword (sample name) desired

    def userInput(self) -> None:
        self.pathToData = input("Digite o caminho da pasta: ")
        self.keywordToMatch = input("Digite o nome completo da amostra: ")
        return

    # This will create a list (of flexible size) with the name of all the .dat files in the folder specified previously that have the chosen keyword (sample name) at the start of it

    def getMatchingFiles(self) -> None:
        self.allFilesInFolder = [self.dataFile for self.dataFile in os.listdir(
            self.pathToData) if self.dataFile.endswith(".dat")]
        self.filesWithKeyWord = [fileWithKeyword for fileWithKeyword in self.allFilesInFolder if (
            fileWithKeyword.startswith(self.keywordToMatch) and fileWithKeyword.endswith(".dat"))]
        self.sortedMatchingFiles = sorted(self.filesWithKeyWord)
        print(self.sortedMatchingFiles)
        return

    def getDataFromFile(self) -> None:
        self.timeAxis = pd.read_csv(
            f"{self.pathToData}/{self.keywordToMatch}_t.dat", header=None)
        self.fileToView = input(
            "Selecione o número da série a ser visualizado 001-200: ")
        self.serieNumber = int(self.fileToView)
        self.completeFilePath = f"{self.pathToData}/{self.keywordToMatch}{self.serieNumber:03}.dat"
        self.fileReader = pd.read_csv(self.completeFilePath, header=None)
        self.dfOfTimeSeries = pd.concat([self.timeAxis, self.fileReader], axis=1)
        self.dfOfTimeSeries.columns = ["Time", "Series"]
        print(self.dfOfTimeSeries)
        self.dfOfTimeSeries.plot(kind="line")



if __name__ == "__main__":
    fw = FileWorkers()
    fw.userInput()
    fw.getMatchingFiles()
    fw.getDataFromFile()

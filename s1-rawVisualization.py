import os  # Library to manipulate system files

import pandas as pd  # Library to manipulate raw data (similar to numpy, personal preference)

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QComboBox, QSpacerItem, QSizePolicy)

from pyqtgraph import PlotWidget, mkPen, setConfigOption

import re # Regex support

setConfigOption("background", "w")
setConfigOption("foreground", "k")

class FileWorkers():

    def __init__(self) -> None:
        super().__init__()

    def userInput(self, folderPath: str, keyword: str, timeAxisFile: str) -> None:
        self.folderPath = folderPath
        self.keywordToMatch = keyword
        self.timeAxisFile = timeAxisFile

    def getMatchingFiles(self) -> list:
        self.allFilesInFolder = [self.dataFile for self.dataFile in os.listdir(self.folderPath) if self.dataFile.endswith(".dat")]
        self.filesWithKeyWord = [fileWithKeyword for fileWithKeyword in self.allFilesInFolder if (
            fileWithKeyword.startswith(self.keywordToMatch) and fileWithKeyword.endswith(".dat"))]
        self.sortedMatchingFiles = sorted(
            [f for f in self.filesWithKeyWord if f != f"{self.keywordToMatch}_t.dat"])
        return self.sortedMatchingFiles

    def getDataFromFile(self, serieNumber: int) -> pd.DataFrame:
        self.timeAxis = pd.read_csv(
            f"{self.folderPath}/{self.timeAxisFile}", header=None)  # Use the user-specified time axis file
        self.serieNumber = serieNumber
        self.completeFilePath = f"{self.folderPath}/{self.keywordToMatch}{self.serieNumber:03}.dat"
        self.fileReader = pd.read_csv(self.completeFilePath, header=None)
        self.dfOfTimeSeries = pd.concat([self.timeAxis, self.fileReader], axis=1)
        self.dfOfTimeSeries.columns = ["Time", "Series"]
        return self.dfOfTimeSeries


class DataShower(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Plotter das séries temporais do BN")

        self.mainLayout = QHBoxLayout()

        self.leftContainer = QWidget()
        self.leftContainerLayout = QVBoxLayout()
        self.leftContainer.setLayout(self.leftContainerLayout)

        self.leftContainerLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.pathLabel = QLabel("Caminho da pasta: ")
        self.leftContainerLayout.addWidget(self.pathLabel)

        self.pathUserInput = QLineEdit()
        self.leftContainerLayout.addWidget(self.pathUserInput)

        self.browseButton = QPushButton("Abrir explorador de arquivos...")
        self.browseButton.clicked.connect(self.browseFolder)
        self.leftContainerLayout.addWidget(self.browseButton)

        self.keywordLabel = QLabel("Nome da amostra: ")
        self.leftContainerLayout.addWidget(self.keywordLabel)

        self.keywordUserInput = QLineEdit()
        self.leftContainerLayout.addWidget(self.keywordUserInput)

        self.loadButton = QPushButton("Indexar")
        self.loadButton.clicked.connect(self.loadMatchingFiles)
        self.leftContainerLayout.addWidget(self.loadButton)

        self.timeAxisLabel = QLabel("Nome do arquivo da série temporal: ")
        self.leftContainerLayout.addWidget(self.timeAxisLabel)

        self.timeAxisFileInput = QLineEdit()
        self.leftContainerLayout.addWidget(self.timeAxisFileInput)

        self.pathUserInput.textChanged.connect(self.checkInputs)
        self.keywordUserInput.textChanged.connect(self.checkInputs)
        self.timeAxisFileInput.textChanged.connect(self.checkInputs)


        self.fileIndexComboBox = QComboBox()
        self.fileIndexComboBox.addItem("Selecione uma série")
        self.fileIndexComboBox.currentIndexChanged.connect(self.updateFileIndex)
        self.fileIndexComboBox.setEnabled(False) 

        self.leftContainerLayout.addWidget(self.fileIndexComboBox)

        self.leftContainerLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.rightColumn = QVBoxLayout()
        self.plotWidget = PlotWidget()
        self.rightColumn.addWidget(self.plotWidget)

        self.mainLayout.addWidget(self.leftContainer, stretch=1)  # 1/3
        self.mainLayout.addLayout(self.rightColumn, stretch=2)  # 2/3

        self.setLayout(self.mainLayout)

        self.fileWorkerInterfacer = FileWorkers()

    def browseFolder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        if folder:
            self.pathUserInput.setText(folder)

    def loadMatchingFiles(self) -> None:
        path = self.pathUserInput.text()
        keyword = self.keywordUserInput.text()
        
        if not (path and keyword):
            self.fileIndexComboBox.setEnabled(False)
            self.fileIndexComboBox.clear()
            self.fileIndexComboBox.addItem("Selecione uma série")
            return 

        allFiles = [f for f in os.listdir(path) if f.endswith(".dat") and f.startswith(keyword)]
        
        seriesFiles = []
        timeAxisCandidate = None
        for f in allFiles:
            if re.search(r'\d{3}\.dat$', f):
                seriesFiles.append(f)
            else:

                if timeAxisCandidate is None:
                    timeAxisCandidate = f

        if timeAxisCandidate:
            self.timeAxisFileInput.setText(timeAxisCandidate)
        
        self.fileWorkerInterfacer.userInput(path, keyword, self.timeAxisFileInput.text())
        
        self.matchingFiles = seriesFiles  # Save for later use in updateFileIndex().
        self.fileIndexComboBox.clear()
        self.fileIndexComboBox.addItem("Selecione uma série")  # Default item
        for i in range(len(seriesFiles)):
            self.fileIndexComboBox.addItem(f"{i + 1}")  # 1-based numbering

        if seriesFiles:
            self.fileIndexComboBox.setEnabled(True)
        else:
            self.fileIndexComboBox.setEnabled(False)


    def updateFileIndex(self) -> None:
        selectedIndex = self.fileIndexComboBox.currentIndex() - 1  # Convert to 0-based index
        if selectedIndex >= 0 and selectedIndex < len(self.matchingFiles):
            fileName = self.matchingFiles[selectedIndex]
            self.plotData(fileName)

    def checkInputs(self) -> None:

        if self.pathUserInput.text() and self.keywordUserInput.text() and self.timeAxisFileInput.text():
            self.fileIndexComboBox.setEnabled(True)
        else:
            self.fileIndexComboBox.setEnabled(False)
            self.fileIndexComboBox.clear()
            self.fileIndexComboBox.addItem("Selecione uma série")


    def plotData(self, fileName: str) -> None:
        serieNumber = int(fileName[-7:-4])
        df = self.fileWorkerInterfacer.getDataFromFile(serieNumber)
        self.plotWidget.clear()
        
        xmin = df["Time"].min()
        xmax = df["Time"].max()
        ymin = df["Series"].min()
        ymax = df["Series"].max()

        self.plotWidget.getViewBox().setRange(xRange=[xmin, xmax], yRange=[ymin, ymax])

        # Plot the data
        self.plotWidget.plot(df["Time"], df["Series"], pen=mkPen("k", width=2))



if __name__ == "__main__":
    app = QApplication([])
    window = DataShower()
    window.resize(1600, 900)
    window.show()
    app.exec()

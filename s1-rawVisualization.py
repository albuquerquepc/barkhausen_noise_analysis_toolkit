import os #Basic os file manipulation
import pandas as pd #Data processing library, akin to Numpy; personal preference
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QComboBox, QSpacerItem, QSizePolicy) #GUI drawing tools
from PySide6.QtCore import Qt #Qt interfacing
from pyqtgraph import PlotWidget, mkPen, setConfigOption, ScatterPlotItem, mkBrush, PlotCurveItem #GPU-accelerated plotting capabilities
import re #Regex support


#For some reason, this only works here. I really don't know why, maybe a bug?
setConfigOption("background", "w")
setConfigOption("foreground", "k")


#File management and data processing class handler
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
            f"{self.folderPath}/{self.timeAxisFile}", header=None)
        self.serieNumber = serieNumber
        self.completeFilePath = f"{self.folderPath}/{self.keywordToMatch}{self.serieNumber:03}.dat"
        self.fileReader = pd.read_csv(self.completeFilePath, header=None)
        self.dfOfTimeSeries = pd.concat([self.timeAxis, self.fileReader], axis=1)
        self.dfOfTimeSeries.columns = ["Time", "Series"]
        return self.dfOfTimeSeries

#GUI interectability and data show class handler
class DataShower(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Plotter das séries temporais do BN")
        self.highlightPlot = None
        self.currentHighlightedIndex = None
        self.currentDataX = None
        self.currentDataY = None
        self.setFocusPolicy(Qt.StrongFocus)

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

        self.leftContainerLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.numberOfPointsTeller = QLabel("Número de pontos: ")
        self.leftContainerLayout.addWidget(self.numberOfPointsTeller)
        self.timeSpanTeller = QLabel("Duração da varredura: ")
        self.leftContainerLayout.addWidget(self.timeSpanTeller)
        self.samplingRateTeller = QLabel("Sampling Rate: ")
        self.leftContainerLayout.addWidget(self.samplingRateTeller)

        self.leftContainerLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.rightColumn = QVBoxLayout()
        self.plotWidget = PlotWidget()
        self.rightColumn.addWidget(self.plotWidget)

        self.dataInfoLabel = QLabel("Clique em um ponto ou use ← → para navegar")
        self.rightColumn.addWidget(self.dataInfoLabel)

        self.zoomControlLayout = QHBoxLayout()
        self.zoomInButton = QPushButton("Zoom In")
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomControlLayout.addWidget(self.zoomInButton)
        self.zoomOutButton = QPushButton("Zoom Out")
        self.zoomOutButton.clicked.connect(self.zoomOut)
        self.zoomControlLayout.addWidget(self.zoomOutButton)

        self.rightColumn.addLayout(self.zoomControlLayout)

        self.mainLayout.addWidget(self.leftContainer, stretch=1)
        self.mainLayout.addLayout(self.rightColumn, stretch=2)
        self.setLayout(self.mainLayout)

        self.fileWorkerInterfacer = FileWorkers()

        self.plotWidget.scene().sigMouseClicked.connect(self.onPlotClicked)

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

        self.matchingFiles = seriesFiles
        self.fileIndexComboBox.clear()
        self.fileIndexComboBox.addItem("Selecione uma série")
        for i in range(len(seriesFiles)):
            self.fileIndexComboBox.addItem(f"{i + 1}")

        self.fileIndexComboBox.setEnabled(bool(seriesFiles))


    def updateFileIndex(self) -> None:
        selectedIndex = self.fileIndexComboBox.currentIndex() - 1
        if 0 <= selectedIndex < len(self.matchingFiles):
            self.plotData(self.matchingFiles[selectedIndex])
            serieNumber = int(self.matchingFiles[selectedIndex][-7:-4])
            df = self.fileWorkerInterfacer.getDataFromFile(serieNumber)
            lenOfSeries = len(df["Series"].values)
            sweepDuration = (max(df["Time"].values) - min(df["Time"].values))
            samplingRate = lenOfSeries * sweepDuration
            self.numberOfPointsTeller.setText(f"Número de pontos: {lenOfSeries}")
            self.timeSpanTeller.setText(f"Duração da varredura: {sweepDuration} (s)")
            self.samplingRateTeller.setText(f"Samplign Rate: {samplingRate} (S/s)")

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

        self.currentDataX = df["Time"].values
        self.currentDataY = df["Series"].values

        self.plotWidget.setLabel('left', 'V=dphi/dt (V)')
        self.plotWidget.setLabel('bottom', 'time (s)')

        xmin, xmax = self.currentDataX.min(), self.currentDataX.max()
        ymin, ymax = self.currentDataY.min(), self.currentDataY.max()
        self.plotWidget.getViewBox().setRange(xRange=[xmin, xmax], yRange=[ymin, ymax])

        curve = PlotCurveItem(
            self.currentDataX,
            self.currentDataY,
            pen=mkPen("k", width=2),
            downsample=10,
            autoDownsample=True
        )
        self.plotWidget.addItem(curve)

    def onPlotClicked(self, event) -> None:
        if self.currentDataX is None:
            return
        pos = event.scenePos()
        vb = self.plotWidget.getViewBox()
        mousePoint = vb.mapSceneToView(pos)
        x_clicked = mousePoint.x()
        index = int((abs(self.currentDataX - x_clicked)).argmin())
        self.currentHighlightedIndex = index
        self.updateHighlight(self.currentDataX[index], self.currentDataY[index])

    def updateHighlight(self, x: float, y: float) -> None:
        if self.highlightPlot:
            self.plotWidget.removeItem(self.highlightPlot)
        self.highlightPlot = ScatterPlotItem([x], [y], size=10, brush=mkBrush('r'))
        self.plotWidget.addItem(self.highlightPlot)
        self.dataInfoLabel.setText(f"x: {x}, y: {y}")

    def zoomIn(self) -> None:
        vb = self.plotWidget.getViewBox()
        vb.scaleBy((0.9, 0.9))

    def zoomOut(self) -> None:
        vb = self.plotWidget.getViewBox()
        vb.scaleBy((1.1, 1.1))

    def keyPressEvent(self, event) -> None:
        if self.currentDataX is None or self.currentHighlightedIndex is None:
            return super().keyPressEvent(event)
        if event.key() == Qt.Key_Right and self.currentHighlightedIndex < len(self.currentDataX) - 1:
            self.currentHighlightedIndex += 1
            x = self.currentDataX[self.currentHighlightedIndex]
            y = self.currentDataY[self.currentHighlightedIndex]
            self.updateHighlight(x, y)
        elif event.key() == Qt.Key_Left and self.currentHighlightedIndex > 0:
            self.currentHighlightedIndex -= 1
            x = self.currentDataX[self.currentHighlightedIndex]
            y = self.currentDataY[self.currentHighlightedIndex]
            self.updateHighlight(x, y)
        else:
            super().keyPressEvent(event)

#Boilerplate block for code execution
if __name__ == "__main__":
    app = QApplication([])
    window = DataShower()
    window.resize(1600, 900)
    window.show()
    app.exec()

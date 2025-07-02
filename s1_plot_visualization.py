import os
import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
from pyqtgraph import PlotWidget, mkPen, setConfigOption, ScatterPlotItem, mkBrush, PlotCurveItem

# For some reason, this only works here. I really don't know why, maybe a bug?
setConfigOption("background", "w")
setConfigOption("foreground", "k")


# File management and data processing class handler
class FileWorkers():
    def __init__(self) -> None:
        super().__init__()

    def get_data_from_file(self, data_file_path: str, time_axis_file_path: str) -> tuple[np.ndarray, np.ndarray]:
        time_axis = np.loadtxt(time_axis_file_path)
        series_data = np.loadtxt(data_file_path, dtype=np.float128)
        return time_axis, series_data

# GUI interectability and data show class handler
class DataShower(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Plotter das séries temporais do BN")
        self.highlight_plot = None
        self.current_highlighted_index = None
        self.current_data_x = None
        self.current_data_y = None
        self.setFocusPolicy(Qt.StrongFocus)

        self.main_layout = QHBoxLayout()

        self.left_container = QWidget()
        self.left_container_layout = QVBoxLayout()
        self.left_container.setLayout(self.left_container_layout)

        self.left_container_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.data_file_path_label = QLabel("Caminho do arquivo de dados (.dat):")
        self.left_container_layout.addWidget(self.data_file_path_label)

        self.data_file_path_input = QLineEdit()
        self.data_file_path_input.setText("/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_FFT_0.2316s_0.2318s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/R798D001.dat")
        self.left_container_layout.addWidget(self.data_file_path_input)

        self.browse_data_file_button = QPushButton("Procurar arquivo de dados...")
        self.browse_data_file_button.clicked.connect(self.browse_data_file)
        self.left_container_layout.addWidget(self.browse_data_file_button)

        self.time_axis_path_label = QLabel("Caminho do arquivo do eixo de tempo:")
        self.left_container_layout.addWidget(self.time_axis_path_label)

        self.time_axis_path_input = QLineEdit()
        self.time_axis_path_input.setText("/home/paulo/Scripts/barkhausen-noise-analysis/Prepared_Selected_FFT_0.2316s_0.2318s_Py_1000nm_R798D_0.05Hz_100kHz_4MSs/R798D_t.dat")
        self.left_container_layout.addWidget(self.time_axis_path_input)

        self.browse_time_file_button = QPushButton("Procurar arquivo de tempo...")
        self.browse_time_file_button.clicked.connect(self.browse_time_file)
        self.left_container_layout.addWidget(self.browse_time_file_button)

        self.plot_button = QPushButton("Plotar")
        self.plot_button.clicked.connect(self.plot_from_inputs)
        self.left_container_layout.addWidget(self.plot_button)

        self.left_container_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.number_of_points_teller = QLabel("Número de pontos: ")
        self.left_container_layout.addWidget(self.number_of_points_teller)
        self.time_span_teller = QLabel("Duração da varredura: ")
        self.left_container_layout.addWidget(self.time_span_teller)
        self.sampling_rate_teller = QLabel("Sampling Rate: ")
        self.left_container_layout.addWidget(self.sampling_rate_teller)

        self.left_container_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.right_column = QVBoxLayout()
        self.plot_widget = PlotWidget()
        self.right_column.addWidget(self.plot_widget)

        self.data_info_label = QLabel("Clique em um ponto ou use ← → para navegar")
        self.right_column.addWidget(self.data_info_label)

        self.zoom_control_layout = QHBoxLayout()
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_control_layout.addWidget(self.zoom_in_button)
        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_control_layout.addWidget(self.zoom_out_button)

        self.right_column.addLayout(self.zoom_control_layout)

        self.main_layout.addWidget(self.left_container, stretch=1)
        self.main_layout.addLayout(self.right_column, stretch=2)
        self.setLayout(self.main_layout)

        self.file_worker_interfacer = FileWorkers()

        self.plot_widget.scene().sigMouseClicked.connect(self.on_plot_clicked)

    def browse_data_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo de dados", "", "Data Files (*.dat)")
        if file_path:
            self.data_file_path_input.setText(file_path)

    def browse_time_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo de eixo de tempo", "", "Data Files (*.dat)")
        if file_path:
            self.time_axis_path_input.setText(file_path)

    def plot_from_inputs(self) -> None:
        data_path = self.data_file_path_input.text()
        time_path = self.time_axis_path_input.text()

        if not (data_path and time_path and os.path.exists(data_path) and os.path.exists(time_path)):
            self.data_info_label.setText("Erro: Verifique se os caminhos dos arquivos estão corretos.")
            return

        try:
            time_data, series_data = self.file_worker_interfacer.get_data_from_file(data_path, time_path)
            self.plot_data(time_data, series_data)

            len_of_series = len(series_data)
            sweep_duration = (time_data[-1] - time_data[0])
            sampling_rate = len_of_series / sweep_duration if sweep_duration > 0 else 0
            self.number_of_points_teller.setText(f"Número de pontos: {len_of_series}")
            self.time_span_teller.setText(f"Duração da varredura: {sweep_duration:.4f} (s)")
            self.sampling_rate_teller.setText(f"Sampling Rate: {sampling_rate:.2f} (S/s)")
            self.data_info_label.setText("Clique em um ponto ou use ← → para navegar")
        except Exception as e:
            self.data_info_label.setText(f"Falha ao carregar dados: {e}")

    def plot_data(self, time_data: np.ndarray, series_data: np.ndarray) -> None:
        self.plot_widget.clear()
        self.highlight_plot = None
        self.current_highlighted_index = None

        self.current_data_x = time_data
        self.current_data_y = series_data

        self.plot_widget.setLabel('left', 'V=dphi/dt (V)')
        self.plot_widget.setLabel('bottom', 'time (s)')

        xmin, xmax = self.current_data_x.min(), self.current_data_x.max()
        ymin, ymax = self.current_data_y.min(), self.current_data_y.max()
        self.plot_widget.getViewBox().setRange(xRange=[xmin, xmax], yRange=[ymin, ymax])

        curve = PlotCurveItem(
            self.current_data_x,
            self.current_data_y,
            pen=mkPen("k", width=2),
            downsample=10,
            autoDownsample=True
        )
        self.plot_widget.addItem(curve)

    def on_plot_clicked(self, event) -> None:
        if self.current_data_x is None:
            return
        pos = event.scenePos()
        view_box = self.plot_widget.getViewBox()
        mouse_point = view_box.mapSceneToView(pos)
        x_clicked = mouse_point.x()
        index = int((abs(self.current_data_x - x_clicked)).argmin())
        self.current_highlighted_index = index
        self.update_highlight(self.current_data_x[index], self.current_data_y[index])

    def update_highlight(self, x: float, y: float) -> None:
        if self.highlight_plot:
            self.plot_widget.removeItem(self.highlight_plot)
        self.highlight_plot = ScatterPlotItem([x], [y], size=10, brush=mkBrush('r'))
        self.plot_widget.addItem(self.highlight_plot)
        self.data_info_label.setText(f"x: {x}, y: {y}")

    def zoom_in(self) -> None:
        view_box = self.plot_widget.getViewBox()
        view_box.scaleBy((0.9, 0.9))

    def zoom_out(self) -> None:
        view_box = self.plot_widget.getViewBox()
        view_box.scaleBy((1.1, 1.1))

    def keyPressEvent(self, event) -> None:
        if self.current_data_x is None or self.current_highlighted_index is None:
            super().keyPressEvent(event)
            return

        if event.key() == Qt.Key_Right and self.current_highlighted_index < len(self.current_data_x) - 1:
            self.current_highlighted_index += 1
            x = self.current_data_x[self.current_highlighted_index]
            y = self.current_data_y[self.current_highlighted_index]
            self.update_highlight(x, y)
        elif event.key() == Qt.Key_Left and self.current_highlighted_index > 0:
            self.current_highlighted_index -= 1
            x = self.current_data_x[self.current_highlighted_index]
            y = self.current_data_y[self.current_highlighted_index]
            self.update_highlight(x, y)
        else:
            super().keyPressEvent(event)

# Boilerplate block for code execution
if __name__ == "__main__":
    app = QApplication([])
    window = DataShower()
    window.resize(1600, 900)
    window.show()
    app.exec()
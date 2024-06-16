import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

from module.trigger_calc import trigger_station_calc, trigger_dock_calc, trigger_distance_calc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metro Bike App")
        self.setGeometry(100, 100, 1200, 800)  # Adjust size as needed

        # Central widget and layouts
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Views
        self.view1 = QWebEngineView()
        self.view2 = QWebEngineView()
        self.view3 = QWebEngineView()

        # Initialize views with initial HTML content
        self.view1.setHtml(self.read_file('views/user_bike_map.html'))
        self.view2.setHtml(self.read_file('views/user_dock_map.html'))
        self.view3.setHtml(self.read_file('views/user_bike_map.html'))

        # Input fields and buttons for each view
        self.setup_view(1, main_layout)
        self.setup_view(2, main_layout)
        self.setup_view(3, main_layout)

    def setup_view(self, view_number, layout):

        # Layout for each view
        view_layout = QVBoxLayout()
        view_layout.addWidget(eval(f'self.view{view_number}'))

        # Add view layout to main layout
        layout.addLayout(view_layout)

    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

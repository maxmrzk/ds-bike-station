import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QStackedWidget, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

from module.trigger_calc import trigger_station_calc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lat_entry = None
        self.long_entry = None
        self.k_entry = None
        self.setWindowTitle("Metro Bike App")
        self.setGeometry(100, 100, 1200, 800)  # Adjust size as needed

        # Create a stacked widget to switch between views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create and add the startup page
        self.startup_page = QWidget()
        self.setup_startup_page()
        self.stacked_widget.addWidget(self.startup_page)

        # Create and add each view
        self.view1 = self.create_view('views/user_bike_map.html', "View 1")
        self.stacked_widget.addWidget(self.view1)

        self.view2 = self.create_view('views/user_dock_map.html', "View 2")
        self.stacked_widget.addWidget(self.view2)

        self.view3 = self.create_view('views/user_bike_map.html', "View 3")
        self.stacked_widget.addWidget(self.view3)

        # Show the startup page initially
        self.stacked_widget.setCurrentWidget(self.startup_page)

    def setup_startup_page(self):
        layout = QGridLayout()

        # Add buttons to navigate to each view
        btn_view1 = QPushButton("Go to View 1")
        btn_view1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.view1))
        layout.addWidget(btn_view1, 0, 0, 1, 1)

        btn_view2 = QPushButton("Go to View 2")
        btn_view2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.view2))
        layout.addWidget(btn_view2, 0, 1, 1, 1)

        btn_view3 = QPushButton("Go to View 3")
        btn_view3.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.view3))
        layout.addWidget(btn_view3, 0, 2, 1, 1)

        # Add title label
        title_label = QLabel("Startup Page")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label, 1, 0, 1, 3)

        # Set layout spacing and alignment
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        self.startup_page.setLayout(layout)

    def create_view(self, html_file, view_title):
        page = QWidget()
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel(view_title)
        layout.addWidget(title_label)

        # Add a web view
        web_view = QWebEngineView()
        web_view.setHtml(self.read_file(html_file))
        layout.addWidget(web_view)

        # Input fields and a button to refresh content
        input_layout = QHBoxLayout()
        self.lat_entry = QLineEdit("34.0522")  # Default latitude
        self.lat_entry.textChanged.connect(lambda text: self.lat_entry.setText(text))
        input_layout.addWidget(QLabel("Latitude:"))
        input_layout.addWidget(self.lat_entry)

        self.long_entry = QLineEdit("-118.2437")  # Default longitude
        self.long_entry.textChanged.connect(lambda text: self.long_entry.setText(text))
        input_layout.addWidget(QLabel("Longitude:"))
        input_layout.addWidget(self.long_entry)

        self.k_entry = QLineEdit("5")  # Default K value
        self.k_entry.textChanged.connect(lambda text: self.k_entry.setText(text))
        input_layout.addWidget(QLabel("Number K:"))
        input_layout.addWidget(self.k_entry)

        layout.addLayout(input_layout)

        # Add a button to update the HTML content
        update_button = QPushButton("Update View")
        update_button.clicked.connect(lambda: self.update_view(web_view))
        layout.addWidget(update_button)

        # Add a button to navigate back to the startup page
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.startup_page))
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def update_view(self, web_view):
        try:
            float_lat = float(self.lat_entry.text())
            float_long = float(self.long_entry.text())
            int_k = int(self.k_entry.text())

            coordinates = (float_lat, float_long)
            trigger_station_calc(int_k, coordinates)

            web_view.setHtml(self.read_file('views/user_bike_map.html'))
        except ValueError:
            # Show an error message if inputs are not valid numbers
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values.")

    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

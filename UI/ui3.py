import sys
import csv
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem
)

class CSVViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Viewer")

        # Main layout for overall structure
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Horizontal layout for the top tables
        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        # Load and add existing tables
        self.csv_files = ["last_5minutes.csv", "output_client.csv", "output_security.csv"]
        self.table_widgets = []
        for csv_file in self.csv_files:
            table_widget = QTableWidget()
            self.load_csv_data(table_widget, csv_file)
            self.top_layout.addWidget(table_widget)
            self.table_widgets.append(table_widget)
        # Create and add the new full-width table
        
        self.bottom_table = QTableWidget()
        self.load_csv_data(self.bottom_table, "sample-trades.csv")
        self.main_layout.addWidget(self.bottom_table)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tables)
        self.timer.start(1000)  # Check for updates every second

    def load_csv_data(self, table_widget, csv_file):
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            data_rows = list(reader)  # Store data rows in a list

            table_widget.setColumnCount(len(header))
            table_widget.setHorizontalHeaderLabels(header)
            table_widget.setRowCount(len(data_rows))  # Set row count to the number of data rows

            for row, data in enumerate(data_rows):
                for col, value in enumerate(data):
                    table_widget.setItem(row, col, QTableWidgetItem(str(value)))

    def update_tables(self):
        for csv_file, table_widget in zip(self.csv_files, self.table_widgets):
            self.load_csv_data(table_widget, csv_file)
            # self.load_csv_data(self.bottom_table, "sample-trades.csv")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec_())

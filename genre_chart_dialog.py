from PyQt5.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GenreChartDialog(QDialog):
    def __init__(self, genre_counts, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ნანახი ფილმების სტატისტიკა ჟანრით")
        self.setFixedSize(500, 500)


        layout = QVBoxLayout(self)

        # Matplotlib figure and canvas
        self.figure = Figure(figsize=(4, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_pie_chart(genre_counts)

    def plot_pie_chart(self, genre_counts):
        ax = self.figure.add_subplot(111)
        ax.clear()

        labels = list(genre_counts.keys())
        sizes = list(genre_counts.values())

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')

        self.canvas.draw()
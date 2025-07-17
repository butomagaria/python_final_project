from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class MovieDialog(QDialog):
    def __init__(self, movie_title, movie_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle(movie_title)
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: black; color: white; font-size: 14px;")

        layout = QVBoxLayout()

        label = QLabel(movie_info)
        label.setWordWrap(True)
        layout.addWidget(label)

        button_layout = QHBoxLayout()

        self.watch_later_btn = QPushButton()
        self.watch_later_btn.setIcon(QIcon("icons/clock.png"))
        self.watch_later_btn.setIconSize(QSize(32, 32))
        button_layout.addWidget(self.watch_later_btn)
        self.watch_later_btn.setStyleSheet("background-color: white; border: none;")

        self.fav_btn = QPushButton()
        self.fav_btn.setIcon(QIcon("icons/star_empty.png"))
        self.fav_btn.setIconSize(QSize(32, 32))
        button_layout.addWidget(self.fav_btn)
        self.fav_btn.setStyleSheet("background-color: white; border: none;")

        self.watched_btn = QPushButton()
        self.watched_btn.setIcon(QIcon("icons/check.png"))
        self.watched_btn.setIconSize(QSize(32, 32))
        button_layout.addWidget(self.watched_btn)
        self.watched_btn.setStyleSheet("background-color: white; border: none;")

        layout.addLayout(button_layout)
        self.setLayout(layout)

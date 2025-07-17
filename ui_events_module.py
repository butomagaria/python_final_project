from PyQt5.QtWidgets import QMessageBox


def show_message(title, text, icon=QMessageBox.Information):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()


def confirm_action(parent, title, text):
    return QMessageBox.question(
        parent, title, text, QMessageBox.Yes | QMessageBox.No
    )


def style_app(app):
    app.setStyleSheet("""
        QMessageBox {
            background-color: black;
            color: white;
        }
        QMessageBox QLabel {
            color: white;
        }
        QMessageBox QPushButton {
            background-color: #444;
            color: white;
        }
        QDialog {
            background-color: black;
            color: white;
        }
        QDialog QLabel {
            color: white;
        }
        QDialog QPushButton {
            background-color: #444;
            color: white;
        }
    """)
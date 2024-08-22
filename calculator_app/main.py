from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QFont

class calcApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("calc")
        self.resize(444, 222)

        self.text_box = QLineEdit()
        self.text_box.setFont(QFont("monospace", 32))
        self.text_box.setContentsMargins(10, 10, 10, 10)  # Add margin around the text box
        self.grid = QGridLayout()

        self.buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
        ]

        self.clear = QPushButton("clear")
        self.delete = QPushButton("<")

        row = 0
        col = 0
        for text in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_click)
            button.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding: 10px;}")
            self.grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.clear.clicked.connect(self.button_click)
        self.delete.clicked.connect(self.button_click)
        self.clear.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding: 10px;}")
        self.delete.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding: 10px;}")

        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)

        button_row = QHBoxLayout()
        button_row.addWidget(self.clear)
        button_row.addWidget(self.delete)
        master_layout.addLayout(button_row)
        master_layout.setContentsMargins(25, 25, 25, 25)

        self.setLayout(master_layout)

    def button_click(self):
        button = self.sender()
        text = button.text()

        if text == "=":
            expression = self.text_box.text()
            try:
                res = eval(expression)
                self.text_box.setText(str(res))
            except Exception as e:
                self.text_box.setText("Error")
        
        elif text == "<":
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
        
        elif text == "clear":
            self.text_box.clear()

        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)


if __name__ == "__main__":
    app = QApplication([])
    main_window = calcApp()
    main_window.show()
    app.exec()

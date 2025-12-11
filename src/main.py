import os
import sys

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi


class TicketBester(QWidget):

    def __init__(self):
        # Initialize the application
        self.app = QApplication(sys.argv)

        # Load the UI file
        ui_file_path = './qt/GUI.ui'
        self.window = loadUi(ui_file_path)

        # Connect signals and slots, customize UI, etc.
        # (Add your customization code here)

        # Display the window
        self.window.show()

    def run(self):
        # Start the event loop
        sys.exit(self.app.exec())

def main():
    # Create an instance of the application class and run it
    my_app = TicketBester()
    my_app.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python
import sys
import os
from PyQt5.QtWidgets import QWidget, QInputDialog, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import numpy as np

class GUI(QMainWindow):

    # Initializes Main Window, sets size and file.
    
    def __init__(self):
        super().__init__()
        self.title = 'Multiplication App'
        self.left = 10
        self.top = 20
        self.width = 500
        self.height = 500
        self.path0, file0 = os.path.split(__file__)
        
        # Import Style Sheet
        
        with open(self.path0 + '/stylesheet.css', "r") as fh:
            self.setStyleSheet(fh.read())
        
        self.initUI()
        
    def initUI(self):
        
        # Sets up main window, and sets the central widget, which will be modified in START_SCREEN.
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.layout = QVBoxLayout()
        self.display = START_SCREEN(self)
        self.setCentralWidget(self.display)
        self.show()
        
class START_SCREEN(QWidget):
     
    
    #modifies cenral widget
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.path0 = parent.path0
        
        # Main Layout of central widget is vertical.
        self.layout = QVBoxLayout()
        self.label = QLabel('Multiplication')
        self.layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Creates an image and adjusts size.
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap(self.path0 + '/icons/hex.png')
        self.smaller_pixmap = self.pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.image.setPixmap(self.smaller_pixmap)

        # Set label font
        font = QFont("Arial", 40, QFont.Bold)
        self.label.setFont(font)
        
        # Creates an organizer for the Start Screen buttons (Start, Quit, and Stop)
        self.buttonShelf = QWidget()
        self.buttonShelfLayout = QHBoxLayout()
        
        # Start button launches game.
        self.startButton = QPushButton('Start')
        self.startButton.setFixedSize(200, 50)
        
        # Quit button exits main window
        self.quitButton = QPushButton('Quit')
        self.quitButton.setFixedSize(200, 50)
        
        #Stop button brings user back to start screen.
        self.stopButton = QPushButton('Stop')
        self.stopButton.setFixedSize(200, 50)

        # Hide stop button, since we are already on main screen.
        self.stopButton.hide()
        
        # Create connections for the buttons.
        self.startButton.clicked.connect(self.playState)
        self.quitButton.clicked.connect(sys.exit)
        
        # Organize button shelf layout.
        self.buttonShelfLayout.addWidget(self.startButton)
        self.buttonShelfLayout.addWidget(self.stopButton)
        self.buttonShelfLayout.addWidget(self.quitButton)
        self.buttonShelf.setLayout(self.buttonShelfLayout)

        # Create a button where user can click to pick a number
        self.getValue = QPushButton('Pick a Number')
        self.getValue.clicked.connect(self.prompt)
        
        # Sets value to -1, in case user doesn't pick any number. 
        # Will be used later to generate random multiplication problems.
        self.value = [-1]
        
        # All widgets are added to the layout in order of apperance.
        self.layout.addWidget(self.getValue)
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.getValue)
        self.layout.addWidget(self.buttonShelf)
        
        # Sets main layout.
        self.setLayout(self.layout)
        
    def prompt(self):
        # User is prompted to select an integer between 0-9.
        self.value = QInputDialog.getInt(self, 'Window', 'Enter an integer between 0-9', 0, 0, 9, 1)
         
    def playState(self):
        # Game setup begins. QWidgets are added for oganization.
        self.label.setText('')
        self.row1 = QWidget()
        self.row2 = QWidget()
        
        # Initialize player score.
        self.score = 0
        
        # Answer buttons are created.
        self.btn1 = QPushButton('1')
        self.btn2 = QPushButton('2')
        self.btn3 = QPushButton('3')
        self.btn4 = QPushButton('4')
       
        # Create horizontal layouts
        self.layoutrow1 = QHBoxLayout()
        self.layoutrow2 = QHBoxLayout()
        
        # Answer buttons are added to the screen.
        self.layoutrow2.addWidget(self.btn1)
        self.layoutrow2.addWidget(self.btn2)
        self.layoutrow1.addWidget(self.btn3)
        self.layoutrow1.addWidget(self.btn4)
        
        # answer rows are added to the main layout.
        self.layout.addWidget(self.row1)
        self.layout.addWidget(self.row2)
        
        # Apply horizontal layouts to the answer rows.
        self.row1.setLayout(self.layoutrow1)
        self.row2.setLayout(self.layoutrow2)
        self.button_array = [self.btn1, self.btn2, self.btn3, self.btn4]
        
        # Hide unnecessary buttons
        self.getValue.hide()
        self.startButton.disconnect()
        
        # Trigger next state, game begins.
        self.generateAnswer()
    
    
    def generateAnswer(self):
        # Random numbers are generated, main image is hidden.
        self.image.hide()

        # Remove previous connections in buttons
        for i, button in enumerate(self.button_array):
            button.disconnect()
            
        # Create a set keeping track of unique answers
        answerBank = set([])
        
        # Create a bool to keep track of whether the user deserves a point
        self.correct = True
        
        # Hide unnecessary buttons
        self.quitButton.hide()
        self.stopButton.show()
        
        # Sees if user has selected a valid number. If so, number is used.
        self.x = int(self.value[0])
        if self.x != -1:
            firstInt = self.x
        else :
            # If not, a random number is generated between 0-9.
            firstInt = np.random.randint(0, 9)
        
        # Another random number is generated between 0-9.
        secondInt = np.random.randint(0, 9)
        
        # Answer is calculated.
        self.ans = firstInt * secondInt
        
        # Answer is added to the answerBank, to prevent duplicates from being made.
        answerBank.add(self.ans)

        # Alter button text and functions; start becomes next. Stop button is connected & shown.
        self.startButton.setText('Next')
        self.startButton.clicked.connect(self.generateAnswer)
        self.stopButton.clicked.connect(self.STOP)
        self.stopButton.show()
        
        # Hide the getValue button since it is no longer needed at this point.
        self.getValue.hide()
        
        # Updates label with the multiplication problem.
        self.sol = ' ' + str(firstInt) + ' x ' + str(secondInt) + ' = '
        self.label.setText(self.sol + '?')
        
        # Randomly generates a location; one of the 4 buttons will hold the answer.
        self.answerPlacement = np.random.randint(0,4)
        
        # Set either a fake answer or the real answer to each of the buttons.
        for i, button in enumerate(self.button_array):
            if i == self.answerPlacement:
                button.setText(str(self.ans))
                button.setStyleSheet("background-color: green")
                button.clicked.connect(self.rightAnswer)
            else:
                fakeAnswer = np.random.randint(0, 9) * np.random.randint(0, 9)
                while (fakeAnswer in answerBank) == True:
                    fakeAnswer = np.random.randint(0, 9) * np.random.randint(0, 9)
                answerBank.add(fakeAnswer)
                button.setText(str(fakeAnswer))
                # If the wrong button is clicked, the button will become red.
                button.setStyleSheet("QPushButton { background-color: green }"
                                     "QPushButton:pressed { background-color: red }" )
                button.clicked.connect(self.wrongAnswer)
                
    # This method tells the user that their answer was wrong. The user is no longer elegible for a point.   
    def wrongAnswer(self):
        self.correct = False
        self.label.setText(self.sol + '?' + ' Try again.')
        
    # This method tells the user that their answer is right, and increments their score.
    def rightAnswer(self, button):
        if self.correct == True:
            self.score +=1
        self.label.setText(self.sol + str(self.ans) + '       Correct! :)' + '  Your Score is: ' + str(self.score))
        
    def STOP(self):
    # This method resets all labels, buttons, and images to the start screen state.
        self.image.show()
        self.label.setText('Multiplication Game')
        self.newscreen = START_SCREEN(self)
        self.startButton.setText('Start')
        self.stopButton.hide()
        self.getValue.show()
        self.quitButton.show()
        self.startButton.clicked.connect(self.playState)
        self.row1.hide()
        self.row2.hide()
        self.scoreBoard.hide()
        
def main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    screen_resolution = app.desktop().screenGeometry()
    width = screen_resolution.width()
    gui.setGeometry(width * 0.025, 0, width * 0.95, width * 0.45)
    sys.exit(app.exec_())
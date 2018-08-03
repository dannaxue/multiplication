#!/usr/bin/env python
import sys
import os
from PyQt5.QtWidgets import QButtonGroup, QSizePolicy, QWidget, QInputDialog, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
# from multiplication.display import playState
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy as np

class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Multiplication App'
        self.left = 10
        self.top = 20
        self.width = 500
        self.height = 500
        self.path0, file0 = os.path.split(__file__)
        self.quitButton = QPushButton('Quit')
        
        # Style
        
        with open(self.path0 + '/stylesheet.css', "r") as fh:
            self.setStyleSheet(fh.read())
        
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.layout = QVBoxLayout()
        self.display = START_SCREEN(self)
        self.setCentralWidget(self.display)
        self.show()
        
class START_SCREEN(QWidget):
     
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.label = QLabel('Multiplication Game')
        self.layout.addWidget(self.label)
        font = QFont("Arial", 40, QFont.Bold)
        self.label.setFont(font)
        self.buttonShelf = QWidget()
        self.buttonShelfLayout = QHBoxLayout()
        self.startButton = QPushButton('Start')
        self.quitButton = QPushButton('Quit')

        self.stopButton = QPushButton('Stop')
        self.stopButton.hide()
        # self.stopButton.clicked.connect(self.STOP)
        # self.startButton.resize(50,50)
        self.startButton.clicked.connect(self.playState)
        self.quitButton.clicked.connect(sys.exit)
        self.buttonShelfLayout.addWidget(self.startButton)
        self.buttonShelfLayout.addWidget(self.stopButton)
        self.buttonShelfLayout.addWidget(self.quitButton)
        self.buttonShelf.setLayout(self.buttonShelfLayout)
        
        self.value = [-1]
        self.getValue = QPushButton('Pick a Number')
        self.getValue.clicked.connect(self.prompt)
        # self.layout.addWidget(self.input)
        #self.layout.addWidget(self.table)
        self.layout.addWidget(self.getValue)
        self.layout.addWidget(self.buttonShelf)
        self.setLayout(self.layout)
        
    def prompt(self):
        self.value = QInputDialog.getText(self, 'Window', 'Enter an integer between 0-9')
        self.getValue.hide()
        
    def playState(self):
        self.label.setText('')
        self.row0 = QLabel()
        self.row1 = QWidget()
        self.row2 = QWidget()
        # self.label.setText('')

        self.score = 0
        
        self.btn1 = QPushButton('1')
        self.btn2 = QPushButton('2')
        self.btn3 = QPushButton('3')
        self.btn4 = QPushButton('4')
        
        self.layoutrow1 = QHBoxLayout()
        self.layoutrow2 = QHBoxLayout()

        self.layoutrow2.addWidget(self.btn1)
        self.layoutrow2.addWidget(self.btn2)
        self.layoutrow1.addWidget(self.btn3)
        self.layoutrow1.addWidget(self.btn4)
        
        self.layout.addWidget(self.row1)
        self.layout.addWidget(self.row2)
        
        self.row1.setLayout(self.layoutrow1)
        self.row2.setLayout(self.layoutrow2)
        self.button_array = [self.btn1, self.btn2, self.btn3, self.btn4]
        self.startButton.disconnect()
        self.generateAnswer()
    
    def generateAnswer(self):
        for i, button in enumerate(self.button_array):
            button.disconnect()
        self.correct = True
        self.quitButton.hide()
        self.stopButton.show()
        self.tracker = 0;
        self.button_location = np.zeros(4,)
        self.x = int(self.value[0])
        if self.x != -1:
            firstInt = self.x
        else :
            firstInt = np.random.randint(0, 9)
            
        secondInt = np.random.randint(0, 9)
        self.ans = firstInt * secondInt
        self.startButton.setText('Next')
        self.startButton.clicked.connect(self.generateAnswer)
        self.stopButton.clicked.connect(self.STOP)
        self.stopButton.show()
        self.getValue.hide()
        self.sol = ' ' + str(firstInt) + ' x ' + str(secondInt) + ' = '
        self.label.setText(self.sol + '?')
        self.answerPlacement = np.random.randint(0,4)
        
        for i, button in enumerate(self.button_array):
            if i == self.answerPlacement:
                button.setText(str(self.ans))
                button.setStyleSheet("background-color: green")
                button.clicked.connect(self.rightAnswer)
                
                
            else:
                fakeAnswer = np.random.randint(0, 9) * np.random.randint(0, 9)
                button.setText(str(fakeAnswer))
                button.setStyleSheet("QPushButton { background-color: green }"
                                     "QPushButton:pressed { background-color: red }" )
                self.button_location[i] = 1;
                button.clicked.connect(self.wrongAnswer)
                
        
    def wrongAnswer(self):
        self.correct = False
        self.label.setText(self.sol + '?' + ' Try again.')
        
    def rightAnswer(self, button):
        if self.correct == True:
            self.score +=1
        self.label.setText(self.sol + str(self.ans) + '       Correct! :)' + '      Your Score is: ' + str(self.score))
        print('Right')
        
    def STOP(self):
        self.label.setText('Multiplication Game')
        self.newscreen = START_SCREEN(self)
        self.startButton.setText('Start')
        self.stopButton.hide()
        self.getValue.show()
        self.quitButton.show()
        self.startButton.clicked.connect(self.playState)
        self.row1.hide()
        self.row2.hide()
        
def main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    screen_resolution = app.desktop().screenGeometry()
    width = screen_resolution.width()
    gui.setGeometry(width * 0.025, 0, width * 0.95, width * 0.45)
    sys.exit(app.exec_())
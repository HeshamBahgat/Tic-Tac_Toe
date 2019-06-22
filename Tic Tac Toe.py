import sys
import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")

from PyQt4 import QtGui


import random

from functools import partial
import subprocess

from PyQt4.QtCore import *
from PyQt4.QtGui import *


def whogoesfirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return "computer"
    else:
        return "player"

def getboardcopy(board):
    # make a duplicate of the board list and return it the duplicate.
    dupeboard = []
    for i in board:
        dupeboard.append(i)
    return dupeboard

def isspacefree(board, move):
    # return true if the passed move is free on the passed board.
    return board[move] == " "

def isboardfull(board):
    # Return True if every space on the board has been taken. otherwise return False
    for i in range(0, 9):
        if isspacefree(board, i):
            return False
    return True

def makemove(board, letter, move):
    board[move] = letter

def iswinner(bo, le):
    # Given a board and player's letter, this function returns True if that player won.
    # We use bo instead of board and le instead of letter so we dont have to type as much.
    return ((bo[6] == le and bo[7] == le and bo[8] == le) or
            (bo[3] == le and bo[4] == le and bo[5] == le) or
            (bo[0] == le and bo[1] == le and bo[2] == le) or
            (bo[2] == le and bo[5] == le and bo[8] == le) or
            (bo[1] == le and bo[4] == le and bo[7] == le) or
            (bo[0] == le and bo[3] == le and bo[6] == le) or
            (bo[0] == le and bo[4] == le and bo[8] == le) or
            (bo[2] == le and bo[4] == le and bo[6] == le))


def chooserandommovefromlist(board, moveslist):
    # return a valid move from the passed list on the passed board
    # return none if there is no valid move.
    possiblemoves = []
    for i in moveslist:
        if isspacefree(board, i):
            possiblemoves.append(i)
    if len(possiblemoves) != 0:
        return random.choice(possiblemoves)
    else:
        return None

def getcomputermove(board, computerletter):
    # given a board and the computer's letter, determine where to move and return that move.
    if computerletter == "X":
        playerletter = "O"
    else:
        playerletter = "X"
    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(0, 9):
        copy = getboardcopy(board)
        if isspacefree(copy, i):
            makemove(copy, computerletter, i)
            if iswinner(copy, computerletter):
                return i
    # check if the player could win on his next move, and black them.
    for i in range(0, 9):
        copy = getboardcopy(board)
        if isspacefree(copy, i):
            makemove(copy, playerletter, i)
            if iswinner(copy, playerletter):
                return i
    # Try to take one of the corners, if they are free.
    move = chooserandommovefromlist(board, [0, 2, 6, 8])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isspacefree(board, 5):
        return 4

    # Move on one of the sides.
    return chooserandommovefromlist(board, [1, 3, 5, 7])

class Game_Frame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.break_start = 0
        self.Final_result = ""

        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(300, 300, 250, 150)
        self.First_layout()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.First_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

    def First_layout(self):

        self.lbl1 = QLabel('Welcome To the Game!')
        self.lbl1.setFixedWidth(200)

        self.lbl2 = QLabel("Do You Want To be X or O?")
        self.lbl3 = QComboBox()
        self.lbl3.addItems(["Choose X or O", "X", "O"])
        self.lbl3.activated[str].connect(self.player_tag)

        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.lbl1, 0)
        self.layout1.addWidget(self.lbl2, 1)
        self.layout1.addWidget(self.lbl3, 1)

        self.First_widget = QWidget()
        self.First_widget.setLayout(self.layout1)

    def player_tag(self, tag):
        self.GameTage = ""
        if tag == "X":
            self.add_start()
            self.GameTage = ["X", "O"]
        elif tag == "O":
            self.add_start()
            self.GameTage = ["O", "X"]
        self.playertage, self.computertage = self.GameTage
        self.lbl3.addItem(self.playertage)

    def add_start(self):

        self.lbl3.removeItem(2)
        self.lbl3.removeItem(1)
        self.lbl3.removeItem(0)

        if self.break_start == 0:
            self.break_start += 1
            self.turn = whogoesfirst()
            self.lbl5 = QLabel("The " + self.turn + " Will go first.")
            self.layout1.addWidget(self.lbl5, 3)

            self.lbl4 = QPushButton("Start")
            self.lbl4.clicked.connect(self.switching_layouts)
            self.layout1.addWidget(self.lbl4, 2)
        else:
            print("erro")

    def switching_layouts(self):
        self.Second_Layout()
        self.stacked_layout.addWidget(self.Second_widget)
        self.stacked_layout.setCurrentIndex(1)

    def Second_Layout(self, Parent = None):


        self.theboard = [' '] * 9
        self.gameisplaying = True


        self.layout2 = QGridLayout()
        names = ('--','--', '--', '--', '--', '--', '--', '--', '--')
        self.button = []

        for i, name in enumerate(names):
            self.button.append(i)
            self.button[i] = QPushButton(self)
            self.button[i].setText("{0}".format(name))

            row, col = divmod(i, 3)
            self.layout2.addWidget(self.button[i], row, col)

            self.button[i].clicked.connect(partial(self.player_move, move= i))



        self.Second_widget = QWidget()
        self.Second_widget.setLayout(self.layout2)


        self.start_the_game()

    def start_the_game(self):
        if self.turn == "player":
            self.player_move

        elif self.turn == "computer":
            self.computer_move()

    def player_move(self, move):
        if self.gameisplaying == True:
            if self.theboard[move] == " ":
                self.button[move].setText(self.playertage)
                self.theboard[move] = self.playertage
                self.copy_pl_move = move

                if iswinner(self.theboard, self.playertage):
                    self.Final_result = ("Hooray! You have won the game!")
                    print("Hooray! You have won the game!")
                    self.gameisplaying = False


                else:
                    if isboardfull(self.theboard):
                        self.Final_result = ("the game is a tie!")
                        print("the game is a tie!")
                        self.gameisplaying = False

                    else:
                        self.turn = "computer"
                        self.computer_move()
            else:
                print("error")
        elif self.gameisplaying == False:
            print("game finshed")
            self.third_layout()
            self.stacked_layout.addWidget(self.Third_Widget)
            self.stacked_layout.setCurrentIndex(2)

    def computer_move(self):
        if self.gameisplaying == True:
            com_move = getcomputermove(self.theboard, self.computertage)
            if self.theboard[com_move] == " ":
                self.button[com_move].setText(self.computertage)
                self.button[com_move].setStyleSheet("background-color: green")
                self.theboard[com_move] = self.computertage

                if iswinner(self.theboard, self.computertage):
                    self.Final_result = ("You Lost!!!!!!!!!!!!")
                    print("You Lost!!!!!!!!!!!!")
                    self.gameisplaying = False
                else:
                    if isboardfull(self.theboard):
                        self.Final_result = ("the game is a tie!")
                        print('The game is a tie!')
                        self.gameisplaying = False

                    else:
                        self.turn = "player"
            else:
                print("error")

        elif self.gameisplaying == False:
            print("game finshed")
            self.third_layout()
            self.stacked_layout.addWidget(self.Third_Widget)
            self.stacked_layout.setCurrentIndex(2)


    def play_again(self, answer):
        print(answer)
        print("Do you want to play again? (yes or no)")
        #answer = input().lower().startswith("y")
        if answer == ("Yes"):
            print("Yessssssssssssssss")
            self.clearbutton()

        else:
            print("Nooooooooooooooooooooooooo")
            sys.exit()
            #return answer

    def clearbutton(self):
        restart_button = QPushButton("Restart", self)
        self.layout3.addWidget(restart_button, 2)
        restart_button.clicked.connect(self.restartGame)
    def restartGame(self):
        self.close()
        subprocess.call("python3" + " ~/PycharmProjects/Projects/Tic\ Tac\ Toe.py", shell=True)


    def third_layout(self):
        self.Third_Widget = QWidget()

        self.layout3 = QVBoxLayout()

        self.lbl_finsih = QLabel('Game Finshed! %s' %(self.Final_result ))
        self.lbl_play_again = QLabel('Do You Want to play again?')
        self.lbl_y_o_n = QComboBox()
        self.lbl_y_o_n.addItems(["Yes", "No"])
        self.lbl_y_o_n.activated[str].connect(self.play_again)

        self.layout3.addWidget(self.lbl_finsih, 0)
        self.layout3.addWidget(self.lbl_play_again, 1)
        self.layout3.addWidget(self.lbl_y_o_n, 2)
        self.Third_Widget.setLayout(self.layout3)


def main():
    app = QApplication(sys.argv)
    start_game = Game_Frame()
    start_game.show()
    start_game.raise_()
    app.exec_()

if __name__ == "__main__":
    main()
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QWidgetItem, QSlider
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QThread, pyqtSignal, QObject, Qt
import sys
import queue
# from time import sleep
from mathOp import calculateMath, findMath
import speech_recognition as sr



RECOGNIZER = sr.Recognizer()
MICROPHONE = sr.Microphone()


class ResObject(QObject):
    def __init__(self, val):
        super().__init__()
        self.val = val


class ListenThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, queue, callback, parent=None):
        QThread.__init__(self, parent)
        self.queue = queue
        self.finished.connect(callback)

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            arg = self.queue.get()
            print(arg)
            with MICROPHONE as source:
                print("Speak ...")
                RECOGNIZER.adjust_for_ambient_noise(source)
                audio = RECOGNIZER.listen(source)
            try:
                result = RECOGNIZER.recognize_google(audio)
            except:
                result = "Didn't know"
            self.queue.put(result)
            if result == "exit" or "kapat":
                self.__del__()
            self.fun(result)

    def fun(self, arg):
        self.sleep(2)
        self.finished.emit(ResObject(arg))


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 200
        self.top = 50
        self.width = 850
        self.height = 400



        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)

        self.text = QLabel()
        self.text.setParent(self.mainWidget)
        self.text.setFont(QFont("Times", 30, QFont.Bold))

        self.squares = []
        self.title = "PyQt 5 Application"

        self.VLayout = QVBoxLayout(self.mainWidget)
        self.VLayout.setContentsMargins(25, 25, 25, 25)

        self.blockQueue = queue.Queue(2)

        self.InitUI()

        self.listen_microphone()





    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.text.setGeometry(0, 450, self.width, self.height)

        self.text.setAlignment(Qt.AlignCenter)

        self.text.setText("TEST ŞEY EDİYORUZ BURADA")
        self.mainWidget.setStyleSheet("QWidget{background-color:gray;border:3px solid black}")


        self.VLayout.addWidget(self.text)
        self.show()



    def changeText(self, sayi):
        sayi = sayi.val
        if "change" or "color" in sayi:
            x = "QWidget{background-color:"+"red"+";border:3px solid black}"
            self.mainWidget.setStyleSheet(x)
        items = findMath(sayi)
        if "hide" in sayi:
            self.hide()
        if "exit" in sayi:
            sys.exit(self.exec_())
        if "show" in sayi:
            self.show()

        try:
            res = calculateMath(items)
            # print(bool((res)))
            if bool(res):
                x = SquareBlocks(self.mainWidget)
                x.createBlocks(items[0],items[2], res)
                if self.blockQueue.full():
                    print("çıkıyor")
                    f = self.blockQueue.get()
                    f.hide()
                    f.destroy()
                self.blockQueue.put(x)
                self.VLayout.addWidget(x)
                print(self.blockQueue.qsize())
        except:
            res = ""


        self.text.setText(str(sayi) + "  :  " + str(res))

    def listen_microphone(self):
        MAX_CORE = 1
        self.queue = queue.Queue()
        self.threads = []
        for i in range(MAX_CORE):
            self.thread = ListenThread(self.queue,self.changeText)
            self.threads.append(self.thread)
            self.thread.start()


        for _ in range(MAX_CORE):
            self.queue.put(None)




# blocks for mathematical squares in Main Widget
class SquareBlocks(QWidget):
    squares = []

    def __init__(self, parent):
        super(SquareBlocks, self).__init__(parent=parent)
        self.setMaximumSize(800,800)
        self.setMinimumSize(800, 200)
        # Bunlar sonradan silincek "main widget" sadece orda olduğunu görmek için varlar
        self.mainWidget = QWidget(self)
        self.mainWidget.setGeometry(self.geometry())

        self.blocks = []

        self.mainLayout = QHBoxLayout(self)
        # self.setLayout(self.mainLayout)

        self.initBlock()

    def initBlock(self):

        self.setStyleSheet("QWidget{background-color:yellow;border:3px solid red}")

        self.show()

    def createBlocks(self,*arg):
        for _ in arg:
            sq = Squares(self, _)
            sq.callMeYouNeed()
            self.blocks.append(sq)
            self.mainLayout.addWidget(sq)


class Squares(QWidget):
    def __init__(self, parent, count = 0):
        super(Squares, self).__init__(parent=parent)
        self.setStyleSheet("QWidget{background-color:green;border:2px solid blue}")
        self.widget = QWidget(self)
        # self.widget.setGeometry(0,0,100,100)
        self.count = count
        self.widget.setMinimumSize(250,250)
        self.widget.setMaximumSize(300,300)
        self.squareLayouts = QGridLayout(self)

        self.squares = []

        self.initUI()

    def initUI(self):
        self.show()


    def createSquares(self, count):

        posis = [(i, j) for i in range(count) for j in range(count)]
        for x in range(count):
            square = QWidget()
            square.setMaximumSize(50, 50)
            # square.setMinimumSize(50, 50)
            # try:
            square.setStyleSheet("QWidget{background-color:red}")
            # except:
            #     square.setStyleSheet("QWidget{background-color:red}")
            self.squares.append(square)
        x = 0
        y = 0
        for square in self.squares:
            if x+1 >= 5:
                x = 0
                y += 1
            else:
                x += 1
            self.squareLayouts.addWidget(square, *(x, y))

    def callMeYouNeed(self):
        self.createSquares(self.count)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())

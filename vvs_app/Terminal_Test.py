#
# import sys
# import code
# import re
# from typing import Callable
# from contextlib import redirect_stdout, redirect_stderr
#
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
#
#
# class LineEdit(QLineEdit):
#     """QLIneEdit with a history buffer for recalling previous lines.
#     I also accept tab as input (4 spaces).
#     """
#     newline = pyqtSignal(str)  # Signal when return key pressed
#
#     def __init__(self, history: int = 100) -> 'LineEdit':
#         super().__init__()
#         self.historymax = history
#         self.clearhistory()
#         self.promptpattern = re.compile('^[>\.]')
#
#     def clearhistory(self) -> None:
#         """Clear history buffer"""
#         self.historyindex = 0
#         self.historylist = []
#
#     def event(self, ev: QEvent) -> bool:
#         """Intercept tab and arrow key presses.  Insert 4 spaces
#         when tab pressed instead of moving to next contorl.  WHen
#         arrow up or down are pressed select a line from the history
#         buffer.  Emit newline signal when return key is pressed.
#         """
#         if ev.type() == QEvent.KeyPress:
#             if ev.key() == int(Qt.Key_Tab):
#                 self.insert('    ')
#                 return True
#             elif ev.key() == int(Qt.Key_Up):
#                 self.recall(self.historyindex - 1)
#                 return True
#             elif ev.key() == int(Qt.Key_Down):
#                 self.recall(self.historyindex + 1)
#                 return True
#             elif ev.key() == int(Qt.Key_Home):
#                 self.recall(0)
#                 return True
#             elif ev.key() == int(Qt.Key_End):
#                 self.recall(len(self.historylist) - 1)
#                 return True
#             elif ev.key() == int(Qt.Key_Return):
#                 self.returnkey()
#                 return True
#         return super().event(ev)
#
#     def returnkey(self) -> None:
#         """Return key was pressed.  Add line to history and emit
#         the newline signal.
#         """
#         text = self.text().rstrip()
#         self.record(text)
#         self.newline.emit(text)
#         self.setText('')
#
#     def recall(self, index: int) -> None:
#         """Select a line from the history list"""
#         length = len(self.historylist)
#         if length > 0:
#             index = max(0, min(index, length - 1))
#             self.setText(self.historylist[index])
#             self.historyindex = index
#
#     def record(self, line: str) -> None:
#         """Add line to history buffer"""
#         self.historyindex += 1
#         while len(self.historylist) >= self.historymax - 1:
#             self.historylist.pop()
#         self.historylist.append(line)
#         self.historyindex = min(self.historyindex, len(self.historylist))
#
#
# class Redirect:
#     """Map self.write to a function"""
#
#     def __init__(self, func: Callable) -> 'Redirect':
#         self.func = func
#
#     def write(self, line: str) -> None:
#         self.func(line)
#
#
# class Console(QWidget):
#     """A GUI version of code.InteractiveConsole."""
#
#     def __init__(
#             self,
#             context=locals(),  # context for interpreter
#             history: int = 20,  # max lines in history buffer
#             blockcount: int = 500  # max lines in output buffer
#     ) -> 'Console':
#         super().__init__()
#         self.setcontext(context)
#         self.buffer = []
#
#         self.content = QGridLayout(self)
#         self.content.setContentsMargins(0, 0, 0, 0)
#         self.content.setSpacing(0)
#
#         # Display for output and stderr
#         self.outdisplay = QPlainTextEdit(self)
#         self.outdisplay.setMaximumBlockCount(blockcount)
#         self.outdisplay.setReadOnly(True)
#         self.content.addWidget(self.outdisplay, 0, 0, 1, 2)
#
#         # Use color to differentiate input, output and stderr
#         self.inpfmt = self.outdisplay.currentCharFormat()
#         self.outfmt = QTextCharFormat(self.inpfmt)
#         self.outfmt.setForeground(QBrush(QColor(0, 0, 255)))
#         self.errfmt = QTextCharFormat(self.inpfmt)
#         self.errfmt.setForeground(QBrush(QColor(255, 0, 0)))
#
#         # Display input prompt left of input edit
#         self.promptdisp = QLineEdit(self)
#         self.promptdisp.setReadOnly(True)
#         self.promptdisp.setFixedWidth(15)
#         self.promptdisp.setFrame(False)
#         self.content.addWidget(self.promptdisp, 1, 0)
#         self.setprompt('> ')
#
#         # Enter commands here
#         self.inpedit = LineEdit(history=history)
#         self.inpedit.newline.connect(self.push)
#         self.inpedit.setFrame(False)
#         self.content.addWidget(self.inpedit, 1, 1)
#
#     def setcontext(self, context):
#         """Set context for interpreter"""
#         self.interp = code.InteractiveInterpreter(context)
#
#     def resetbuffer(self) -> None:
#         """Reset the input buffer."""
#         self.buffer = []
#
#     def setprompt(self, text: str):
#         self.prompt = text
#         self.promptdisp.setText(text)
#
#     def push(self, line: str) -> None:
#         """Execute entered command.  Command may span multiple lines"""
#         if line == 'clear':
#             self.inpedit.clearhistory()
#             self.outdisplay.clear()
#         else:
#             lines = line.split('\n')
#             for line in lines:
#                 if re.match('^[\>\.] ', line):
#                     line = line[2:]
#                 self.writeoutput(self.prompt + line, self.inpfmt)
#                 self.setprompt('. ')
#                 self.buffer.append(line)
#             # Built a command string from lines in the buffer
#             source = "\n".join(self.buffer)
#             more = self.interp.runsource(source, '<console>')
#             if not more:
#                 self.setprompt('> ')
#                 self.resetbuffer()
#
#     def setfont(self, font: QFont) -> None:
#         """Set font for input and display widgets.  Should be monospaced"""
#         self.outdisplay.setFont(font)
#         self.inpedit.setFont(font)
#
#     def write(self, line: str) -> None:
#         """Capture stdout and display in outdisplay"""
#         if len(line) != 1 or ord(line[0]) != 10:
#             self.writeoutput(line.rstrip(), self.outfmt)
#
#     def errorwrite(self, line: str) -> None:
#         """Capture stderr and display in outdisplay"""
#         self.writeoutput(line, self.errfmt)
#
#     def writeoutput(self, line: str, fmt: QTextCharFormat = None) -> None:
#         """Set text formatting and display line in outdisplay"""
#         if fmt is not None:
#             self.outdisplay.setCurrentCharFormat(fmt)
#         self.outdisplay.appendPlainText(line.rstrip())
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     console = Console()
#     console.setWindowTitle('Console')
#     console.setfont(QFont('Lucida Sans Typewriter', 10))
#
#     # Redirect stdout to console.write and stderr to console.errorwrite
#     redirect = Redirect(console.errorwrite)
#     with redirect_stdout(console), redirect_stderr(redirect):
#         console.show()
#         sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QGridLayout, QHBoxLayout, QVBoxLayout, \
    QSizePolicy
from PyQt5.QtCore import Qt


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moving Items Between List Widgets")
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.initUI()

        for i in range(10):
            self.listWidgetLeft.addItem('Item {0}'.format(list("ABCDEFGHIJK")[i]))

        self.updateButtonStatus()
        self.setButtonConnections()

    def initUI(self):
        subLayouts = {}

        subLayouts['LeftColumn'] = QGridLayout()
        subLayouts['RightColumn'] = QVBoxLayout()
        self.layout.addLayout(subLayouts['LeftColumn'], 1)
        self.layout.addLayout(subLayouts['RightColumn'], 1)

        self.buttons = {}
        self.buttons['>>'] = QPushButton('&>>')
        self.buttons['>'] = QPushButton('>')
        self.buttons['<'] = QPushButton('<')
        self.buttons['<<'] = QPushButton('&<<')
        self.buttons['Up'] = QPushButton('&Up')
        self.buttons['Down'] = QPushButton('&Down')

        for k in self.buttons:
            self.buttons[k].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

        """
        First Column
        """
        self.listWidgetLeft = QListWidget()
        subLayouts['LeftColumn'].addWidget(self.listWidgetLeft, 1, 0, 4, 4)

        subLayouts['LeftColumn'].setRowStretch(4, 1)
        subLayouts['LeftColumn'].addWidget(self.buttons['>>'], 1, 4, 1, 1, alignment=Qt.AlignTop)
        subLayouts['LeftColumn'].addWidget(self.buttons['<'], 2, 4, 1, 1, alignment=Qt.AlignTop)
        subLayouts['LeftColumn'].addWidget(self.buttons['>'], 3, 4, 1, 1, alignment=Qt.AlignTop)
        subLayouts['LeftColumn'].addWidget(self.buttons['<<'], 4, 4, 1, 1, alignment=Qt.AlignTop)

        """
        Second Column
        """
        self.listWidgetRight = QListWidget()

        hLayout = QHBoxLayout()
        subLayouts['RightColumn'].addLayout(hLayout)

        hLayout.addWidget(self.listWidgetRight, 4)

        vLayout = QVBoxLayout()
        hLayout.addLayout(vLayout, 1)

        vLayout.addWidget(self.buttons['Up'])
        vLayout.addWidget(self.buttons['Down'])
        vLayout.addStretch(1)

    def setButtonConnections(self):
        self.listWidgetLeft.itemSelectionChanged.connect(self.updateButtonStatus)
        self.listWidgetRight.itemSelectionChanged.connect(self.updateButtonStatus)

        self.buttons['>'].clicked.connect(self.buttonAddClicked)
        self.buttons['<'].clicked.connect(self.buttonRemoveClicked)
        self.buttons['>>'].clicked.connect(self.buttonAddAllClicked)
        self.buttons['<<'].clicked.connect(self.buttonRemoveAllClicked)

        self.buttons['Up'].clicked.connect(self.buttonUpClicked)
        self.buttons['Down'].clicked.connect(self.buttonDownClicked)

    def buttonAddClicked(self):
        row = self.listWidgetLeft.currentRow()
        rowItem = self.listWidgetLeft.takeItem(row)
        self.listWidgetRight.addItem(rowItem)

    def buttonRemoveClicked(self):
        row = self.listWidgetRight.currentRow()
        rowItem = self.listWidgetRight.takeItem(row)
        self.listWidgetLeft.addItem(rowItem)

    def buttonAddAllClicked(self):
        for i in range(self.listWidgetLeft.count()):
            self.listWidgetRight.addItem(self.listWidgetLeft.takeItem(0))

    def buttonRemoveAllClicked(self):
        for i in range(self.listWidgetRight.count()):
            self.listWidgetLeft.addItem(self.listWidgetRight.takeItem(0))

    def buttonUpClicked(self):
        rowIndex = self.listWidgetRight.currentRow()
        currentItem = self.listWidgetRight.takeItem(rowIndex)
        self.listWidgetRight.insertItem(rowIndex - 1, currentItem)
        self.listWidgetRight.setCurrentRow(rowIndex - 1)

    def buttonDownClicked(self):
        rowIndex = self.listWidgetRight.currentRow()
        currentItem = self.listWidgetRight.takeItem(rowIndex)
        self.listWidgetRight.insertItem(rowIndex + 1, currentItem)
        self.listWidgetRight.setCurrentRow(rowIndex + 1)

    def updateButtonStatus(self):
        self.buttons['Up'].setDisabled(
            not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        self.buttons['Down'].setDisabled(not bool(
            self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(
            not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
        QPushButton {
            font-size: 30px;
            width: 200px;
            height: 45px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')



















from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import QObject, pyqtSlot
from Styles import Fonts, Colors
from Finder import WorkerThread


class MainApp(QMainWindow, QWidget):
    # progressStatus = pyqtSignal('QString')
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)

        self.win = QWidget()
        self.setPalette(Colors().bgColorOne)

        self.workerThread = WorkerThread()

        self.__settings()
        self.__controls()
        self.__connectors()
        self.__layout()

    def __settings(self):
        self.setWindowTitle('Text Finder')
        self.setGeometry(200, 200, 800, 600)

        self.frameGm = self.frameGeometry()
        self.screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        self.centerPoint = QApplication.desktop().screenGeometry(self.screen).center()
        self.frameGm.moveCenter(self.centerPoint)
        self.move(self.frameGm.topLeft())



    def __controls(self):
        # LABELS
        self.title_lbl = QLabel()
        self.title_lbl.setText('Text Finder')
        self.title_lbl.setFont(Fonts().titleSize)
        self.title_lbl.setPalette(Colors().titleColor)

        self.search_lbl = QLabel()
        self.search_lbl.setText('SEARCH VALUE:')
        self.search_lbl.setFont(Fonts().defaultSize)
        self.search_lbl.setPalette(Colors().defaultColor)

        self.matchCase_lbl = QLabel('MATCH CASE')
        self.matchCase_lbl.setPalette(Colors().defaultColor)
        self.matchWord_lbl = QLabel('WORD')
        self.matchWord_lbl.setPalette(Colors().defaultColor)

        self.dirPath_lbl = QLabel()
        self.dirPath_lbl.setText('DIRECTORY:')
        self.dirPath_lbl.setFont(Fonts().defaultSize)
        self.dirPath_lbl.setPalette(Colors().defaultColor)

        self.progress_lbl = QLabel()
        self.progress_lbl.setPalette(Colors().defaultColor)

        # LINE EDIT
        self.search_fld = QLineEdit()
        self.search_fld.setStyleSheet(Colors().bgColorStyleTwo)
        self.search_fld.setFont(Fonts().defaultSize)


        self.dirPath_fld = QLineEdit()
        self.dirPath_fld.setEnabled(False)
        self.dirPath_fld.setStyleSheet(Colors().bgColorStyleTwo)
        self.dirPath_fld.setFont(Fonts().defaultSize)

        # BUTTON
        self.dirPath_btn = QPushButton()
        self.dirPath_btn.setIcon(QIcon('folder.png'))
        self.dirPath_btn.setFixedSize(30, 20)
        self.dirPath_btn.setStyleSheet(Colors().bgColorStyleOne)

        self.search_btn = QPushButton()
        self.search_btn.setText('Search')
        self.search_btn.setStyleSheet(Colors().bgColorStyleOne)

        self.clear_btn = QPushButton()
        self.clear_btn.setText('Clear Results')
        self.clear_btn.setStyleSheet(Colors().bgColorStyleOne)

        self.clearAll_btn = QPushButton()
        self.clearAll_btn.setText('Clear All')
        self.clearAll_btn.setStyleSheet(Colors().bgColorStyleOne)

        # CHECKBOX
        self.matchCase_cbx = QCheckBox()
        self.matchWord_cbx = QCheckBox()


        # TEXT BOX
        self.results_tbox = QTextEdit()
        # self.results_tbox.setReadOnly(True)
        self.results_tbox.setStyleSheet(Colors().bgColorStyleTwo)
        self.results_tbox.setFont(Fonts().defaultSize)



    def __connectors(self):
        self.dirPath_btn.clicked.connect(self.getDirectory)
        self.search_btn.clicked.connect(self.startProcess)
        self.search_fld.returnPressed.connect(self.startProcess)
        self.clearAll_btn.clicked.connect(self.clearAllFields)
        self.clear_btn.clicked.connect(self.clearTextbox)

        # self.progressStatus[str].connect(self.statusUpdate)
        self.workerThread.progressStatus.connect(self.statusUpdate)
        self.workerThread.results.connect(self.resultsText)
        # self.workerThread.error.connect(self.errorMessage)
        # self.connect(self.workerThread, PYQT_SIGNAL("finished()"), self.errorMessage)


    def __layout(self):
        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.title_lbl)
        self.titleLayout.setAlignment(Qt.AlignLeft)

        self.searchWidgetLayout = QHBoxLayout()
        self.searchWidgetLayout.addWidget(self.search_fld)
        # self.searchWidgetLayout.addSpacing(15)
        # self.searchWidgetLayout.addWidget(self.matchCase_cbx)
        # self.searchWidgetLayout.addWidget(self.matchCase_lbl)
        # self.searchWidgetLayout.addSpacing(15)
        # self.searchWidgetLayout.addWidget(self.matchWord_cbx)
        # self.searchWidgetLayout.addWidget(self.matchWord_lbl)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.search_lbl, self.searchWidgetLayout)
        self.formLayout.addRow(self.dirPath_lbl, self.dirPath_fld)
        self.formLayout.setLabelAlignment(Qt.AlignRight)

        self.dirPathBtnLayout = QVBoxLayout()
        self.dirPathBtnLayout.addWidget(self.dirPath_btn)
        self.dirPathBtnLayout.setAlignment(Qt.AlignBottom)

        self.formDirPathLayout = QHBoxLayout()
        self.formDirPathLayout.addLayout(self.formLayout)
        self.formDirPathLayout.addLayout(self.dirPathBtnLayout)


        self.searchBtnLayout = QHBoxLayout()
        self.searchBtnLayout.addWidget(self.progress_lbl)
        self.searchBtnLayout.addStretch(1)
        self.searchBtnLayout.addWidget(self.clearAll_btn)
        self.searchBtnLayout.addWidget(self.clear_btn)
        self.searchBtnLayout.addWidget(self.search_btn)
        self.searchBtnLayout.setAlignment(Qt.AlignRight)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.titleLayout)
        self.mainLayout.addLayout(self.formDirPathLayout)
        self.mainLayout.addWidget(self.results_tbox)
        self.mainLayout.addLayout(self.searchBtnLayout)

        self.win.setLayout(self.mainLayout)

        self.setCentralWidget(self.win)
        # self.setLayout(self.mainLayout)


    def getDirectory(self):
        self.dirPath = QFileDialog.getExistingDirectory(self, 'Select Folder', 'C:\\')
        self.dirPath_fld.setText(self.dirPath)

    def startProcess(self):

        self.workerThread.process(self.search_fld, self.dirPath_fld)
        self.workerThread.start()

    def clearTextbox(self):
        self.results_tbox.clear()

    def clearAllFields(self):
        self.results_tbox.clear()
        self.dirPath_fld.clear()
        self.search_fld.clear()

    @pyqtSlot('QString')
    def statusUpdate(self, status):
        # print('statusUpdateing')
        # print(status)
        self.progress_lbl.setText(status)
        if status == 'Search Complete':
            self.workerThread.terminate()

    @pyqtSlot('QString')
    def resultsText(self, text):
        # print(text)
        self.results_tbox.append(text)

    # @pyqtSlot('QString')
    # def errorMessage(self):
    #
    #     print('message for error')




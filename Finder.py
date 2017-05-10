import os, sys
from os.path import isfile
import re
from PyQt5.QtCore import *
from xlrd import open_workbook



class WorkerThread(QThread):
    progressStatus = pyqtSignal('QString')
    results = pyqtSignal('QString')
    error = pyqtSignal('QString')
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)


    def process(self, find, dirPath):

        self.find = find
        self.dirPath = dirPath

    def run(self):
        try:
            self.progressStatus.emit('Search in Progress')
            text_finder(self.results, self.dirPath, self.find)
            self.progressStatus.emit('Search Complete')
        except:
            (self.type, self.value, self.traceback) = sys.exc_info()
            sys.excepthook(self.type, self.value, self.traceback)



class text_finder(QObject):
    def __init__(self, threadObject,  rootDir, find):

        self.find = str(find.displayText())
        self.dirPath = str(rootDir.displayText())
        print('text finder function', self.find)

        self.isFound = ''

    # def read_file(self):
        for self.file in os.listdir(self.dirPath):
            self.dirFilePath = '\\'.join([self.dirPath, self.file])

            if isfile(self.dirFilePath):
                # SEARCHES ONLY EXCEL FILES
                if re.findall('\\b.xls\\b', str(self.file)) or re.findall('\\b.xlsx\\b', str(self.file)):

                    self.workbook = open_workbook(self.dirFilePath)
                    self.worksheet = self.workbook.sheet_by_index(0)

                    for self.row in range(self.worksheet.nrows):
                        self.stringList = ','.join(map(str, self.worksheet.row_values(self.row)))
                        if re.search(self.find, self.stringList, flags=re.IGNORECASE) is None:
                            pass
                        else:
                            self.results_string = self.file + ' Found ' + str(self.row + 1) + ' ' + self.stringList
                            threadObject.emit(self.results_string)

                            self.isFound = 'Yes'
                    if self.isFound == '':
                        self.results_string = self.file + ' Not Found'
                        threadObject.emit(self.results_string)

                    self.isFound = ''

                # TODO READ .PDF FILES
                elif re.findall('\\b.pdf\\b', self.file):
                    print('Find a PDF file')

                # SEARCHES ONLY TEXT FILES.  FILES CAN BE .csv, .txt, .html, .xml, .dat, raw text file
                else:
                    print('text file processing')
                    # print dirFilePath

                    with open(self.dirFilePath, 'rb', newline=None) as self.text_file:
                        self.lines = self.text_file.readlines()


                    for self.index, self.line in enumerate(self.lines):

                        if re.search(str(self.find), str(self.line), flags=re.IGNORECASE) is None:
                            pass
                        else:
                            try:
                                self.results_string = self.file + ' - ' + ' Found - Row Number: ' + str(self.index + 1) + \
                                                  ' - ' + self.line.decode('utf-8').rstrip('\r\n')
                            except:
                                self.results_string = self.file + ' - ' + ' Found - Row Number: ' + str(
                                    self.index + 1) + ' - ' + str(self.line).rstrip('\r\n')

                            threadObject.emit(self.results_string)

                            self.isFound = 'Yes'


                    if self.isFound == '':
                        self.results_string = self.file + ' - ' + ' Not Found'

                        threadObject.emit(self.results_string)

                    self.isFound = ''

        print('text finder done')
from PyQt5.QtGui import QFont, QPalette, QColor

class Fonts(QFont):
    def __init__(self):
        super(Fonts, self).__init__()

        self.titleSize = QFont("", 20, QFont.Bold)

        self.defaultSize = QFont("", 9)


class Colors(QColor, QPalette):
    def __init__(self):
        super(Colors, self).__init__()

        colorOne = '#474444'
        colorTwo = '#2b2727'

        # THESE COLORS ARE FOR QWIDGET
        self.bgColorOne = QPalette()
        self.bgColorOne.setColor(QPalette.Background, QColor(colorOne))

        # THESE COLORS ARE FOR BUTTON, TEXTBOX AND LINE WIDGETS
        self.bgColorStyleOne = "color: lightgray; background-color: {}" .format(colorOne)
        self.bgColorStyleTwo = "color: lightgray; background-color: {}" .format(colorTwo)

        self.titleColor = QPalette()
        self.titleColor.setColor(QPalette.Foreground, QColor('#ffffff'))

        self.defaultColor = QPalette()
        self.defaultColor.setColor(QPalette.Foreground, QColor('lightgrey'))
from PyQt5.QtWidgets import QTextEdit,QWidget,QVBoxLayout,QHBoxLayout,QCheckBox,QButtonGroup,QPushButton,QApplication,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import sys
import base64
import webbrowser
import os 

VERSION = 1.0

class WidgetEncoderDecoder(QWidget):
    def __init__(self,btnText="",btnFunction=lambda:print("None"),textEditReadOnly=False):
        super().__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(textEditReadOnly)

        self.B64Btn = QPushButton(text=btnText)
        self.B64Btn.clicked.connect(btnFunction)

        self.btnLayout = QVBoxLayout()
        self.btnLayout.addWidget(self.B64Btn)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.textEdit)
        self.layout.addLayout(self.btnLayout)
        self.setLayout(self.layout)

class CheckBoxGroup(QWidget):
    def __init__(self,nCheckBox=1,checkBoxStrs=[],ungroupCheckBox=[]):
        super().__init__()

        self.checkBoxs = [QCheckBox() for i in range(nCheckBox)]
        for i,s in enumerate(checkBoxStrs): self.checkBoxs[i].setText(s)

        self.layout = QVBoxLayout()
        self.checkBoxsGroup = QButtonGroup()
        self.checkBoxsGroup.setExclusive(True)

        for checkBox in self.checkBoxs: 
            self.checkBoxsGroup.addButton(checkBox)
            self.layout.addWidget(checkBox)
            
        self.checkBoxs[0].setChecked(True)

        for i in ungroupCheckBox:
            self.checkBoxsGroup.removeButton(self.checkBoxs[i])
        
        self.setLayout(self.layout)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Base64 Encoder/Decoder v{VERSION}')
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__),'icon.ico')))
        self.setGeometry(300,300,700,100)

        self.timer = QTimer(self)
        self.timer.start(100)
        self.timer.timeout.connect(self.timeout)

        self.WidgetEnc = WidgetEncoderDecoder("Encoder",self.EncodeB64)
        self.WidgetDec = WidgetEncoderDecoder("Decoder",self.DecodeB64)
        self.WidgetResult = WidgetEncoderDecoder("Copy",self.ResultCopy,True)

        self.webbrowserBtn = QPushButton("Web Open")
        self.WidgetResult.btnLayout.addWidget(self.webbrowserBtn)
        self.webbrowserBtn.clicked.connect(self.WebOpen)

        
        self.testLabel = QLabel()

        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.WidgetEnc)
        self.vLayout.addWidget(self.WidgetDec)
        self.vLayout.addWidget(self.WidgetResult)
        self.vLayout.addWidget(self.testLabel)

        self.checkBoxGroup = CheckBoxGroup(4,['Auto Cancel','Auto Encode','Auto Decode','Auto Copy'],[3])

        self.hLayout = QHBoxLayout()
        self.hLayout.addLayout(self.vLayout)
        self.hLayout.addWidget(self.checkBoxGroup)

        self.setLayout(self.hLayout)

    def EncodeB64(self):
        text = self.WidgetEnc.textEdit.toPlainText()
        encoded_text = base64.b64encode(text.encode()).decode()
        self.WidgetResult.textEdit.setText(encoded_text)

    def DecodeB64(self):
        text = self.WidgetDec.textEdit.toPlainText()
        try:
            decoded_text = base64.b64decode(text.encode()).decode()
            self.WidgetResult.textEdit.setText(decoded_text)
        except Exception as e:
            self.WidgetResult.textEdit.setText(f'Error decoding text: {e}')

    def ResultCopy(self):
        QApplication.clipboard().setText(self.WidgetResult.textEdit.toPlainText())

    def timeout(self):
        if self.checkBoxGroup.checkBoxs[1].isChecked():
            self.EncodeB64()
        elif self.checkBoxGroup.checkBoxs[2].isChecked():
            self.DecodeB64()
        elif self.checkBoxGroup.checkBoxs[3].isChecked():
            self.ResultCopy()
    
    def WebOpen(self):
        webbrowser.open(self.WidgetResult.textEdit.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    app.exec_()




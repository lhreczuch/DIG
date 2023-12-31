
class Ui_DomainLookup(object):
    def setupUi(self, DomainLookup):
        DomainLookup.setObjectName("DomainLookup")
        DomainLookup.resize(601, 422)
        self.centralwidget = QtWidgets.QWidget(DomainLookup)
        self.centralwidget.setObjectName("centralwidget")

        self.domainInput = QtWidgets.QTextEdit(self.centralwidget)
        self.domainInput.setGeometry(QtCore.QRect(10, 10, 581, 31))
        self.domainInput.setFrameShape(QtWidgets.QFrame.Box)
        self.domainInput.setFrameShadow(QtWidgets.QFrame.Raised)
        self.domainInput.setObjectName("domainInput")

        self.recordTypeBox = QtWidgets.QComboBox(self.centralwidget)
        self.recordTypeBox.setGeometry(QtCore.QRect(10, 50, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.recordTypeBox.setFont(font)
        self.recordTypeBox.setObjectName("recordTypeBox")
        self.recordTypeBox.addItem("ALL")
        self.recordTypeBox.addItem("A")
        self.recordTypeBox.addItem("MX")
        self.recordTypeBox.addItem("NS")
        self.recordTypeBox.addItem("SOA")
        self.recordTypeBox.addItem("TXT")

        self.digButton = QtWidgets.QPushButton(self.centralwidget,clicked = lambda:self.clickIt())
        self.digButton.setGeometry(QtCore.QRect(210, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.digButton.setFont(font)
        self.digButton.setObjectName("digButton")

        self.copyButton = QtWidgets.QPushButton(self.centralwidget,clicked = lambda:self.copy())
        self.copyButton.setEnabled(False)
        self.copyButton.setGeometry(QtCore.QRect(320, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.copyButton.setFont(font)
        self.copyButton.setObjectName("copyButton")

        self.whoisButton = QtWidgets.QPushButton(self.centralwidget,clicked = lambda:self.whoisIt())
        self.whoisButton.setGeometry(QtCore.QRect(430, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.whoisButton.setFont(font)
        self.whoisButton.setObjectName("whoisButton")

        
        

        self.outputField = QtWidgets.QLabel(self.centralwidget)
        self.outputField.setGeometry(QtCore.QRect(10, 100, 571, 251))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputField.sizePolicy().hasHeightForWidth())
        self.outputField.setSizePolicy(sizePolicy)
        self.outputField.setAutoFillBackground(True)
        self.outputField.setWordWrap(True)
        self.outputField.setText("")
        
        self.outputField.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.outputField.setObjectName("outputField")

        DomainLookup.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(DomainLookup)
        self.statusbar.setObjectName("statusbar")
        DomainLookup.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(DomainLookup)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 601, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuPlik = QtWidgets.QMenu(self.menuBar)
        self.menuPlik.setObjectName("menuPlik")
        DomainLookup.setMenuBar(self.menuBar)
        self.saveAs = QtWidgets.QAction(DomainLookup)
        self.saveAs.setObjectName("saveAs")
        self.menuPlik.addAction(self.saveAs)
        self.menuBar.addAction(self.menuPlik.menuAction())
        self.saveAs.triggered.connect(self.saveIt)
                               

        self.retranslateUi(DomainLookup)
        QtCore.QMetaObject.connectSlotsByName(DomainLookup)

    def retranslateUi(self, DomainLookup):
        _translate = QtCore.QCoreApplication.translate
        DomainLookup.setWindowTitle(_translate("DomainLookup", "Domain lookup"))
        self.recordTypeBox.setItemText(0, _translate("DomainLookup", "ALL"))
        self.recordTypeBox.setItemText(1, _translate("DomainLookup", "A"))
        self.recordTypeBox.setItemText(2, _translate("DomainLookup", "MX"))
        self.recordTypeBox.setItemData(3, _translate("DomainLookup", "NS"))
        self.recordTypeBox.setItemText(4, _translate("DomainLookup", "SOA"))
        self.recordTypeBox.setItemText(5, _translate("DomainLookup", "TXT"))
        self.digButton.setText(_translate("DomainLookup", "DIG"))
        self.copyButton.setText(_translate("DomainLookup", "Copy"))
        self.whoisButton.setText(_translate("DomainLookup", "WHOIS"))
        self.menuPlik.setTitle(_translate("DomainLookup", "Plik"))
        self.saveAs.setText(_translate("DomainLookup", "Zapisz wyniki jako"))

    def clickIt(self):
        self.copyButton.setEnabled(True)
        self.copyButton.setText("Copy")

        screen = self.domainInput.toPlainText()
        # delete whitespaces from adress
        screen = screen.translate({ord(c): None for c in string.whitespace})
        
        try:
            if self.recordTypeBox.currentText() == "ALL":
                recordList = ['A',"MX",'NS',"SOA","TXT"]
                data = []
                for a in recordList:
                
                    aRecordDig = dns.resolver.resolve(screen,f"{a}")
                    newData = [f"{a}: {screen}: {recordData}" for recordData in aRecordDig]
                    data.extend(newData)
                data = '\n'.join(data)
            
                self.outputField.setText(f"{data}")

            else:
                recordType = self.recordTypeBox.currentText()
                aRecordDig = dns.resolver.resolve(screen,recordType)
                data = [f"{recordType}: {screen}: {recordData}" for recordData in aRecordDig]
            
                data = '\n'.join(data)
                self.outputField.setText(f"{data}")
        except dns.resolver.NXDOMAIN:
            self.outputField.setText(f"ERROR - Can't find domain. Check if domain name is correct")
        except dns.resolver.LifetimeTimeout:
            self.outputField.setText(f"ERROR - timeout. Check if domain name is correct and your internet connection is good")
        except dns.resolver.NoAnswer:
            self.outputField.setText(f"ERROR - no answer. Check if domain name is correct and your internet connection is good")
        except:
            self.outputField.setText(f"UNKNOWN ERROR")
        
    def copy(self):

        screen = self.outputField.text()
        
        pyperclip.copy(screen)
        self.copyButton.setText("Copied !")

    def saveIt(self):
            pass
            # to do in the future
    
    def whoisIt(self):
        screen = self.domainInput.toPlainText()
        # delete whitespaces from adress
        screen = screen.translate({ord(c): None for c in string.whitespace})
        
        try:
            domain = whois.whois(screen)

            self.outputField.clear()
        
            for i,j in domain.items():
                self.outputField.setText(f"{self.outputField.text()}" + f"{i}: {j}\n")

            self.copyButton.setEnabled(True)
        except whois.parser.PywhoisError:
            self.outputField.setText(f"Cannot find domain: {screen}")

if __name__ == "__main__":
    import dns.resolver
    from PyQt5 import QtCore, QtGui, QtWidgets
    import string
    import pyperclip
    import whois
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DomainLookup = QtWidgets.QMainWindow()
    ui = Ui_DomainLookup()
    ui.setupUi(DomainLookup)
    DomainLookup.show()
    sys.exit(app.exec_())

import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QProgressBar, QDialog
from PyQt5.QtGui import QIcon
import os

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(682, 555)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        Dialog.setFont(font)

        self.instructions_lbl = QtWidgets.QLabel(Dialog)
        self.instructions_lbl.setGeometry(QtCore.QRect(100, 20, 571, 51))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.instructions_lbl.setFont(font)
        self.instructions_lbl.setScaledContents(False)
        self.instructions_lbl.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.instructions_lbl.setObjectName("instructions_lbl")

        self.openfile_button = QtWidgets.QPushButton(Dialog)
        self.openfile_button.setGeometry(QtCore.QRect(290, 90, 111, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.openfile_button.setFont(font)
        self.openfile_button.setObjectName("openfile_button")
        self.openfile_lbl = QtWidgets.QLabel(Dialog)
        self.openfile_lbl.setGeometry(QtCore.QRect(220, 160, 251, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.openfile_lbl.setFont(font)
        self.openfile_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.openfile_lbl.setObjectName("openfile_lbl")

        self.check_button = QtWidgets.QPushButton(Dialog)
        self.check_button.setGeometry(QtCore.QRect(290, 210, 111, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.check_button.setFont(font)
        self.check_button.setObjectName("check_button")
        self.check_lbl = QtWidgets.QLabel(Dialog)
        self.check_lbl.setGeometry(QtCore.QRect(130, 250, 431, 41))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.check_lbl.setFont(font)
        self.check_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.check_lbl.setObjectName("check_lbl")

        self.icon = QtWidgets.QLabel(Dialog)
        self.icon.setGeometry(QtCore.QRect(10, 20, 71, 71))
        self.icon.setText("")
        self.username = os.getlogin()
        self.icon.setPixmap(QtGui.QPixmap("C:\\Users\\{}\\Desktop\\icon.png".format(self.username)))
        self.icon.setObjectName("icon")
        self.icon.setScaledContents(True)

        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(70, 130, 551, 21))
        self.progressBar.setProperty("value", 0)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(8)
        self.progressBar.setFont(font)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setHidden(True)
        self.progressBar.setMaximum(100)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.openfile_button.clicked.connect(self.fraud_detect)
        self.check_button.clicked.connect(self.fraud_report)

    def fraud_detect(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        open_dialog = QFileDialog()

        data_name = QtWidgets.QFileDialog.getOpenFileName(open_dialog, 'Open File', "C:\\Users\\{}\\Desktop\\Untitled".format(self.username), 'CSV Files (*.csv)', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        try :
            with open(data_name[0], 'r') as data_file:
                df = pd.read_csv(data_file)

            import sklearn
            from sklearn.preprocessing import StandardScaler
            sc = StandardScaler()
            df['S_Amount'] =  sc.fit_transform(df.iloc[:,29].values.reshape(-1,1))
            data = df[['V1', 'V2', 'V3', 'V4', 'V9', 'V10', 'V11', 'V12', 'V14', 'V18', 'V19', 'S_Amount']]
            array_data = np.asarray(data)

            import pickle
            model_name = 'Finalized_model_SMOTE_RF_12F'
            with open(model_name, 'rb') as model_file:
                Pickled_LR_Model = pickle.load(model_file)
                y_pred = Pickled_LR_Model.predict(array_data)

            self.predict=[]
            self.progressBar.setHidden(False)
            self.progressBar.setEnabled(True)
            counter = 0
            for i in y_pred:
                counter = counter + 1
                progress = int(counter / y_pred.shape[0] * 100)
                self.progressBar.setValue(progress)
                if i==1:
                    self.predict.append("Fraud")
                else:
                    self.predict.append("Not Fraud")

            self.openfile_lbl.setText('Analysis has been completed')

        except :
            self.openfile_lbl.setText('Please choose another file')

    def fraud_report(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        save_dialog = QFileDialog()

        save_name = QtWidgets.QFileDialog.getSaveFileName(save_dialog, 'Save File', "C:\\Users\\{}\\Desktop\\Untitled".format(self.username), 'CSV Files (*.csv)', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        try :
            if ".csv" in save_name[0].lower():
                report_name = save_name[0]
            else:
                report_name = save_name[0]+".csv"
            pd.DataFrame(self.predict).to_csv(report_name, index=None, header=["Prediction"]) # savetxt("{}".format(report_name), self.predict, delimiter=',')
            self.check_lbl.setText("File has been saved")

        except :
            self.check_lbl.setText('Please enter a valid name')

            # save_dialog = QInputDialog() # save_name = QtWidgets.QInputDialog.getText(save_dialog, 'Save As', 'Please enter a file name with the extension .csv:')[0]'''

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Credit Card Fraud Detector"))
        self.check_button.setText(_translate("Dialog", "Save Results"))
        self.instructions_lbl.setText(_translate("Dialog", "Click \"Open File\" and choose a credit card transaction dataset for fraud\n"
"analysis, then click \"Save Results\" to save the fraud analysis report"))
        self.openfile_button.setText(_translate("Dialog", "Open File"))
        self.openfile_lbl.setText(_translate("Dialog", " "))
        self.check_lbl.setText(_translate("Dialog", " "))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QDialog, QTableView, QFileDialog, QProgressBar
from PyQt5.QtGui import QIcon
import inspect, os, sys

class PandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(PandasModel, self).__init__()
        self._data = data

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return str(self._data.values[index.row()][index.column()])

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._data.columns[section])
            #for ROW headings:
            #if orientation == QtCore.Qt.Vertical:
                #return str(self._data.index[section])

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(682, 555)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        Dialog.setFont(font)

        self.instructions_lbl = QtWidgets.QLabel(Dialog)
        self.instructions_lbl.setGeometry(QtCore.QRect(100, 20, 571, 60))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.instructions_lbl.setFont(font)
        self.instructions_lbl.setScaledContents(True)
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
        icon_path = "{}\\icon.png".format(os.getcwd())
        #for RUNNING file path:
        #__file__ same as #inspect.getfile(inspect.currentframe())
        #print(sys.argv[0]) or print(os.path.realpath(__file__)) gives #C:\Users\farah\AppData\Local\Temp\atom_script_tempfiles\3dd706a0-984c-11ea-ae39-b3f8c41a4593
        #print(os.path.dirname(os.path.abspath(__file__))) gives #C:\Users\farah\AppData\Local\Temp\atom_script_tempfiles
        self.icon.setPixmap(QtGui.QPixmap(icon_path))
        self.icon.setObjectName("icon")
        self.icon.setScaledContents(True)

        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(70, 130, 551, 21))
        self.progressBar.setProperty("value", 0) #value?
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(8)
        self.progressBar.setFont(font)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setHidden(True)
        self.progressBar.setMaximum(100)

        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(40, 300, 600, 200))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(9)
        self.tableView.setFont(font)
        #pass #hidden?
        self.tableView.setObjectName("tableView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.openfile_button.clicked.connect(self.fraud_detect)
        self.check_button.clicked.connect(self.fraud_report)

    def fraud_detect(self):

        #redundant as defined in parameter:
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #options |= QFileDialog.DontUseCustomDirectoryIcons
        open_dialog = QFileDialog()
        self.username = os.getlogin()
        data_name = QtWidgets.QFileDialog.getOpenFileName(open_dialog, 'Open File', "C:\\Users\\{}\\Desktop\\Untitled".format(self.username), 'CSV Files (*.csv)', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        try :
            with open(data_name[0], 'r') as data_file:
                df = pd.read_csv(data_file)

            import sklearn
            from sklearn.preprocessing import StandardScaler
            sc = StandardScaler()
            df['S_Amount'] =  sc.fit_transform(df.iloc[:,29].values.reshape(-1,1))
            array_data = np.asarray(df[['V1', 'V2', 'V3', 'V4', 'V9', 'V10', 'V11', 'V12', 'V14', 'V18', 'V19', 'S_Amount']])

            import pickle
            model_path = "{}\\Finalized_model_SMOTE_RF_12F".format(os.getcwd())
            with open(model_path, 'rb') as model_file:
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

            '''
            example = np.asarray([0, 1, 1, 0, 0, 0, 1, 0, 1, 1])
            self.predict=[]
            self.progressBar.setHidden(False)
            self.progressBar.setEnabled(True)
            counter = 0
            for i in example:
                counter = counter + 1
                progress = int(counter / example.shape[0] * 100)
                self.progressBar.setValue(progress)
                if i==1:
                    self.predict.append("Fraud")
                else:
                    self.predict.append("Not Fraud")
            self.openfile_lbl.setText('Analysis has been completed')
            '''

        except :
            self.openfile_lbl.setText('Please choose another file')

    def fraud_report(self):

        #redundant as defined in parameter:
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #options |= QFileDialog.DontUseCustomDirectoryIcons
        save_dialog = QFileDialog()
        save_name = QtWidgets.QFileDialog.getSaveFileName(save_dialog, 'Save File', "C:\\Users\\{}\\Desktop\\Untitled".format(self.username), 'CSV Files (*.csv)', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        #for INPUT dialog:
        #save_dialog = QInputDialog()
        #save_name = QtWidgets.QInputDialog.getText(save_dialog, 'Save File', 'Please enter a file name:')[0]
        try :
            if ".csv" in save_name[0].lower():
                report_name = save_name[0]
            else:
                report_name = save_name[0]+".csv"
            self.df = pd.DataFrame(self.predict, index=None, columns=["Prediction"])
            self.df.to_csv(report_name)
            #for TEXT method:
            #savetxt("{}".format(report_name), self.predict, delimiter=',')
            self.model = PandasModel(self.df)
            #self.model.setHorizontalHeaderLabels(["Prediction"]) gives #error
            self.tableView.setModel(self.model)
            self.check_lbl.setText("File has been saved")

        except :
            self.check_lbl.setText('Please enter a valid name')

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Credit Card Fraud Detector"))
        self.check_button.setText(_translate("Dialog", "Save Results"))
        self.instructions_lbl.setText(_translate("Dialog", "Click \"Open File\" and choose a credit card transaction dataset for\nfraud"
"analysis, then click \"Save Results\" to save and preview the fraud\nanalysis report"))
        self.openfile_button.setText(_translate("Dialog", "Open File"))
        self.openfile_lbl.setText(_translate("Dialog", " "))
        self.check_lbl.setText(_translate("Dialog", " "))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

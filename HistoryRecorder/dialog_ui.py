# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1037, 571)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sessions_label = QtWidgets.QLabel(Dialog)
        self.sessions_label.setObjectName("sessions_label")
        self.verticalLayout.addWidget(self.sessions_label)
        self.session_list_widget = QtWidgets.QListWidget(Dialog)
        self.session_list_widget.setObjectName("session_list_widget")
        self.verticalLayout.addWidget(self.session_list_widget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabs = QtWidgets.QTabWidget(Dialog)
        self.tabs.setTabsClosable(False)
        self.tabs.setObjectName("tabs")
        self.tab_time_spent = QtWidgets.QWidget()
        self.tab_time_spent.setObjectName("tab_time_spent")
        self.tabs.addTab(self.tab_time_spent, "")
        self.tab_ease = QtWidgets.QWidget()
        self.tab_ease.setObjectName("tab_ease")
        self.tabs.addTab(self.tab_ease, "")
        self.verticalLayout_2.addWidget(self.tabs)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)

        self.retranslateUi(Dialog)
        self.tabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.sessions_label.setText(_translate("Dialog", "You past sessions:"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_time_spent), _translate("Dialog", "Time spent"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_ease), _translate("Dialog", "Ease"))

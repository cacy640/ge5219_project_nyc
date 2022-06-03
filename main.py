# This is the main file to execute.
# This main.py file will generate a GUI using PyQt5 commands.
# Make sure the python interpreter is the version provided by ArcGIS Pro, which includes ArcPy license.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
import pandas as pd
import arcpy
from arcpy import env
from arcpy.sa import *
import os
import transbigdata as tbd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# embed the functions defined in other py file#
from KDens import KDensall, KDensday, KDensnight, KDensweekday, KDensweekend
from Hotspot import Hotspotall, Hotspotday, Hotspotnight, Hotspotweekday, Hotspotweekend
from BlackSpotAnalysis import blackspot

## change mapbox API accordingly
tbd.set_mapboxtoken('pk.eyJ1IjoiamlheHVhbnciLCJhIjoiY2wxaTdxb2luMGJ1YzNsbGRjZTBraGQyNyJ9.bGnZXSnnTLwjhaeDSqxf_w')
tbd.set_imgsavepath(r'C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\code\\')

from pylab import rcParams
rcParams['figure.figsize']=5,5 #set figure parameters



# change directory path: where the py files are located
dir_path = r'C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\code'

##==== ArcPy Workflow ====##
# Set environment settings
#### path of gdb file
arcpy.env.workspace = r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\database\final.gdb"
#### paths of data subsets
datapath = r"C:\Users\cacy6\National University of Singapore\GE5219 - General"
#### path of aprx, layout, and map
aprx = arcpy.mp.ArcGISProject(r"C:\Users\cacy6\OneDrive - National University of Singapore\MUP_year2\y6s2\GE5219 spatial programming\project\database\database.aprx")
lyt = aprx.listLayouts("Layout*")[0]
m = aprx.listMaps("Map")[0]
arcpy.env.overwriteOutput = True

##### Need to set Layout parameters in Arcgis pro:
##### width: 17.1cm or 690 pixel
##### height: 12.9cm or 490 pixel
##### scale is 1:400,000

# Run the following codes if it's the first time that you run this main.py
# This is to create point features and projections from the input dataset
'''
# Description: Creates a point feature class from input table
# Make the XY event layer
arcpy.management.XYTableToPoint(os.path.join(datapath,"crash_all.csv"), "Crash_all_points", "LONGITUDE", "LATITUDE")
arcpy.management.XYTableToPoint(os.path.join(datapath,"crash_day.csv"), "Crash_day_points", "LONGITUDE", "LATITUDE")
arcpy.management.XYTableToPoint(os.path.join(datapath,"crash_night.csv"), "Crash_night_points", "LONGITUDE", "LATITUDE")
arcpy.management.XYTableToPoint(os.path.join(datapath,"crash_weekday.csv"), "Crash_weekday_points", "LONGITUDE", "LATITUDE")
arcpy.management.XYTableToPoint(os.path.join(datapath,"crash_weekend.csv"), "Crash_weekend_points", "LONGITUDE", "LATITUDE")

# Project
# Description: Project all feature classes in a geodatabase
###### input data is in WGS 1984 coordinate system
input_features = "Crash_all_points"
###### output data
output_feature_class = "Crash_all_Prj"
###### create a spatial reference object for the output coordinate system
out_coordinate_system = arcpy.SpatialReference('WGS 1984 World Mercator')
###### run the tool
arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)
###### input data is in WGS 1984 coordinate system
input_features = "Crash_day_points"
###### output data
output_feature_class = "Crash_day_Prj"
###### create a spatial reference object for the output coordinate system
out_coordinate_system = arcpy.SpatialReference('WGS 1984 World Mercator')
###### run the tool
arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)
###### input data is in WGS 1984 coordinate system
input_features = "Crash_night_points"
###### output data
output_feature_class = "Crash_night_Prj"
###### create a spatial reference object for the output coordinate system
out_coordinate_system = arcpy.SpatialReference('WGS 1984 World Mercator')
###### run the tool
arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)
###### input data is in WGS 1984 coordinate system
input_features = "Crash_weekday_points"
###### output data
output_feature_class = "Crash_weekday_Prj"
###### create a spatial reference object for the output coordinate system
out_coordinate_system = arcpy.SpatialReference('WGS 1984 World Mercator')
###### run the tool
arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)
###### input data is in WGS 1984 coordinate system
input_features = "Crash_weekend_points"
###### output data
output_feature_class = "Crash_weekend_Prj"
###### create a spatial reference object for the output coordinate system
out_coordinate_system = arcpy.SpatialReference('WGS 1984 World Mercator')
###### run the tool
arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)
'''


##==== GUI codes ====##
### class of map dialog that shows a map ###
class Ui_Dialog(object):
    """
    This is a class for the dialog showing the map output.
    """
    def setupUi(self, Dialog):
        """
        This is a function to setup the dialog ui.

        :param Dialog: The type of ui defined.
        :return: A dialog ui with a text label showing current analysis, and a pixmap.
        """
        Dialog.setObjectName("Dialog")
        Dialog.resize(895, 727)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 670, 521, 31))
        self.label.setObjectName("label")

        #qpixmap = QPixmap(os.path.join(dir_path, "images.jpg"))
        self.label_2 = QtWidgets.QLabel(Dialog)
        #self.label_2.setPixmap(qpixmap)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 851, 631))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">TextLabel</span></p></body></html>"))
        #self.label_2.setText(_translate("Dialog", "TextLabel"))

### class of Message Dialog that shows the text results
class Ui_Dialog3(object):
    """
    This is a class for the dialog showing the text message output.
    """
    def setupUi(self, Dialog):
        """
        This is a function to setup the dialog ui.

        :param Dialog: The type of ui defined.
        :return: A dialog ui with a text label showing current analysis, and a string showing the message result.
        """
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 270)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 40, 961, 31))
        self.label.setObjectName("label")

        self.Moran_label = QtWidgets.QLabel(Dialog)
        self.Moran_label.setGeometry(QtCore.QRect(20, 130, 951, 51))
        self.Moran_label.setObjectName("label2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt, font-weight:600;\">TextLabel</span></p></body></html>"))
        self.Moran_label.setText(_translate("Dialog", "TextLabel"))


### class main window ui ###
class Ui_MainWindow(object):
    """
    This is the class of the ui main window.
    """
    def setupUi(self, MainWindow):
        """
        This is a function to set up main window ui.

        :param MainWindow: The type of MainWindow defined.
        :return: The main window of this gui
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(809, 608)

        ## load map dialog 1
        self.mapdialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.mapdialog)

        ## load message dialog
        self.messagedialog = QtWidgets.QDialog()
        self.ui3 = Ui_Dialog3()
        self.ui3.setupUi(self.messagedialog)

        ## load map dialog 2
        #self.mapdialog2 = QtWidgets.QDialog()
        #self.ui2 = Ui_Dialog2()
        #self.ui2.setupUi(self.mapdialog2)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 781, 541))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # browse csv file
        self.label_input = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_input.setObjectName("label_input")
        self.gridLayout.addWidget(self.label_input, 0, 0, 1, 1)
        self.browsefile = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.browsefile.setObjectName("browsefile")
        self.gridLayout.addWidget(self.browsefile, 0, 2, 1, 1)
        self.browsefile.clicked.connect(self.browse_csv)
        ### show file path
        self.filename = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.filename.setObjectName("filename")
        self.gridLayout.addWidget(self.filename, 0, 1, 1, 1)

        # browse shp
        self.label_shp = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_shp.setObjectName("label_shp")
        self.gridLayout.addWidget(self.label_shp, 1, 0, 1, 1)
        self.browseshp = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.browseshp.setObjectName("browseshp")
        self.gridLayout.addWidget(self.browseshp, 1, 2, 1, 1)
        self.browseshp.clicked.connect(self.browse_shp)
        ###show shp path
        self.filename_shp = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.filename_shp.setObjectName("filename_shp")
        self.gridLayout.addWidget(self.filename_shp, 1, 1, 1, 1)
        # set env
        arcpy.env.extent = self.filename_shp.text()
        #mask = self.filename_shp.text()

        # browse wd
        self.label_wd = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_wd.setObjectName("label_wd")
        self.gridLayout.addWidget(self.label_wd, 4, 0, 1, 1)
        self.browsewd = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.browsewd.setObjectName("browsewd")
        self.gridLayout.addWidget(self.browsewd, 4, 2, 1, 1)
        self.browsewd.clicked.connect(self.browse_wd)
        ###show wd path
        self.filename_wd = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.filename_wd.setObjectName("filename_wd")
        self.gridLayout.addWidget(self.filename_wd, 4, 1, 1, 1)
        #output_path = self.filename_wd.text()

        # data preview
        self.datapreview = QtWidgets.QLabel(self.gridLayoutWidget)
        self.datapreview.setObjectName("datapreview")
        self.gridLayout.addWidget(self.datapreview, 2, 2, 1, 1)
        self.tableView = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 3, 0, 1, 3)

        # select type of analysis
        ## radiobutton: 1-spatial autocorrelation, 2-blackspot, 3-hotspot, 4-kde
        self.label_analysis = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_analysis.setObjectName("label_analysis")
        self.gridLayout.addWidget(self.label_analysis, 6, 0, 1, 1)

        ###rb1 - spatial autocorrelation
        self.radioButton = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 6, 1, 1, 1)

        ##rb3 - hotspot
        self.radioButton_3 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout.addWidget(self.radioButton_3, 7, 1, 1, 1)

        # rb4 - kde
        self.radioButton_4 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout.addWidget(self.radioButton_4, 8, 1, 1, 1)

        # rb2 - blackspot
        self.radioButton_2 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 9, 1, 1, 1)

        # time period combobox
        self.label_time = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_time.setObjectName("label_time")
        self.gridLayout.addWidget(self.label_time, 10, 0, 1, 1)

        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("All")
        self.comboBox.addItem("Day")
        self.comboBox.addItem("Night")
        self.comboBox.addItem("Weekday")
        self.comboBox.addItem("Weekend")
        self.gridLayout.addWidget(self.comboBox, 10, 1, 1, 1)

        # run button
        self.runbtn = QtWidgets.QPushButton(self.gridLayoutWidget, clicked=lambda: self.run_analysis()) #once clicked, run the function run_analysis()
        self.runbtn.setObjectName("runbtn")
        self.gridLayout.addWidget(self.runbtn, 11, 2, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # browse csv input function
    def browse_csv(self):
        """
        This is a function to browse csv file.

        :return: A pandas dataframe to preview the dataset, and the path of csv file.
        """
        fname = QFileDialog.getOpenFileName(None, "Open CSV File",
                                            dir_path,
                                            'CSV Files (*.csv)')
        self.filename.setText(fname[0])

        # load csv and preview
        df = pd.read_csv(fname[0])
        df = df.head(500)  # preview head 500 rows, can modify
        self.tableView.setRowCount(df.shape[0])
        self.tableView.setColumnCount(df.shape[1])
        self.tableView.setHorizontalHeaderLabels(df.columns)

        # returns pandas array object
        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                # if isinstance(value, (float, int)):
                #   value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.tableView.setItem(row[0], col_index, tableItem)

    # browse shp function
    def browse_shp(self):
        """
        This is a function to browse shapefile.

        :return: The path of shapefile.
        """
        shpname = QFileDialog.getOpenFileName(None, "Open SHP File",
                                              dir_path,
                                              'Shapefile (*.shp)')
        self.filename_shp.setText(shpname[0])

    # browse working directory function
    def browse_wd(self):
        """
        This is a function to set working directory.

        :return: The path of working directory pointed by the user.
        """
        wdname = QFileDialog.getExistingDirectory(None, "Set Working Directory",
                                                  dir_path)
        self.filename_wd.setText(wdname)


    # def run_analysis function
    def run_analysis(self):
        """
        This is the main function to perform the analysis that the user selected.

        :return: 1) The message output of spatial autocorrelation analysis;
                2) The map output of hotspot analysis, or kernel density estimation, ot black spot analysis.
        """

        # set global parameters used in this function
        comma = ', '
        in_path = arcpy.env.workspace
        output_path = os.path.normpath(self.filename_wd.text())
        mask = os.path.normpath(self.filename_shp.text())

        ### global moran's i
        if self.radioButton.isChecked():  #if select spatial autocorrelation
            passtext = self.radioButton.text()
            if self.comboBox.currentText() == "All":  #time =All
                out_all = arcpy.SpatialAutocorrelation_stats("Crash_all_Prj", "injured_killed", "GENERATE_REPORT",
                                                   "INVERSE_DISTANCE", "EUCLIDEAN DISTANCE", "ROW")
                print("Global Moran's of crash all finished")
                message = "Global Moran's I index value is {}; The z-score is {}; The p-value is {}; The file path of the HTML report file is {}".format(
                    out_all[0], out_all[1], out_all[2], out_all[3])
                print(message)
                self.ui3.label.setText(("The result of " + passtext + comma + self.comboBox.currentText())) #show the analysis performed
                self.ui3.Moran_label.setText(".".join(message.split(";")[0:3])+".")
                self.messagedialog.show()
            elif self.comboBox.currentText() == "Day":  #time=Day
                out_day = arcpy.SpatialAutocorrelation_stats("Crash_day_Prj", "injured_killed", "GENERATE_REPORT",
                                                   "INVERSE_DISTANCE", "EUCLIDEAN DISTANCE", "ROW")
                print("Global Moran's of crash day finished")
                message = "Global Moran's I index value is {}; The z-score is {}; The p-value is {}; The file path of the HTML report file is {}".format(
                    out_day[0], out_day[1], out_day[2], out_day[3])
                print(message)
                self.ui3.label.setText(("The result of " + passtext + comma + self.comboBox.currentText()))
                self.ui3.Moran_label.setText(".".join(message.split(";")[0:3])+".")
                self.messagedialog.show()
            elif self.comboBox.currentText() == "Night":  #time=Night
                out_night = arcpy.SpatialAutocorrelation_stats("Crash_night_Prj", "injured_killed", "GENERATE_REPORT",
                                                   "INVERSE_DISTANCE", "EUCLIDEAN DISTANCE", "ROW")
                print("Global Moran's of crash night finished")
                message = "Global Moran's I index value is {}; The z-score is {}; The p-value is {}; The file path of the HTML report file is {}".format(
                    out_night[0], out_night[1], out_night[2], out_night[3])
                print(message)
                self.ui3.label.setText(("The result of " + passtext + comma + self.comboBox.currentText()))
                self.ui3.Moran_label.setText(".".join(message.split(";")[0:3])+".")
                self.messagedialog.show()
            elif self.comboBox.currentText() == "Weekday": #time=Weekday
                out_weekday = arcpy.SpatialAutocorrelation_stats("Crash_weekday_Prj", "injured_killed", "GENERATE_REPORT",
                                                   "INVERSE_DISTANCE", "EUCLIDEAN DISTANCE", "ROW")
                print("Global Moran's of crash weekday finished")
                message = "Global Moran's I index value is {}; The z-score is {}; The p-value is {}; The file path of the HTML report file is {}".format(
                    out_weekday[0], out_weekday[1], out_weekday[2], out_weekday[3])
                print(message)
                self.ui3.label.setText(("The result of " + passtext + comma + self.comboBox.currentText()))
                self.ui3.Moran_label.setText(".".join(message.split(";")[0:3])+".")
                self.messagedialog.show()
            elif self.comboBox.currentText() == "Weekend":  #time=Weekend
                out_weekend = arcpy.SpatialAutocorrelation_stats("Crash_weekend_Prj", "injured_killed", "GENERATE_REPORT",
                                                   "INVERSE_DISTANCE", "EUCLIDEAN DISTANCE", "ROW")
                print("Global Moran's of crash weekend finished")
                message = "The Moran's I index value is {}; The z-score is {}; The p-value is {}; The file path of the HTML report file is {}".format(
                    out_weekend[0], out_weekend[1], out_weekend[2], out_weekend[3])
                print(message)
                self.ui3.label.setText(("The result of " + passtext + comma + self.comboBox.currentText()))
                self.ui3.Moran_label.setText(".".join(message.split(";")[0:3])+".")
                self.messagedialog.show()


        ### hotspot analysis
        elif self.radioButton_3.isChecked():  #if hotspot analysis is selected
            passtext = self.radioButton_3.text()
            if self.comboBox.currentText() == "All":
                Hotspotall(os.path.join(datapath, "crash_all.csv"), mask, in_path, output_path, m, aprx)
                print("Hotspot Analysis of crash all success")
                qpixmap = QPixmap(os.path.join(output_path, "hotspotall.jpg"))
                # change map parameters
                self.ui.label.setText(passtext + comma + self.comboBox.currentText()) #show analysis performed
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()
            elif self.comboBox.currentText() == "Day":
                Hotspotday(os.path.join(datapath, "crash_day.csv"), mask, in_path, output_path, m, aprx)
                print("Hotspot Analysis of crash day success")
                qpixmap = QPixmap(os.path.join(output_path, "hotspotday.jpg"))
                # change map parameters
                self.ui.label.setText(passtext + comma + self.comboBox.currentText())
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()
            elif self.comboBox.currentText() == "Night":
                Hotspotnight(os.path.join(datapath, "crash_night.csv"), mask, in_path, output_path, m, aprx)
                print("Hotspot Analysis of crash night success")
                qpixmap = QPixmap(os.path.join(output_path, "hotspotnight.jpg"))
                # change map parameters
                self.ui.label.setText(passtext + comma + self.comboBox.currentText())
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()
            elif self.comboBox.currentText() == "Weekday":
                Hotspotweekday(os.path.join(datapath, "crash_weekday.csv"), mask, in_path, output_path, m, aprx)
                print("Hotspot analysis of crash of crash weekday success")
                qpixmap = QPixmap(os.path.join(output_path, "hotspotweekday.jpg"))
                # change map parameters
                self.ui.label.setText(passtext + comma + self.comboBox.currentText())
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()
            elif self.comboBox.currentText() == "Weekend":
                Hotspotweekend(os.path.join(datapath, "crash_weekend.csv"), mask, in_path, output_path, m, aprx)
                print("Hotspot analysis of crash of weekend success")
                qpixmap = QPixmap(os.path.join(output_path, "hotspotweekend.jpg"))
                # change map parameters
                self.ui.label.setText(passtext + comma + self.comboBox.currentText())
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()


        ### kernel density
        elif self.radioButton_4.isChecked():  #if kernel density is selected
            passtext = self.radioButton_4.text()
            if self.comboBox.currentText() == "All":
                KDensall(os.path.join(datapath, "crash_all.csv"), mask, in_path, output_path, m, aprx)
                print("Kernel Density Estimation of crash all success")
                qpixmap = QPixmap(os.path.join(output_path, "all.jpg"))  ### path of output map
                # change map parameters
                self.ui.label.setText(passtext + comma + self.comboBox.currentText()) #show analysis performed
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()
            elif self.comboBox.currentText() == "Day":
                KDensday(os.path.join(datapath, "crash_day.csv"), mask, in_path, output_path, m, aprx)
                print("Kernel Density Estimation of crash day success")
                qpixmap = QPixmap(os.path.join(output_path, "day.jpg"))

                self.ui.label.setText(passtext + comma + self.comboBox.currentText())
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()
            elif self.comboBox.currentText() == "Night":
                KDensnight(os.path.join(datapath, "crash_night.csv"), mask, in_path, output_path, m, aprx)
                print("Kernel Density Estimation of crash night success")
                qpixmap = QPixmap(os.path.join(output_path, "night.jpg"))

                self.ui.label.setText(passtext + comma + self.comboBox.currentText())
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()
            elif self.comboBox.currentText() == "Weekday":
                KDensweekday(os.path.join(datapath, "crash_weekday.csv"), mask, in_path, output_path, m, aprx)
                print("Kernel Density Estimation of crash weekday success")
                qpixmap = QPixmap(os.path.join(output_path, "weekday.jpg"))

                self.ui.label.setText(passtext + comma + self.comboBox.currentText())
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()
            elif self.comboBox.currentText() == "Weekend":
                KDensweekend(os.path.join(datapath, "crash_weekend.csv"), mask, in_path, output_path, m, aprx)
                print("Kernel Density Estimation of crash weekend success")
                qpixmap = QPixmap(os.path.join(output_path, "weekend.jpg"))

                self.ui.label.setText(passtext + comma + self.comboBox.currentText())
                self.ui.label_2.setPixmap(qpixmap)
                self.mapdialog.show()


        ### blackspot analysis
        elif self.radioButton_2.isChecked(): #if blackspot analysis is performed
            passtext = self.radioButton_2.text()
            bsfile = os.path.join(datapath, "3yearsdata.csv")
            blackspot(bsfile, in_path, output_path)
            print("Blackspot analysis success")
            qpixmap = QPixmap(os.path.join(output_path, "blackspot.png"))

            self.ui.label.setText(passtext)
            self.ui.label_2.setPixmap(qpixmap)
            self.mapdialog.show()


    # set UI translate parameters
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton_4.setText(_translate("MainWindow", "Kernel Density"))
        self.radioButton_3.setText(_translate("MainWindow", "Hotspot Analysis"))
        self.browsefile.setText(_translate("MainWindow", "Browse"))
        self.browsewd.setText(_translate("MainWindow", "Browse"))
        self.radioButton_2.setText(_translate("MainWindow", "Black Spot Analysis"))
        self.label_time.setText(_translate("MainWindow",
                                           "<html><head/><body><p><span style=\" font-weight:600;\">Time period</span></p></body></html>"))
        self.comboBox.setItemText(0, _translate("MainWindow", "All"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Day"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Night"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Weekday"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Weekend"))
        self.label_input.setText(_translate("MainWindow", "Inout csv file"))
        self.datapreview.setText(
            _translate("MainWindow", "<html><head/><body><p align=\"right\">Data Preview</p></body></html>"))
        self.browseshp.setText(_translate("MainWindow", "Browse"))
        self.label_shp.setText(_translate("MainWindow", "Input Shapefile"))
        self.label_analysis.setText(_translate("MainWindow",
                                               "<html><head/><body><p><span style=\" font-weight:600;\">Type of Analysis</span></p></body></html>"))
        self.radioButton.setText(_translate("MainWindow", "Spatial Autocorrelation"))
        self.runbtn.setText(_translate("MainWindow", "Run"))
        self.label_wd.setText(_translate("MainWindow", "Working directory"))




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

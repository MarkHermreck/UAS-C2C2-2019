from __future__ import unicode_literals
import sys
import os
import csv
import numbers
import re
from matplotlib.backends import qt_compat

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtWidgets, QtCore
else:
    from PyQt5 import QtWidgets, QtCore
    from PyQt5.QtWidgets import QListWidget, QLineEdit, QLabel, QPushButton, QCheckBox, QInputDialog
    from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import communication

#progname = os.path.basename(sys.argv[0])
progname = "GPS Coordinate Entry UI"
progversion = "0.1"

# format is [[x], [y], [x2], [y2], [x3], [y3]]
dataPoints = [[], [], [], [], [], []]

#com = communication.Communication(sys.argv[1], float(sys.argv[2]))


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(1000)
        cid = self.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        aw.setFocus()

        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

        # rounding. Rounds to 0 decimal places, but this can be changed
        #it has been
        roundedX = round(event.xdata, 8)
        roundedY = round(event.ydata, 8)
        roundedAlt = round(float(aw.altitudeEdit.text()), 8)

        if roundedX > 250:
            roundedX = 250
        elif roundedX < -250:
            roundedX = -250

        if roundedY > 250:
            roundedY = 250
        elif roundedY < -250:
            roundedY = -250

        if roundedAlt < 1:
            roundedAlt = 1

        self.addPoint(roundedX, roundedY, roundedAlt)

    def addPoint(self, xPoint, yPoint, altitude):
        lenCoords = len(dataPoints[0])
        coordExists = False

        for i in range(0, lenCoords):
            if xPoint == dataPoints[0][i] and yPoint == dataPoints[1][i] and altitude == dataPoints[2][i]:
                coordExists = True

        # Checks if the current coordinate exists (including altitude). Currently disabled, but if we want it back uncomment the next line and fix the indentation accordingly
        # if coordExists == False:
        dataPoints[0].append(xPoint)
        dataPoints[1].append(yPoint)
        dataPoints[2].append(altitude)
        print("added a point at (" + str(dataPoints[0][lenCoords]) + ", " + str(
            dataPoints[1][lenCoords]) + ")  Alt: " + str(dataPoints[2][lenCoords]))
        aw.list.addItem(str(lenCoords + 1) + ".  " + "(" + str(dataPoints[0][lenCoords]) + ", " + str(
            dataPoints[1][lenCoords]) + ")  Alt: " + str(dataPoints[2][lenCoords]))

        self.axes.cla()
        self.axes.plot(dataPoints[0], dataPoints[1], c='c', linestyle='dashed', marker='o')
        self.dc.axes.set_xlabel('Longitude in Decimal Degrees (m)')
        self.dc.axes.set_ylabel('Latitude in Decimal Degrees (m)')
        self.dc.axes.set_title('ISU & Ground Station Locations Entry')
        self.axes.set_xlim(-270, 270)
        self.axes.set_ylim(-270, 270)

        # Annotation happens here, see what the rest of the group thinks

        # if(altitudeCheckBox

        for i in range(0, len(dataPoints[0])):
            if aw.altitudeCheckBox.isChecked():
                self.axes.annotate(str(dataPoints[2][i]) + ' m', (dataPoints[0][i] - 10, dataPoints[1][i] + 20))

            self.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3 * len(str(i + 1)), dataPoints[1][i] - 8), size=8)

        self.draw()

    def removePoint(self, indexToRemove):
        del dataPoints[0][indexToRemove]
        del dataPoints[1][indexToRemove]
        del dataPoints[2][indexToRemove]
        self.axes.cla()
        self.axes.plot(dataPoints[0], dataPoints[1], c='c', linestyle='dashed', marker='o')
        self.dc.axes.set_xlabel('Longitude in Decimal Degrees (m)')
        self.dc.axes.set_ylabel('Latitude in Decimal Degrees (m)')
        self.dc.axes.set_title('ISU & Ground Station Locations Entry')
        self.axes.set_xlim(-270, 270)
        self.axes.set_ylim(-270, 270)

        aw.list.clear()

        for i in range(0, len(dataPoints[0])):
            if aw.altitudeCheckBox.isChecked():
                self.axes.annotate(str(dataPoints[2][i]) + ' m', (dataPoints[0][i] - 10, dataPoints[1][i] + 20))

            self.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3 * len(str(i + 1)), dataPoints[1][i] - 8), size=8)

            aw.list.addItem(
                str(i + 1) + ".  " + "(" + str(dataPoints[0][i]) + ", " + str(dataPoints[1][i]) + ")  Alt: " + str(
                    dataPoints[2][i]))

        self.draw()

    def compute_initial_figure(self):
        self.axes.plot(dataPoints[0], dataPoints[1], c='c', linestyle='dashed', marker='o')
        # self.axes.plot(exampleData[0],exampleData[1],c='b',marker='o')
        self.axes.set_xlim(-270, 270)
        self.axes.set_ylim(-270, 270)
        self.axes.set_xlabel('Relative Position, West/East (m)')
        self.axes.set_ylabel('Relative Position, South/North (m)')
        self.axes.set_title('Flight Path Definition')


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QGridLayout(self.main_widget)
        # sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.dc = MyDynamicMplCanvas(self.main_widget, width=10, height=8, dpi=100)
        self.list = QListWidget(self)
        self.list.setFont(QFont('Courier'))
        self.list.doubleClicked.connect(self.listItemDoubleClicked)
        # l.addWidget(sc)
        self.xEdit = QLineEdit()
        self.yEdit = QLineEdit()
        self.xEdit2 = QLineEdit()
        self.yEdit2 = QLineEdit()
        self.xEdit3 = QLineEdit()
        self.yEdit3 = QLineEdit()
        #self.altitudeEdit = QLineEdit()

        self.xEdit.setText('0')
        self.yEdit.setText('0')
        self.xEdit2.setText('0')
        self.yEdit2.setText('0')
        self.xEdit3.setText('0')
        self.yEdit3.setText('0')
        #self.altitudeEdit.setText('5')

        self.xLabel = QLabel('ISU #1 Longitude')
        self.yLabel = QLabel('ISU #1 Latitude')
        self.xLabel2 = QLabel('ISU #2 Longitude')
        self.yLabel2 = QLabel('ISU #2 Latitude')
        self.xLabel3 = QLabel('Ground Station Longitude')
        self.yLabel3 = QLabel('Ground Station Latitude')
        #self.altitudeLabel = QLabel('Altitude in Feet')
        self.gpsLabel = QLabel('      Use GPS as position')

        self.addButton = QPushButton("Add Point")
        self.addButton.clicked.connect(self.addPointButtonClicked)
        self.startButton = QPushButton("Begin")
        self.startButton.clicked.connect(self.beginButtonClicked)
        self.loadCSVButton = QPushButton("Load from CSV")
        self.loadCSVButton.clicked.connect(self.loadCSVButtonClicked)
        self.gpsCheckBox = QCheckBox()

        self.altitudeCheckBox = QCheckBox()
        self.altitudeCheckBoxLabel = QLabel('      Show altitude annotations')
        self.altitudeCheckBox.stateChanged.connect(self.altitudeCheckBoxClicked)
        self.altitudeCheckBox.toggle()

        l.addWidget(self.xLabel, 0, 0, 1, 1)
        l.addWidget(self.yLabel, 0, 1, 1, 1)
        l.addWidget(self.xLabel2, 0, 2, 1, 1)
        l.addWidget(self.yLabel2, 0, 3, 1, 1)

        l.addWidget(self.xLabel3, 0, 4, 1, 1)
        l.addWidget(self.yLabel3, 0, 5, 1, 1)
        #l.addWidget(self.altitudeLabel, 0, 6, 1, 1)
        l.addWidget(self.gpsLabel, 1, 8, 1, 1)

        l.addWidget(self.xEdit, 1, 0, 1, 1)
        l.addWidget(self.yEdit, 1, 1, 1, 1)
        l.addWidget(self.xEdit2, 1, 2, 1, 1)
        l.addWidget(self.yEdit2, 1, 3, 1, 1)
        l.addWidget(self.xEdit3, 1, 4, 1, 1)
        l.addWidget(self.yEdit3, 1, 5, 1, 1)
        #l.addWidget(self.altitudeEdit, 1, 6, 1, 1)
        l.addWidget(self.addButton, 1, 7, 1, 1)
        l.addWidget(self.gpsCheckBox, 1, 8, 1, 1)
        l.addWidget(self.startButton, 3, 8, 1, 1)
        l.addWidget(self.loadCSVButton, 3, 7, 1, 1)
        #l.addWidget(self.altitudeCheckBoxLabel, 0, 8, 1, 1)
        #l.addWidget(self.altitudeCheckBox, 0, 8, 1, 1)

        l.addWidget(self.dc, 2, 0, 1, 7)
        l.addWidget(self.list, 2, 7, 1, 2)

        # self.addButton.clicked.connect(dc.addPoint(str(self.xEdit.text()), str(self.yEdit.text()), str(self.altitudeEdit.text())))

        lenCoords = len(dataPoints[0])
        for i in range(0, lenCoords):
            self.list.addItem(
                str(i + 1) + ".  " + "(" + str(dataPoints[0][i]) + ", " + str(dataPoints[1][i]) + ")  Alt: " + str(
                    dataPoints[2][i]))

        # lenCoords = len(exampleData[0])
        # for i in range(0,lenCoords):
        # self.list.addItem("(" + str(exampleData[0][i]) + ", " + str(exampleData[1][i]) + ")  Altitude: " + str(exampleData[2][i]) + "   Temp: " + str(exampleData[3][i]) + " °C")
        #	self.list.addItem('{:16s} {:18s} {:18s}'.format("(" + str(exampleData[0][i]) + ", " + str(exampleData[1][i]) + ")", "Altitude: " + str(exampleData[2][i]), "Temp: " + str(exampleData[3][i]) + " °C"))

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    # def buttonClicked(self, dc):
    #	dc.addPoint(self, str(self.xEdit.text()), str(self.yEdit.text()), str(self.altitudeEdit.text()))

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def altitudeCheckBoxClicked(self):
        self.dc.axes.cla()
        self.dc.axes.plot(dataPoints[0], dataPoints[1], c='c', linestyle='dashed', marker='o')
        self.dc.axes.set_xlabel('Longitude in Decimal Degrees')
        self.dc.axes.set_ylabel('Latitude in Decimal Degrees')
        self.dc.axes.set_title('ISU & Ground Station Locations')
        self.dc.axes.set_xlim(-270, 270)
        self.dc.axes.set_ylim(-270, 270)
        # tuscaloosa GPS coords roughly
        # 33.209561 lat, 33 deg 12 min 34.412 sec N
        # -87.567526 long, 87 deg 34 min 3.092 sec W

        if self.altitudeCheckBox.isChecked():

            for i in range(0, len(dataPoints[0])):
                self.dc.axes.annotate(str(dataPoints[2][i]) + ' m', (dataPoints[0][i] - 10, dataPoints[1][i] + 20))

                self.dc.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3 * len(str(i + 1)), dataPoints[1][i] - 8),
                                      size=8)

            self.dc.draw()
        else:
            for i in range(0, len(dataPoints[0])):
                self.dc.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3 * len(str(i + 1)), dataPoints[1][i] - 8),
                                      size=8)

            self.dc.draw()

    def listItemDoubleClicked(self):
        editedRow = self.list.currentRow()
        s = str(dataPoints[0][editedRow]) + ', ' + str(dataPoints[1][editedRow]) + ', ' + str(dataPoints[2][editedRow])
        t, okPressed = QInputDialog.getText(self, "Edit waypoint", "Format: X, Y, Alt", QLineEdit.Normal, s)
        if okPressed:
            if re.match('[-+]?[0-9]*\.?[0-9]+, [-+]?[0-9]*\.?[0-9]+, [-+]?[0-9]*\.?[0-9]+', t):
                editX, editY, editAlt = t.split(', ')
                dataPoints[0][editedRow] = float(editX)
                dataPoints[1][editedRow] = float(editY)
                dataPoints[2][editedRow] = float(editAlt)
                self.list.currentItem().setText(
                    str(editedRow + 1) + ".  " + "(" + str(dataPoints[0][editedRow]) + ", " + str(
                        dataPoints[1][editedRow]) + ")  Alt: " + str(dataPoints[2][editedRow]))
            else:
                QtWidgets.QMessageBox.about(self, "Unsaved edit", "Invalid format")

    def addPointButtonClicked(self):
        lenCoords = len(dataPoints[0])

        newX = self.xEdit.text()
        newY = self.yEdit.text()
        newX2 = self.xEdit2.text()
        newY2 = self.yEdit2.text()
        newX3 = self.xEdit3.text()
        newY3 = self.yEdit3.text()
        #newAlt = self.altitudeEdit.text()

        if isinstance(float(newX), numbers.Number) and isinstance(float(newY), numbers.Number) and isinstance(
                float(newX2), numbers.Number) and isinstance(float(newY2), numbers.Number) and isinstance(
                float(newX3), numbers.Number) and isinstance(float(newY3), numbers.Number):
            dataPoints[0].append(float(newX))
            dataPoints[1].append(float(newY))
            #print("reached here")
            dataPoints[2].append(float(newX2))
            dataPoints[3].append(float(newY2))
            #print("reached here")
            dataPoints[4].append(float(newX3))
            dataPoints[5].append(float(newY3))
            #dataPoints[2].append(float(newAlt))

            print("added a point at (" + str(dataPoints[0][lenCoords]) + ", " + str(
                dataPoints[1][lenCoords]) + ")  " )
            print("added a point at (" + str(dataPoints[2][lenCoords]) + ", " + str(
                dataPoints[3][lenCoords]) + ")  ")
            print("added a point at (" + str(dataPoints[4][lenCoords]) + ", " + str(
                dataPoints[5][lenCoords]) + ")  ")
            self.list.addItem("ISU #1: " + "(" + str(dataPoints[0][lenCoords]) + ", " + str(
                dataPoints[1][lenCoords]) + ") ")
            self.list.addItem("ISU #2: " + "(" + str(dataPoints[2][lenCoords]) + ", " + str(
                dataPoints[3][lenCoords]) + ") ")
            self.list.addItem("Ground Station: "+ "(" + str(dataPoints[4][lenCoords]) + ", " + str(
                dataPoints[5][lenCoords]) + ") ")

            self.dc.axes.cla()
            self.dc.axes.plot(dataPoints[0], dataPoints[1], c='c', linestyle='dashed', marker='o')
            self.dc.axes.plot(dataPoints[2], dataPoints[3], c='c', linestyle='dashed', marker='o')
            self.dc.axes.plot(dataPoints[4], dataPoints[5], c='c', linestyle='dashed', marker='o')
            self.dc.axes.plot(dataPoints[0], dataPoints[1], c='c', linestyle='dashed', marker='o')
            self.dc.axes.set_xlabel('Longitude in Decimal Degrees')
            self.dc.axes.set_ylabel('Latitude in Decimal Degrees')
            self.dc.axes.set_title('ISU & Ground Station Locations')
            self.dc.axes.set_xlim(-270, 270)
            self.dc.axes.set_ylim(-270, 270)

            if self.altitudeCheckBox.isChecked():

                for i in range(0, len(dataPoints[0])):
                    self.dc.axes.annotate(str(dataPoints[2][i]) + ' m', (dataPoints[0][i] - 10, dataPoints[1][i] + 20))

                    self.dc.axes.annotate(str(i + 1),
                                          (dataPoints[0][i] - 2.5 - 3 * len(str(i + 1)), dataPoints[1][i] - 8), size=8)

            else:
                for i in range(0, len(dataPoints[0])):
                    self.dc.axes.annotate(str(i + 1),
                                          (dataPoints[0][i] - 2.5 - 3 * len(str(i + 1)), dataPoints[1][i] - 8), size=8)

            self.dc.draw()

    def beginButtonClicked(self):

        msg = QtWidgets.QMessageBox()
        reply = msg.question(self, 'Begin Flight?',
                             "Flight path will be saved to flightPath.csv. Are you sure you want to begin flight?",
                             QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            with open('flightPath.csv', 'w') as csvfile:
                fieldnames = ['x', 'y']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for i in range(0, 3):

                    writer.writerow({'x': str(dataPoints[2*i]), 'y': str(dataPoints[2*i+1])})

            dictList = []
            for i in range(0, 3):
                currentDict = {'x': dataPoints[2*i], 'y': dataPoints[2*i+1]}
                dictList.append(currentDict)

            #uncomment below when ready to start testing data, as well as uncommenting line 30
            #com.send(dictList)

    # msg.exec_()

    def threeDButtonClicked(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(dataPoints[0], dataPoints[1], dataPoints[2], c='r', linestyle='dashed', marker='o')
        ax.plot(dataPoints[0], dataPoints[1], dataPoints[2], color='r')

        ax.set_xlabel('Relative Position, West/East (m)')
        ax.set_ylabel('Relative Position, South/North (m)')
        ax.set_zlabel('Relative Altitude (m)')

        ax.set_xlim(-270, 270)
        ax.set_ylim(-270, 270)
        ax.set_zlim(0, 25)

        plt.show()

    def loadCSVButtonClicked(self):
        msg = QtWidgets.QMessageBox()
        reply = msg.question(self, 'Load waypoints from CSV?',
                             "Are you sure? This will overwrite your existing waypoints.", QtWidgets.QMessageBox.Yes,
                             QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            del dataPoints[0][:]
            del dataPoints[1][:]
            del dataPoints[2][:]
            del dataPoints[3][:]
            del dataPoints[4][:]
            del dataPoints[5][:]
            aw.list.clear()
            with open('flightPath.csv', 'r') as csvfile:
                csvReader = csv.reader(csvfile)
                for row in csvReader:
                    if len(row) == 3:
                        try:
                            self.dc.addPoint(int(row[0]), int(row[1]), int(row[2]))
                            print(row)
                        except ValueError:
                            True

    # Make sure to check if any row is selected here to avoid crash
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            deletedRow = self.list.currentRow()
            if deletedRow >= 0:
                print('deleted ' + str(deletedRow))
                self.list.takeItem(deletedRow)
                self.dc.removePoint(deletedRow)

        # Left and Right key to increase or decrease altitude
        if event.key() == QtCore.Qt.Key_Right:
            self.altitudeEdit.setText(str(int(self.altitudeEdit.text()) + 1))
        elif event.key() == QtCore.Qt.Key_Left:
            self.altitudeEdit.setText(str(int(self.altitudeEdit.text()) - 1))

        if event.modifiers() & QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Z:
            rowToDelete = len(dataPoints[0]) - 1
            if rowToDelete != 0:
                print('deleted ' + str(rowToDelete))
                self.list.takeItem(rowToDelete)
                self.dc.removePoint(rowToDelete)

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    """A program to plot a flight path for an autonomous UAV."""
                                    )


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
# qApp.exec_()
##############################################################################################
#
# percolation.py - numerical solution for interpretation of a falling head infiltration test
#
##############################################################################################


from functools import partial
from numpy import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import sys
from PyQt5 import QtCore, QtWidgets, uic


# support for user interfacce
qtCreatorFile = 'userInterface.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class DataSet:

    def __init__(self, name):
        # h-vs-t data set
        fileName = name + '.txt'
        lineInput = []        
        inputFile = open(fileName,'r')
        for line in inputFile: lineInput.append(line.split())
        inputFile.close()
        data = array(lineInput[1:])
        data = data.astype(float)
        self.t = transpose(data)[0]
        self.h = transpose(data)[1]
        self.start = min(self.t)
        self.end = max(self.t)


class Model:

    def __init__(self):
        # model parameters
        lineInput = []        
        inputFile = open('params.txt','r')
        for line in inputFile: lineInput.append(line.split())
        inputFile.close()    
        self.K = float(lineInput[0][1])
        self.phi = float(lineInput[1][1])    
        self.S = float(lineInput[2][1])    
        self.E = float(lineInput[3][1])
        self.Q = float(lineInput[4][1])
        self.QFinish = float(lineInput[5][1])
        self.h0 = float(lineInput[6][1])
        self.L0 = float(lineInput[7][1])
        self.name = lineInput[8][1]

    def WriteValues(self):
        # update parameter file with current values
        output_file = open('params.txt','w')
        output_file.writelines(['K', '\t', str(self.K),'\n'])
        output_file.writelines(['phi', '\t', str(self.phi),'\n'])
        output_file.writelines(['S', '\t', str(self.S), '\n'])
        output_file.writelines(['E', '\t', str(self.E), '\n'])
        output_file.writelines(['Q', '\t', str(self.Q), '\n'])
        output_file.writelines(['QFinish', '\t', str(self.QFinish), '\n'])        
        output_file.writelines(['h0', '\t', str(self.h0), '\n'])        
        output_file.writelines(['L0', '\t', str(self.L0), '\n'])
        output_file.writelines(['name', '\t', self.name, '\n'])        
        output_file.close()        
        
    def Qf(self, t):
        # flux into pond (as volume/(time*area))
        flux = self.Q * (t<=self.QFinish)
        return flux

    def Eqns(self, soln, t):
        # coupled ordinary differential equations for percolation
        h = soln[0]
        L = soln[1]
        dhdt = -self.K * (h+L)/L - self.E + self.Qf(t)
        dLdt = self.K * (h+L) / (L*self.phi*(1-self.S))
        return [dhdt, dLdt]

    def SolveODE(self):
        # integrate governing ODEs and plot match to data
        soln0 = [self.h0, self.L0]                                                      # initial conditions
        pond = DataSet(self.name)                                                       # fetch data set
        times = logspace(log10(pond.start), log10(pond.end), num=60, endpoint=True)     # evaluation times
        sol = odeint(self.Eqns, soln0, times)
        sol = transpose(sol)
        PlotCompare(pond.t, pond.h, times, sol[0])                                      # plot model vs. data       
        # write to output file
        output_file = open('model_output.txt','w')
        output_file.writelines(['time','\t', 'h', '\t', 'L', '\n'])
        for i, t in enumerate(times): output_file.writelines([str(t),'\t', str(sol[0][i]), '\t', str(sol[1][i]), '\n'])
        output_file.close() 


class GUI(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, model):
        
        # initiate GUI
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        # load values read from files
        self.KlineInput.setText(str(model.K))    
        self.phiSlider.setValue(int(model.phi*100))
        self.sSlider.setValue(int(model.S*100))
        self.h0lineInput.setText(str(model.h0))
        self.L0lineInput.setText(str(model.L0))
        self.ElineInput.setText(str(model.E))
        self.QflineInput.setText(str(model.Q))
        self.QFinishlineInput.setText(str(model.QFinish))
        self.dataSetlineInput.setText(model.name)

        # button functionality
        self.updateButton.clicked.connect(partial(self.Update, model))
        self.runModelButton.clicked.connect(model.SolveODE)       
        self.saveButton.clicked.connect(model.WriteValues)
        self.exitButton.clicked.connect(self.close)
        
    def Update(self, model):
        # update model and pond objects with values on form
        model.K = float(self.KlineInput.text())
        model.phi = float(self.phiSlider.value())/100.
        model.S = float(self.sSlider.value())/100.
        model.h0 = float(self.h0lineInput.text())
        model.L0 = float(self.L0lineInput.text())
        model.E = float(self.ElineInput.text())
        model.Q = float(self.QflineInput.text())
        model.QFinish = float(self.QFinishlineInput.text())
        model.name = self.dataSetlineInput.text()


def PlotCompare(xd, yd, xm, ym):
    # compare model (xm, ym) with data (xd, yd)
    plt.scatter(xd, yd, s=5, facecolors='none', edgecolors='blue', label = 'Data')
    plt.plot(xm, ym, color = 'black', label = 'Model')
    plt.xlabel('Time')
    plt.ylabel('Water Depth')
    plt.legend(loc=1)
    plt.show()    

		
def Percolation():

    # read model parameters
    model = Model()                             

    # set up GUI
    app = QtCore.QCoreApplication.instance()
    if app is None: app = QtWidgets.QApplication(sys.argv)
    window = GUI(model)
    window.show()
    sys.exit(app.exec_())


############ run script

Percolation()


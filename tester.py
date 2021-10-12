from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, uic
from hilos.serial import Serial

class Test(QDialog):

    btn_salir_testeo = QtCore.pyqtSignal()
    
    def __init__(self, *args):
        super().__init__(*args)
        self.ui = uic.loadUi('views/test.ui', self)
        #Quita los bordes de la ventana
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #El fondo se hace transparente
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.thread = []

        self.btn_exit = self.btn_salir #btn salir de la ventana test

        #Arreglo con los botones de cada panel
        self.paneles = [
            self.btn_testP1, self.btn_testP2, self.btn_testP3, 
            self.btn_testP4, self.btn_testP5, self.btn_testP6
        ]

        #----------EVENTOS----------: 
        #Seleccion de paneles
        self.btn_testP1.clicked.connect(self.selectPanel)
        self.btn_testP2.clicked.connect(self.selectPanel)
        self.btn_testP3.clicked.connect(self.selectPanel)
        self.btn_testP4.clicked.connect(self.selectPanel)
        self.btn_testP5.clicked.connect(self.selectPanel)
        self.btn_testP6.clicked.connect(self.selectPanel)
        
        #Botones para comenzar test e interrumpir
        self.btn_testear.clicked.connect(self.comenzarTest)
        self.btn_stopTest.clicked.connect(self.interrumpir)
        self.btn_salir.clicked.connect(self.salir)


    salir = lambda self: self.btn_salir_testeo.emit()
    #muestra los datos enviados desde el adam en la GUI
    showData = lambda self, texto: self.terminalPanel.append(texto)


    #------------------------COMIENZA EL TEST----------------------------
    def comenzarTest(self):

        self.btn_exit.setEnabled(False)
        self.btn_exit.setStyleSheet("QPushButton{background-color: gray}")
        
        self.btn_stopTest.setEnabled(True)
        self.btn_stopTest.setStyleSheet("QPushButton{background-color: red; color: white; font-weight: bold}")

        for i in range(len(self.paneles)): 
            if(self.paneles[i].isChecked()):
                self.thread = Serial(None, None, None, 1, index=i+1)
                self.thread.start()
                if i == 0: self.thread.panel1Signal.connect(self.showData)
                if i == 1: self.thread.panel2Signal.connect(self.showData)
                if i == 2: self.thread.panel3Signal.connect(self.showData)
                if i == 3: self.thread.panel4Signal.connect(self.showData)
                if i == 4: self.thread.panel5Signal.connect(self.showData)
                if i == 5: self.thread.panel6Signal.connect(self.showData)
                self.paneles[i].setText(f"Testeando panel {i+1}")
                self.paneles[i].setEnabled(False)
        

        #Si alguno de los paneles está checkeado
        for i in range(len(self.paneles)):
            if self.paneles[i]:
                self.btn_testear.setEnabled(False) #btn testear se inhabilita
                self.btn_testear.setStyleSheet("QPushButton{background-color: gray; color: white; font-weight: bold}")
                self.btn_testear.setText("Testeando")
                self.btn_stopTest.setEnabled(True) #btn interrumpir se habilita

 
    #---------------------------INTERRUMPE EL TEST---------------------
    def interrumpir(self):

        self.btn_stopTest.setEnabled(False)
        self.btn_stopTest.setStyleSheet("QPushButton{background-color: gray; color: white; font-weight: bold}")

        for i in range(len(self.paneles)):
            
            if self.paneles[i].isChecked(): 
                self.thread.stop()
                self.paneles[i].setEnabled(True)
                self.paneles[i].setText(f"Test Panel {i+1}")
                self.terminalPanel.clear()

      
        self.btn_testear.setEnabled(False) #btn testear se inhabilita
        self.btn_testear.setStyleSheet("QPushButton{background-color: gray; color: white; font-weight: bold}")
        self.btn_testear.setText("Comenzar tester")

        self.btn_stopTest.setEnabled(False) #btn interrumpir se inhabilita
        self.btn_exit.setEnabled(True)
        self.btn_exit.setStyleSheet("""QPushButton{
            #btn_salir{
                background-color:#414345;
                border-radius:5px;
                border:1px solid #337bc4;
                color:white;
                font-weight:bold;
                text-decoration:none;
            }
            #btn_salir:hover {
	            background-color:#757F9A
            }
            #btn_salir:active {
                position:relative;
                top:1px;
            }
        }""")

        self.deseleccionarPaneles() #deselecciona el panel actual
        self.habilitarPaneles()


    #------------------------SELECCIÓN DE PANELES-----------------------------
    def selectPanel(self):
        
            if (self.btn_testP1.isChecked() or self.btn_testP2.isChecked() or self.btn_testP3.isChecked()
                or self.btn_testP4.isChecked() or self.btn_testP5.isChecked() or self.btn_testP6.isChecked()
            ): 
                for i in range(len(self.paneles)):

                    if self.paneles[i].isChecked():
                        self.paneles[i].setStyleSheet("QPushButton{background-color: #65e615}")
                        continue
                    self.paneles[i].setEnabled(False)
                    self.paneles[i].setStyleSheet("""QPushButton{background-color: gray}""")
                
                self.btn_testear.setEnabled(True)
                self.btn_testear.setStyleSheet("QPushButton{background-color: red; color: white; font-weight: bold}")

            else:
                for i in range(len(self.paneles)):
                    if self.paneles[i].isChecked(): 
                        self.paneles[i].setStyleSheet("QPushButton{background-color: #FC0}")
                        continue

                    self.paneles[i].setEnabled(True)
                    self.paneles[i].setStyleSheet("QPushButton{background-color: #FC0}")
                
                self.btn_testear.setEnabled(False)
                self.btn_testear.setStyleSheet("QPushButton{background-color: gray; color: white; font-weight: bold}")


    #---------------------------HABILITA TODOS LOS PANELES------------------------
    def habilitarPaneles(self):
        for i in range(len(self.paneles)):
            self.paneles[i].setEnabled(True)
            self.paneles[i].setStyleSheet("""QPushButton{background-color: #FC0;}""") #azul
 
    #-------------------------INHABILITA TODOS LOS PANELES----------------------------
    def deseleccionarPaneles(self):
         for i in range(len(self.paneles)):
            self.paneles[i].setChecked(False)
            self.paneles[i].setStyleSheet("""QPushButton{background-color: gray}""")
            

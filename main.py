from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from tester import Test
from formulario import formulario
from historial import historial
from hilos.serial import Serial

class CitecApp(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi('views/main.ui', self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.testeo = Test()
        self.tabla = historial()
        self.formulario = formulario()

        self.thread = {} #aqui se almacenan los hilos

        self.intervaloides = None  

        self.paneles = [
            self.btn_panel1, self.btn_panel2, self.btn_panel3, 
            self.btn_panel4, self.btn_panel5, self.btn_panel6
        ]

        self.panelesCheckeados = []
        self.banderaBtnInciar = False
        

        #---------------------EVENTOS-------------------
        self.btn_test.clicked.connect(self.testear)
        self.btn_iniciar.clicked.connect(self.iniciarProyecto)
        self.btn_salir.clicked.connect(self.salirDeMain)
        self.btn_historial.clicked.connect(self.historial)
        #señal desde tester
        self.testeo.btn_salir_testeo.connect(self.habilitar_btnTest)
        #señal desde formulario
        self.formulario.boolForm.connect(self.habilitar_btnform)

        #Seleccion de paneles
        self.btn_panel1.clicked.connect(self.selectPanel)
        self.btn_panel2.clicked.connect(self.selectPanel)
        self.btn_panel3.clicked.connect(self.selectPanel)
        self.btn_panel4.clicked.connect(self.selectPanel)
        self.btn_panel5.clicked.connect(self.selectPanel)
        self.btn_panel6.clicked.connect(self.selectPanel)

        self.btn_finProyecto.clicked.connect(self.pregunta_fin_proyecto)
        self.limpiar.clicked.connect(self.limpiarTerminal)

        self.registroBtn.clicked.connect(self.registro)

    #----------------------SALIR DE VENTANA MAIN--------------
    def salirDeMain(self):
        self.close()
    #---------------------- VENTANA TESTEO --------------------
    def testear(self):
        self.btn_test.setEnabled(False)
        self.testeo.show()

    habilitar_btnTest = lambda self: self.btn_test.setEnabled(True)
    # ---------------------------------------------------------
    #Funcion muestra ventana historial
    historial = lambda self: self.tabla.show()

    #Ventana formulario
    registro = lambda self: self.formulario.show()

    def limpiarTerminal(self):
        self.terminalPanel.clear()
        
    def habilitar_btnform(self):
        self.banderaBtnInciar = True

    def datos(self):
        self.nomProyecto = self.formulario.getProyecto
        self.nomProfesor = self.formulario.getProfesor
        self.nomAlumno = self.formulario.getAlumno
        self.descripcion = self.formulario.getDescripcion
        self.hf_final  = self.formulario.getFechaFinal
        self.hf_inicio = self.formulario.getFechaInicio
        self.valorIntevalo = self.formulario.getValorIntervalo   
       
    #--------------MOSTRAR DATOS ADAM-------------------
    def iniciarProyecto(self):

        self.btn_salir.setEnabled(False)
        self.btn_salir.setStyleSheet("QPushButton{background-color: gray}")
       
        self.datos()
        #Si el se inicia el proyecto, se habilita el boton interrumpir
        if self.btn_iniciar.isChecked() : 
            self.btn_finProyecto.setEnabled(True)

        for i in range(len(self.paneles)):
            if self.paneles[i].isChecked():
                self.thread[i+1] = Serial(self.nomProyecto, self.hf_inicio, self.hf_final, self.valorIntevalo,index=i+1)
                # self.thread[i+1] = Serial(self.intervaloides, index=i+1)
                self.thread[i+1].start()
                if i == 0: self.thread[i+1].panel1Signal.connect(self.showData)
                if i == 1: self.thread[i+1].panel2Signal.connect(self.showData)
                if i == 2: self.thread[i+1].panel3Signal.connect(self.showData)
                if i == 3: self.thread[i+1].panel4Signal.connect(self.showData)
                if i == 4: self.thread[i+1].panel5Signal.connect(self.showData)
                if i == 5: self.thread[i+1].panel6Signal.connect(self.showData)
                self.thread[i+1].finProyecto.connect(self.interrumpir)
                self.paneles[i].setText(f"Testeando panel {i+1}")
                self.paneles[i].setEnabled(False)

            self.bloquearPaneles()
            self.btn_iniciar.setEnabled(False)
            self.btn_iniciar.setStyleSheet("""QPushButton{
                background-color: grey; 
                color: white;
                font-weight: bold;
            }""")
            self.btn_finProyecto.setEnabled(True)
            self.btn_finProyecto.setStyleSheet("""QPushButton{
                background-color: #65e615; 
                color: black;
                font-weight: bold;
            }""")

    #---------------BLOQUEA LOS PANELES CHECKEADOS---------------------
    def bloquearPaneles(self):

        for i in range(len(self.paneles)):

            if not self.paneles[i].isChecked():
                self.panelesCheckeados.append(self.paneles[i])
                self.paneles[i].setStyleSheet("QPushButton{background-color: gray; color: white; font-weight: bold}")
    
        for i in range(len(self.panelesCheckeados)): self.panelesCheckeados[i].setEnabled(False)
 
    #----------------------Desbloquea TODOS los paneles----------------
    def desbloquearPaneles(self):

        for i in range(len(self.panelesCheckeados)):
        
            self.panelesCheckeados[i].setEnabled(True)
            self.panelesCheckeados[i].setStyleSheet("QPushButton{background-color: #FC0}")
        
    #--------------------Muestra los datos en la "terminal" ------------------
    def showData(self, txt):
        index = self.sender().index
        for i in range(6):
            if index == i+1: self.terminalPanel.append(txt)

    #-----------------------------------------------
    def inicio(self,texto):
        texto = ' Inicio de Proceso'
        self.terminalPanel.append(texto)
    

    def pregunta_fin_proyecto(self):
        res = QMessageBox.question(
            self, "El proyecto será finalizado", "¿Está seguro que desea continuar?", 
            QMessageBox.Yes | QMessageBox.No
        )

        if res == QMessageBox.Yes:
            self.interrumpir()
        

    #------------------INTERRUMPE EL PROYECTO----------------
    def interrumpir(self):
        
        for i in range(len(self.paneles)):

            if self.paneles[i].isChecked():
                self.thread[i+1].stop()
                
                self.paneles[i].setEnabled(True) 
                self.paneles[i].setStyleSheet("QPushButton{background-color: #FC0; }")
                self.paneles[i].setText(f"Panel {i+1}")
                self.paneles[i].setChecked(False)
     
        self.btn_finProyecto.setEnabled(False)
        self.btn_finProyecto.setStyleSheet("""QPushButton{
            background-color: grey; 
            color: white;
            font-weight: bold;
        }""")
        self.desbloquearPaneles()
        self.btn_iniciar.setEnabled(False)
        # self.btn_guardarProyecto.setEnabled(True)

        self.btn_salir.setEnabled(True)
        self.btn_salir.setStyleSheet("""QPushButton{
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


        QMessageBox.information(self, "Proyecto", "El proyecto ha finalizado", QMessageBox.Ok)
    
    #----------------CONTROL ESTILO DE PANELES----------------
    def selectPanel(self):
        count = 0
        for i in range(len(self.paneles)):
            
            if self.paneles[i].isChecked():
                self.paneles[i].setStyleSheet("QPushButton{background-color: #B1001A; color: white}")
                count += 1
            
            if not self.paneles[i].isChecked():
                self.paneles[i].setStyleSheet("QPushButton{background-color: #FC0}")
                # count -= 1

        
        if count != 0  and self.banderaBtnInciar == True: 
            self.btn_iniciar.setEnabled(True)
            self.btn_iniciar.setStyleSheet("""QPushButton{
                background-color: #65e615; 
                color: black;
                font-weight: bold;
            }""")

        else:
            self.btn_iniciar.setEnabled(False)
            self.btn_iniciar.setStyleSheet("""QPushButton{
                background-color: gray; 
                color: white;
                font-weight: bold;
            }""")
          

    #envia este textgo al terminal serial
    def inicio(self,texto):
        texto = ' Inicio de Proceso'
        self.terminalPanel.append(texto)   
   
if __name__=='__main__':
    app = QApplication([])
    mainWindow = CitecApp()
    mainWindow.show()
    app.exec_()
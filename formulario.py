from json.decoder import JSONDecodeError
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic,QtCore
from PyQt5.QtWidgets import QDialog
from datetime import date, datetime
import json
import os
from os import path
import time


from registro import Registros

class formulario(QDialog):

    boolForm = QtCore.pyqtSignal(bool)
 
    def __init__(self, *args):
        super().__init__(*args)
        self.ui = uic.loadUi('views/registro.ui', self)  
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.registro = Registros()
        #------------------Formato-------------
        #--- Hora
        self.horaInicial.setDisplayFormat("H:mm")
        self.horaFinal.setDisplayFormat("H:mm")

        self.horaInicial.setTime(QtCore.QTime.currentTime())
        self.horaFinal.setTime(QtCore.QTime.currentTime())

        #---fecha---
        self.fechaInicial.setDisplayFormat("dd/MM/yyyy")
        self.fechaFinal.setDisplayFormat("dd/MM/yyyy")


        self.fechaInicial.setDate(QtCore.QDate.currentDate())
        self.fechaFinal.setDate(QtCore.QDate.currentDate())
        self.comentario.setPlaceholderText('Maximo 50 Caracteres :')
        self.comentario.textChanged.connect(self.comentariomax)
        
        
      
        self.txt_nomProyecto.setPlaceholderText("Maximo 30 caracteres :")
        self.txt_nomAlumno.setPlaceholderText("Maximo 30 caracteres :")
        self.txt_nomProfeCargo.setPlaceholderText("Maximo 30 caracteres :")

        #------------------------------------------------------------------------   


        # llama f(x) guardar formulario
        self.btn_guardarProyecto.clicked.connect(self.validar) 
        
        self.txt_nomProyecto.textChanged.connect(self.v_proyecto)
        self.txt_nomAlumno.textChanged.connect(self.v_nombre)
        self.txt_nomProfeCargo.textChanged.connect(self.v_profesor)
        # -----------------------------------
        self.btn_salir.clicked.connect(self.reject)

    def comentariomax(self):
        maximo = 50
        comentario = self.comentario.toPlainText()
        

        if len(comentario) > maximo:
            self.comentario.setStyleSheet("border: 4px solid red; ")
            
            return False
        else:
            self.comentario.setStyleSheet("border: 4px solid green; ")
            
            return True

        
    #------------GUARDA LOS DATOS DEL FORMULARIO----------
    def guardarDatos(self):
        #Guarda datos tipo .text()
        self.nomProyecto = self.txt_nomProyecto.text()
        self.nomProfesor = self.txt_nomProfeCargo.text()
        self.nomAlumno   = self.txt_nomAlumno.text()
        self.descripcion = self.comentario.toPlainText()


    #     #Guarda fecha  y hora
        self.hf_inicio_aux = self.horaInicial.text()+' '+ self.fechaInicial.text()
        self.hf_final_aux  = self.horaFinal.text()+' '+self.fechaFinal.text()

    #     #guarda intevalo
        self.valorIntevalo = int(self.intervalo.text())

    #     self.intervaloides = self.valorIntevalo

    #     #guarda fecha y hora tipo DATETIME
        self.hf_inicio = datetime.strptime(self.hf_inicio_aux, '%H:%M %d/%m/%Y')
        self.hf_final = datetime.strptime(self.hf_final_aux, '%H:%M %d/%m/%Y')

        
        self.diccionario()
        # self.registro.abrir()
  

    @property
    def getFechaInicio(self):
        return  self.hf_inicio
    
    @property
    def getProyecto(self):
        return self.nomProyecto
       
    @property
    def getProfesor(self):
        return self.nomProfesor

    @property
    def getAlumno(self):
        return self.nomAlumno
    
    @property
    def getFechaFinal(self):
        return self.hf_final
    
    @property
    def getValorIntervalo(self):
        return self.valorIntevalo    

    @property
    def getDescripcion(self):
        return self.descripcion 
    
    @property
    def getBoolForm(self):
        return self.boolForm  

    # #-----------DATOS DEL FORMULARIO GUARDADOS, LOS ALMACENA EN JSON--------------- 
    def diccionario(self):
        self.DATOS = []

        Proyecto = self.nomProyecto
        Profesor = self.nomProfesor
        Alumno = self.nomAlumno
        Fecha_inicio = self.fechaInicial.text()
        Hora_inicio =  self.horaInicial.text()
        Fecha_final = self.fechaFinal.text()
        Hora_final =  self.horaFinal.text()
        descripcion = self.descripcion
        intervalo = self.intervalo.text()

        datos = {} #Se guarda el ultimo registro del formulario
        datos['Proyecto'] = Proyecto
        datos['Profesor'] = Profesor
        datos['Alumno'] = Alumno
        datos['f_inicio'] = Fecha_inicio
        datos['f_final'] = Hora_inicio
        datos['h_inicio']  = Fecha_final
        datos['h_final']   = Hora_final
        datos['descripcion'] = descripcion
        datos['intervalo'] = intervalo
   
        try:
            #Si no existe el archivo historial.json
            if os.path.isfile('Historial.json') == False:   
                self.DATOS.append(datos)
                self.escribirJson(self.DATOS, 'a+')

            else:
                self.data = json.load(open('Historial.json'))
                self.data.append(datos)#se añade al ultimo
                self.escribirJson(self.data, 'w+')

        except JSONDecodeError:
            print("Hubo un error con JSON") 

    # #-----------------------ESCRIBE EN EL JSON------------------
    def escribirJson(self, obj, p):
        with open ('Historial.json', p) as f:
            json.dump(obj, f, indent=4)

     
        self.registro.mostrar()

    def v_profesor(self):
        profesor = self.txt_nomProfeCargo.text()
        # validar=QRegExpValidator(QtCore.QRegExp('^$'))
        if not profesor:
            self.txt_nomProfeCargo.setStyleSheet("border: 4px solid red; ")
           
            return False
        # if not validar:
        #     self.txt_nomProfeCargo.setStyleSheet("border: 2px solid yellow; ")
        #     print("2")
        #     return False
        else:
            self.txt_nomProfeCargo.setStyleSheet("border: 4px solid green; ")
            return True  
        
    def v_proyecto(self):
        proyecto = self.txt_nomProyecto.text()
        #validar  = QRegExpValidator(QtCore.QRegExp('^$'))
     
        if not proyecto:
               
            self.txt_nomProyecto.setStyleSheet("border: 4px solid red; ")
           
            return False
        # if not validar:
        #     self.txt_nomProyecto.setStyleSheet("border: 2px solid yellow; ")
        #     return False
        else:
           
            self.txt_nomProyecto.setStyleSheet("border: 4px solid green; ")
            return True

    def v_nombre(self):
        nombre = self.txt_nomAlumno.text()
        #validar=QRegExpValidator(QtCore.QRegExp('^$'))
        if not nombre:
            self.txt_nomAlumno.setStyleSheet("border: 4px solid red; ")
            return False
        # if not validar:
        #     self.txt_nomAlumno.setStyleSheet("border: 2px solid yellow; ")
        #     return False
        else:
            self.txt_nomAlumno.setStyleSheet("border: 4px solid green; ")
            return True

    def v_hf_final(self):
        hf_final_aux  = self.horaFinal.text()+' '+self.fechaFinal.text()
        hf_final = datetime.strptime(hf_final_aux, '%H:%M %d/%m/%Y')

        if hf_final > self.hf_inicio:

            self.horaFinal.setStyleSheet("border: 4px solid green; ")
            self.fechaFinal.setStyleSheet("border: 4px solid green; ")
            

            return True
        else:
            self.horaFinal.setStyleSheet("border: 4px solid red; ")
            self.fechaFinal.setStyleSheet("border: 4px solid red; ")
            QMessageBox.warning(
            self,
            "Ingrese Nuevamente",
            f'Hora-Fecha Final: "{hf_final }"\nNo Debe Ser Menor a Hora-Fecha Inicial'
            )

            return False






    def v_hf_inicial(self):
        hf_inicio_aux = self.horaInicial.text()+' '+ self.fechaInicial.text()
        


       


    #     #guarda fecha y hora tipo DATETIME
        self.hf_inicio = datetime.strptime(hf_inicio_aux, '%H:%M %d/%m/%Y')
        
        now = datetime.now() # actual hora y fecha
        time_aux = now.strftime('%H:%M %d/%m/%Y')
        time=datetime.strptime(time_aux, '%H:%M %d/%m/%Y')



        if self.hf_inicio >= time:
            self.horaInicial.setStyleSheet("border: 4px solid green; ")
            self.fechaInicial.setStyleSheet("border: 4px solid green; ")
           
            return True
        else:
            self.horaInicial.setStyleSheet("border: 4px solid red; ")
            self.fechaInicial.setStyleSheet("border: 4px solid red; ")
            QMessageBox.warning(
            self,
            "Ingrese Nuevamente",
            f'Hora-Fecha Final: "{self.hf_inicio}"\nNo Debe Ser Menor a Hora Actual'
            )
            
            return False
      

            
        

        
        
    
    def validar(self):
           
        #Validamos que los metodo validar  retorne true
        if  self.v_proyecto() and self.v_nombre() and self.v_profesor() and self.v_hf_inicial() and self.v_hf_final() and self.comentariomax():
            
            
            QMessageBox.information(self, "Formulario Correcto", "Registro Ingresado", QMessageBox.Ok)
            self.boolForm.emit(True)
            self.guardarDatos()
            self.close()
 
         
            # self.btn_guardarProyecto.isChecked()
            # self.btn_guardarProyecto.setEnabled(False)
            
        else:
            #Mostramos un warning
            QMessageBox.warning(self, "Formulario Incorrecto", "Revisar Datos Ingresados", QMessageBox.Ok)
     

    
from PyQt5.QtWidgets import (
    QDialog,QDialog, QFileDialog,QTableWidgetItem,
    QAbstractItemView,QMenu, QAction,QMessageBox
)
from PyQt5 import uic
from PyQt5.QtCore import QFile, Qt
import json
import os
import csv
import pandas as pd
from registro import Registros
from datos import Libro
from formulario import formulario

class historial(QDialog):
 
    datos = []   

    def __init__(self, *args):
        super().__init__(*args)
        self.ui = uic.loadUi('views/historial.ui', self)

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.iniUI()
        self.registro = Registros()
        self.libro = Libro()
        self.formulario = formulario()
        self.btn_salir.clicked.connect(self.reject)
        #self.btn_borrar.clicked.connect(self.borrarHistorial)
        self.btn_export.clicked.connect(self.export_csv)
        
        
    #-------------------------Widget Tabla---------------
    def iniUI(self):
        #desabilitar edicion
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #desabilitar el arrastrar y soltar
        self.tableWidget.setDragDropOverwriteMode(False)

        #seleccionar toda la fila
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        #seleccionar una fila a la vez
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Especifica dónde deben aparecer los puntos suspensivos "..." cuando se muestran
        # textos que no encajan
        self.tableWidget.setTextElideMode(Qt.ElideRight)# Qt.ElideNone

        #Establecer ajuste de texto
        self.tableWidget.setWordWrap(False)

        #desabilitar clasificacion
        self.tableWidget.setSortingEnabled(False)

        #Establecer numero de columnas
        self.tableWidget.setColumnCount(50)

        #alineacion del texto enabezado
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|
                                                          Qt.AlignCenter)
        
        #desabilitar el resaltado de texto encabezado
        self.tableWidget.horizontalHeader().setHighlightSections(False)

        #la ultima seccion del encabezado visible ocupe todo el espacio
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        #ocultar encabezado vertical
        self.tableWidget.verticalHeader().setVisible(False)

        #Fondo colores alternados
        self.tableWidget.setAlternatingRowColors(True)
        #prueba
        encabezado=["PROYECTO","PROFESOR ACARGO","NOMBRE ALUMNO","FECHA INICIO",
                    "FECHA FINAL","HORA INICIO", "HORA FINAL","DESCRIPCION",
                    "INTERVALO"]
        self.tableWidget.setHorizontalHeaderLabels(encabezado)
 

        #menu contextual
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tableWidget.customContextMenuRequested.connect(self.menuContextual)

        #establecer ancho de columnas
        for indice, ancho in enumerate ((80,120, 120,110,150), start=0):
            self.tableWidget.setColumnWidth(indice,ancho)

       
        
        #-----------------menu contextual --------
        
        menu = QMenu()
        for indice, columna in enumerate(encabezado,start = 0):
            accion = QAction(columna, menu)
            accion.setCheckable(True)
            accion.setChecked(True)
            accion.setData(indice)

            menu.addAction(accion)

        self.botonMostrarOcultar.setMenu(menu)
        #------------- eventos---------------
        #self.btnDatos.clicked.connect(self.datosTabla)
        self.btn_actualizar.clicked.connect(self.existen_datos)
        self.btn_buscar.clicked.connect(self.buscador)
        #self.abrir.clicked.connect(self.guardar2)
        self.guardar.clicked.connect(self.guardar2)

        menu.triggered.connect(self.mostrarOcultar)
        
        
    #---------------Funciones------------
 
      

    def guardar2(self):
        #print("exportar json")
      
        ubicacion = QFileDialog.getSaveFileName(
            self,
            'Guardar Archivo',
            
            'Historial',
            
            'Json (*.json)'
        )[0]
        print(ubicacion)
        QFile.copy('Historial.json',ubicacion)

       
    

        
        




    def buscador(self):
        
        
        proyecto = self.buscar.text()

        encontrado= False
        
        for libro in self.registro:
            if proyecto == libro.alumno:
                # print("este es el alumno:" + libro.alumno)
                # print(" es el mismo")
            # else:
            #     print("nones")
                self.tableWidget.clear()
                self.tableWidget.setRowCount(1)
                encabezado=["NOMBRE ALUMNO","PROYECTO","PROFESOR ACARGO","FECHA INICIO",
                            "FECHA FINAL","HORA INICIO", "HORA FINAL","DESCRIPCION","INTERVALO"]
                self.tableWidget.setHorizontalHeaderLabels(encabezado)

                nombre_wt   =   QTableWidgetItem(libro.alumno)
                proyecto_wt =   QTableWidgetItem(libro.proyecto)
                profesor_wt =   QTableWidgetItem(libro.profesor)
                f_inicio_wt =   QTableWidgetItem(libro.f_inicio)
                f_final_wt =    QTableWidgetItem(libro.f_final)
                h_inicio_wt =   QTableWidgetItem(libro.h_inicio)
                h_final_wt =   QTableWidgetItem(libro.h_final)
                descripcion_wt = QTableWidgetItem(libro.descripcion)
                intervalo_wt = QTableWidgetItem(libro.intervalo)



                self.tableWidget.setItem(0, 0, nombre_wt)
                self.tableWidget.setItem(0, 1, proyecto_wt)
                self.tableWidget.setItem(0, 2, profesor_wt)
                self.tableWidget.setItem(0, 3, f_inicio_wt)
                self.tableWidget.setItem(0, 4, f_final_wt)
                self.tableWidget.setItem(0, 5, h_inicio_wt)
                self.tableWidget.setItem(0, 6, h_final_wt)
                self.tableWidget.setItem(0, 7, descripcion_wt)
                self.tableWidget.setItem(0, 8, intervalo_wt)
                encontrado = True
                return
        if not encontrado:
            QMessageBox.warning(
            self,
            "Atencion",
            f'El  alumno "{proyecto}"  no fue encontrado'
            )

       
      
        # for libro in self.registro:
        #     print(libro)
    
        

    

    def existen_datos(self):
        if os.path.isfile("Historial.json"):
            self.datosTabla()
        else:
            QMessageBox.information(self, "ERROR", "No hay datos en el historial", QMessageBox.Ok)


    def datosTabla(self):
        #limpia la tabla
        self.tableWidget.clearContents()
        self.registro.abrir()
        self.leerJson()
        

        datos = self.datos
        fila_count = (len(datos))
        columnas_count =(len(datos[0]))

        self.tableWidget.setColumnCount(columnas_count)
        self.tableWidget.setRowCount(fila_count)
            # muestras las llaves de la lista en el header
        #self.tableWidget.setHorizontalHeaderLabels((list(datos[0].keys())))
        encabezado=["PROYECTO","PROFESOR ACARGO","NOMBRE ALUMNO","FECHA INICIO",
                    "FECHA FINAL","HORA INICIO", "HORA FINAL","DESCRIPCION",
                    "INTERVALO"]
        self.tableWidget.setHorizontalHeaderLabels(encabezado)
        
        datos_revertidos = list()

       #-----Invierte los datos del json------
        for i in range(len(datos)):
            datos_revertidos.append(datos[len(datos)-1-i])

        #--Muestra los datos en la interfaz
        for fila in range(fila_count):
            for columnas in range(columnas_count):
                valor = (list(datos_revertidos[fila].values())[columnas])
                self.tableWidget.setItem(fila,columnas,QTableWidgetItem(valor))
    
    #------------------------BORRAR HISTORIAL DE PROYECTOS-----------------
    # def borrarHistorial(self):
    #     if os.path.isfile("Historial.json"):
    #         ret = QMessageBox.question(
    #             self, "El historial será eliminado", "¿Está seguro que desea continuar?", 
    #             QMessageBox.Yes | QMessageBox.No
    #         )
    #         if ret == QMessageBox.Yes:
    #             self.tableWidget.clear()            
    #             encabezado=["PROYECTO","PROFESOR ACARGO","NOMBRE ALUMNO","FECHA INICIO",
    #                 "FECHA FINAL","HORA INICIO", "HORA FINAL","DESCRIPCION",
    #                 "INTERVALO"]
    #             self.tableWidget.setHorizontalHeaderLabels(encabezado)
    #     else:
    #         QMessageBox.information(self, "ERROR", "No existe historial para borrar", QMessageBox.Ok)
        

    
    #------------------------EXPORTAR HISTORIAL A CSV-----------------
    def export_csv(self):
        
        if os.path.isfile("Historial.json"):
            df = pd.read_json (r'Historial.json')
            path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            df.to_excel(f"{path_desktop}/archivo.xlsx", index=None, header = True)
            QMessageBox.information(self, "EXITO", "El historial se ha exportado a tu escritorio!", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "ERROR", "No existe historial para exportar", QMessageBox.Ok)


    def mostrarOcultar(self,accion):

        columna = accion.data()

        if accion.isChecked():
            self.tableWidget.setColumnHidden(columna, False)
        else:
            self.tableWidget.setColumnHidden(columna,True)

             
    def leerJson(self):
        
        with open("historial.json", "r") as archivo:
            datos = archivo.read()
        self.datos =json.loads(datos)
        
        
       
        

            
    
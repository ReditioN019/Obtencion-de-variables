from genericpath import exists
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
import serial, time
from datetime import datetime
import os

class Serial(QThread, QDialog):
    
    panel1Signal = pyqtSignal(str)
    panel2Signal = pyqtSignal(str)
    panel3Signal = pyqtSignal(str)
    panel4Signal = pyqtSignal(str)
    panel5Signal = pyqtSignal(str)
    panel6Signal = pyqtSignal(str)

    finProyecto = pyqtSignal(bool)


    def __init__(self, nombreProyecto, hf_inicio, hf_final, intervalo, index=0):
        super().__init__()
        self.index=index
        self.is_running = True
        self.serialPort = serial.Serial()
        self.serialPort.baudrate = 9600
        self.serialPort.port = "COM2"

        self.nombreProyecto = nombreProyecto
        self.intervalo = intervalo
        self.hf_inicio = hf_inicio
        self.hf_final = hf_final
        self.txt = None
        self.banderaWhile = True
        self.proyectoFinalizado = True

    
    def run(self):

        if self.hf_inicio != None and self.hf_final != None:
            self.crearCarpeta()
            tiempo = time.strftime('%d-%m-%Y')

        count = 0

        if self.index == 1: 
            comand = "#03\r"
            if self.hf_inicio != None and self.hf_final != None:
                self.txt = open(f'{self.escritorio}/{tiempo}{"P1"} {self.nombreProyecto}.txt', mode="a")

            try:
                self.serialPort.open()

                while self.serialPort.is_open:

                    self.serialPort.write(comand.encode('ascii'))
                    value = self.serialPort.readline() #readline(58)
        
                    if self.hf_inicio != None and self.hf_final != None:
                       
                        tiempo = time.strftime('%d-%m-%Y   %H:%M:%S  ')
                        
                        if self.hf_inicio.now() > self.hf_final: 
                            count +=1
                            break

                        value = tiempo +' '+ value.decode('utf-8').rstrip()
                        self.txt.write(f"{str(value)}\n") #se escribe la linea de codigo

                        if datetime.now() >= self.hf_inicio:
                            value = "ADAM-1: ",value
                            self.panel1Signal.emit(str(value))
                            
                    else:#para tester
                        value = value.decode('utf-8').rstrip()
                        self.panel1Signal.emit(str(value))
                    

                    time.sleep(self.intervalo )
     
                self.txt.close()  

            except:
                pass


        if self.index == 2:
            if self.hf_inicio != None and self.hf_final != None: 
                self.txt2 = open(f'{self.escritorio}/{tiempo}{"P2"} {self.nombreProyecto}.txt', mode="a")
            try:
                while self.banderaWhile:
                    
                    value = "Datos panel 2"
                    tiempo = time.strftime('%d-%m-%Y   %H:%M:%S  ')

                    value = tiempo +' '+ value

                    if self.hf_inicio != None and self.hf_final != None:

                        if self.hf_inicio.now() > self.hf_final: 
                            count +=1
                            break

      
                        if datetime.now() >= self.hf_inicio:
                            value = "ADAM-2: "+ value
                            self.panel2Signal.emit(str(value))

                        self.txt2.write(f"{str(value)}\n")

                    else: self.panel2Signal.emit(str(value))
                    
                    time.sleep(self.intervalo + 0.03)

                self.txt2.close() 

            except:
                pass

        if self.index == 3: 
            if self.hf_inicio != None and self.hf_final != None:
                self.txt3 = open(f'{self.escritorio}/{tiempo}{"P3"} {self.nombreProyecto}.txt', mode="a")
            try:
                while self.banderaWhile:
                    
                    value = "Datos panel 3"
                    tiempo = time.strftime('%d-%m-%Y   %H:%M:%S  ')

                    value = tiempo +' '+ value

                    if self.hf_inicio != None and self.hf_final != None:

                        if self.hf_inicio.now() > self.hf_final: 
                            count +=1
                            break
                        
                        if datetime.now() >= self.hf_inicio:
                            value = "ADAM-3: "+ value
                            self.panel3Signal.emit(str(value))

                        self.txt3.write(f"{str(value)}\n")
                    
                    else: self.panel3Signal.emit(str(value))

                    time.sleep(self.intervalo + 0.06)

                self.txt3.close() 
            except:
                pass

        if self.index == 4: 
            if self.hf_inicio != None and self.hf_final != None:
                self.txt4 = open(f'{self.escritorio}/{tiempo}{"P4"} {self.nombreProyecto}.txt', mode="a")
            try:
                while self.banderaWhile:
                    
                    value = "Datos panel 4"
                    tiempo = time.strftime('%d-%m-%Y   %H:%M:%S  ')

                    value = tiempo +' '+ value

                    if self.hf_inicio != None and self.hf_final != None:

                        if self.hf_inicio.now() > self.hf_final: 
                            count +=1
                            break
                        
                        if datetime.now() >= self.hf_inicio:
                            value = "ADAM-4: "+ value
                            self.panel4Signal.emit(str(value))

                        self.txt4.write(f"{str(value)}\n")
                    
                    else: self.panel4Signal.emit(str(value))

                    time.sleep(self.intervalo + 0.09)

                self.txt4.close() 
            except:
                pass
            
        if self.index == 5: 
            if self.hf_inicio != None and self.hf_final != None:
                self.txt5 = open(f'{self.escritorio}/{tiempo}{"P5"} {self.nombreProyecto}.txt', mode="a")
            try:
                while self.banderaWhile:
                    
                    value = "Datos panel 5"
                    tiempo = time.strftime('%d-%m-%Y   %H:%M:%S  ')

                    value = tiempo +' '+ value

                    if self.hf_inicio != None and self.hf_final != None:

                        if self.hf_inicio.now() > self.hf_final: 
                            count +=1
                            break
                        
                        if datetime.now() >= self.hf_inicio:
                            value = "ADAM-5: "+ value
                            self.panel5Signal.emit(str(value))

                        self.txt5.write(f"{str(value)}\n")

                    else: self.panel5Signal.emit(str(value))

                    time.sleep(self.intervalo + 0.12)
                
                self.txt5.close() 
            except:    
                pass
                
            

        if self.index == 6: 
            if self.hf_inicio != None and self.hf_final != None:
                self.txt6 = open(f'{self.escritorio}/{tiempo}{"P6"} {self.nombreProyecto}.txt', mode="a")
            try:
                while self.banderaWhile:
                    
                    value = "Datos panel 6"
                    tiempo = time.strftime('%d-%m-%Y   %H:%M:%S  ')

                    value = tiempo +' '+ value

                    if self.hf_inicio != None and self.hf_final != None:

                        if self.hf_inicio.now() > self.hf_final: 
                            count +=1
                            break
                        
                        if datetime.now() >= self.hf_inicio:
                            value = "ADAM-6: "+ value
                            self.panel6Signal.emit(str(value))

                        self.txt6.write(f"{str(value)}\n")

                    else: self.panel6Signal.emit(str(value))

                    time.sleep(self.intervalo + 0.15)
                
                self.txt6.close() 
            except:
                pass

        if count > 0: self.finProyecto.emit(self.proyectoFinalizado)


    #-----------CIERRA EL PUERTO SERIAL-------------
    def stop(self):
        # print("Fin Hilo", self.index)
        self.is_running = False
        self.banderaWhile = False
        self.serialPort.close()

    #--------CREA UN TXT CON FECHA Y NOMBRE DE PROYECTO----------
    # def crearTxt(self):
        
        # self.txt = open(f'{self.escritorio}/{tiempo}{"P1"} {self.nombreProyecto}.txt', mode="a")
        # self.txt2 = open(f'{self.escritorio}/{tiempo}{"P2"} {self.nombreProyecto}.txt', mode="a")
        # self.txt3 = open(f'{self.escritorio}/{tiempo}{"P3"} {self.nombreProyecto}.txt', mode="a")
        # self.txt4 = open(f'{self.escritorio}/{tiempo}{"P4"} {self.nombreProyecto}.txt', mode="a")
        # self.txt5 = open(f'{self.escritorio}/{tiempo}{"P5"} {self.nombreProyecto}.txt', mode="a")
        # self.txt6 = open(f'{self.escritorio}/{tiempo}{"P6"} {self.nombreProyecto}.txt', mode="a")
        # self.txt = open(f'proyectos/{tiempo} {self.nombreProyecto}.txt', mode="w")
 
        
    #--------CREA UN TXT CON FECHA Y NOMBRE DE PROYECTO----------
    def crearCarpeta(self):
        self.escritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop','proyectos')

        if os.path.isdir(self.escritorio):
            return
        else:
            os.makedirs(self.escritorio, exist_ok=True)
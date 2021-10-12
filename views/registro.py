import json




class registro(Qobject): #declaramos la clase principal
    #comentr varias lineas ctrl, +k +
    #definimos los parametros
    def __init__(self,nomProyecto , nomProfesor,nomAlumno,fechaInicio,fechaFinal,horaInicio,horaFin,valorIntervalo,descripcion,estado): 

        estado = "" 
        #declaramos los atributos
        self.nomProyecto = nomProyecto
        self.nomProfesor = nomProfesor
        self.nomAlumno   = nomAlumno
        self.fechaInicio = fechaInicio
        self.fechaFinal = fechaFinal
        self.horaInicio = horaInicio
        self.horaFinal = horaFin
        self.valorIntervalo = valorIntervalo
        self.descripcion = descripcion
        self.estado = estado

    @staticmethod
    def diccionario(dict):
        return registro(dict["nomProyecto"],dict["nomProfesor"],dict["nomAlumno"],dict["fechaInicio"],dict["fechaFinal"],dict["horaInicio"],dict["horaFinal"],dict["descripcion"],dict["estado"] )

    def __str__(self):
        print(" nombre proyecto =", self.nomProyecto)
        print(" fecha inicio =", self.fechaInicio)
        print(" hora inicio =", self.horaInicio)
        
        return self.horaInicio

    def jsonDefault(object):
        return object.__dict__
    #metodo para mostrar el nombre del proyecto


    def _form_packet(self, params=None):
        if not params:
            params = {}
        #params["fecha inicio"] = self.fechaInicio
        params["intervalo"] = self.valorIntervalo
        """ params["Nombre Proyecto"] = self.nomProyecto
        params["Nombre Alumno"] = self.nomAlumno
        params["Nombre Profesor"] = self.nomProfesor
        params["Fecha Inicial"] = self.fechaInicio
        params["Fecha Final"] = self.fechaFinal
        params["Hora Inicial"] = self.horaInicio
        params["Hora Final"] = self.horaFinal
        
        params["Intervalo"] = self.valorIntervalo
        params["Descripcion"] = self.descripcion
        params["Estado"] = self.estado """
        for key, value in params.items():
            if value is None:
                del params[key]
        packet = json.dumps(params)
        with open('prueba.json','a')as f:
            
            json.dump(packet,f,indent=4, separators=(". ", " = "))
        
        return packet    

    
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
    def getFechaInicio(self):
        return self.fechaInicio
    
    @property
    def getFechaFinal(self):
        return self.fechaFinal
    
    @property
    def getHoraInicial(self):
        return self.horaInicio
    
    @property
    def getHoraFinal(self):
        return self.horaFinal

    @property
    def geValorIntervalo(self):
        return self.valorIntervalo    
        

        
        
        
        
    #metodo set para  agregar a la clase registro
    def setNombreProyecto(self, nuevo):
        self.nomProyecto = nuevo
        print(" f(X) set nombre" + self.nomProyecto)

    
    def creaJson(diccionario):
        
        with open('datos.json','w') as f:
            json.drump(diccionario, f)
        
        print()

   
        


   


        
    

    
        
            
        
        
    
        
        
        

        
        


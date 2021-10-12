
#from registro import R01


class Libro:
    def __init__(self, 
                Proyecto= "", 
                Profesor="",
                Alumno="", 
                f_inicio="",
                f_final="",
                h_inicio = "",
                h_final="",    
                descripcion="",
                intervalo= 0):


        self.__proyecto = Proyecto
        self.__profesor = Profesor
        self.__alumno   = Alumno
        self.__f_inicio = f_inicio
        self.__f_final  = f_final
        self.__h_inicio  = h_inicio
        self.__h_final  = h_final
        self.__descripcion = descripcion
        self.__intervalo   = intervalo
    



    def __str__(self):
        lista = "Proyecto:{0} - Profesor: {1} - Alumno: {2} - f_inicio: {3}  - f_final: {4}  - h_inicio: {5} - h_final: {6} - descripcion: {7} - intervalo:{8}  "
        return  lista.format(self.__proyecto, self.__profesor, self.__alumno, self.__f_inicio, self.__f_final, self.__h_inicio, self.__h_final, self.__descripcion, self.__intervalo)
 
    @property
    def proyecto(self):
        return self.__proyecto

    @property
    def profesor(self):
        return self.__profesor
        
    
    @property
    def alumno(self):
        return self.__alumno

    @property
    def f_inicio(self):
        return self.__f_inicio 
    
    @property
    def f_final(self): 
        return self.__f_final 

    @property
    def h_inicio(self):
        return self.__h_inicio

    @property
    def h_final(self):
        return self.__h_final

    
    @property   
    def descripcion(self):
        return self.__descripcion
    @property 
    def intervalo(self):
        return self.__intervalo
        

        

    
        
        
        
    
        

   
# R01 =  Libro(Proyecto="asd",Profesor="asd",Alumno="asd",f_inicio="asd",f_final="sdad")

# print(R01)
    # def to_dict(self):
    #     return {
    #         "Proyecto":self.__proyecto,
    #         "Profesor":self.__profesor,
    #         "Alumno":self.__alumno,
            
    #         "Descripcion":self.__descripcion,
    #         "Intervalo":self.__intervalo,


        # }

    # def __str__(self):
    #     return  (+
    #         'Proyecto: ' + self.__proyecto + '\n' +
    #         'Profesor: ' + self.__profesor + '\n' +
    #         'Alumno: ' + self.__alumno + '\n' +
    #         'Fecha Inicio: ' + self.__fechaInicio + '\n' +
    #         'Hora Inicio: ' + self.__horaInicio+ '\n' +
    #         'Fecha Final: ' + self.__fechaFinal + '\n' +
    #         'Hora Final: ' + self.__horaFinal + '\n' +
    #         'Descripcion: ' + self.__descripcion + '\n' +
    #         'Intervalo: ' + self.__intervalo + '\n' + 
    #     )

    
   

  
   
 
                
 
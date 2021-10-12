
from datos import Libro
import json


class Registros:
    def __init__(self):
        self.__libros = []



    
    def agregar(self, libro:Libro):
        self.__libros.insert(0,libro)

    def mostrar(self):
        for libro in self.__libros:
            print(libro)


    def __str__(self):
        return "".join(
            str(libro)+ '\n' for libro in self.__libros
        )
    

    def __len__(self):
        return len(self.__libros)

    def __iter__(self):
       self.cont = 0
       return self
    
    def __next__(self):
        if self.cont < len(self.__libros):
            libro = self.__libros[self.cont]
            self.cont += 1
            return libro
        else:
            raise StopIteration

       
        
    # def guardar(self):
    #     with open('prueba.json','w')as archivo:
    #         lista = [libro.to_dict() for libro in self.__libros]
    #         print(lista)
          
        

    def abrir(self):
        try:
            with open('Historial.json','r') as archivo:
                lista = json.load(archivo)
                self.__libros = [Libro(**libro) for libro in lista]
                
            return 1
        except:
            return 0
    
    
        
# R01= Libro("camiloasd","asdas","asdas","asdas","asdas","asdas","asdas","asdas",2)
# # R02= Datos("asdsdfas","asdsdfas","assddas","asfdsdas","afdssdas","asdas","asdfdsas","assdfas",50)

# # # print(R01)

# registros = Registros()
# registros.abrir()
# # registros.agregar(R01)
# # # registros.agregar(R02)
# registros.mostrar()
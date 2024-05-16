#Importación de librerias necesarias para conexión con Cassandra y gestión de fechas
import datetime

from cassandra.cluster import Cluster
from datetime import date



#Hacer ejercicio 1
#Programa principal
#Conexión con Cassandra
cluster = Cluster()
#cluster = Cluster(['192.168.0.1', '192.168.0.2'], port=..., ssl_context=...)
session = cluster.connect('gersonvillugas')

numero = -1
#Parte 1: Definición de clases de las entidades y relaciones
class Libro:
    ''' Antiguo constructor usado antes de que hubiese preferencias
    def __init__(self, IdCliente, Nombre, DNI, Direccion):
        self.IdCliente = IdCliente
        self.Nombre = Nombre
        self.DNI = DNI
        self.Direccion = Direccion
    '''
    #nuevo constructor que incluya la coleccion de gustos
    def __init__(self, Libro_ISBN, Libro_anio, Libro_titulo, Libro_temas) :
        self.Libro_ISBN = Libro_ISBN
        self.Libro_anio = Libro_anio
        self.Libro_titulo = Libro_titulo
        self.Libro_temas = Libro_temas

class Ejemplar:
    def __init__(self, Ejemplar_numero, Ejemplar_status, Libro_ISBN,Libro_titulo):#Constructor con relación 1:n entre Libro y Ejemplar
        self.Ejemplar_numero = Ejemplar_numero
        self.Ejemplar_status = Ejemplar_status
        self.Libro_ISBN = Libro_ISBN
        self.Libro_titulo = Libro_titulo

class EjemplarSinRelacion:
    def __init__(self, Ejemplar_numero, Ejemaplar_status): #Constructor sin relación 1:n entre Cliente y Pedido
        self.Ejemplar_numero = Ejemplar_numero
        self.Ejemaplar_status = Ejemaplar_status

class Ejem_usuario:
    def __init__ (self, Ejemplar_numero, Usuario_DNI, Es_prestado):
        self.Ejemplar_numero = Ejemplar_numero
        self.Usuario_DNI = Usuario_DNI
        self.Es_prestado = Es_prestado
class Usuario:
    def __init__(self, Usuario_DNI,Usuario_nombre,Usuario_calle, Usuario_ciudad):
        self.Usuario_DNI = Usuario_DNI
        self.Usuario_nombre = Usuario_nombre
        self.Usuario_calle =Usuario_calle
        self.Usuario_ciudad = Usuario_ciudad

class Autor: #constructor relacion n  :n autor y libro
    def __init__(self, Autor_cod, Autor_nombre, Autor_premios,Libro_ISBN,Libro_titulo,Libro_año):
        self.Autor_cod = Autor_cod
        self.Autor_nombre = Autor_nombre
        self.Autor_premios = Autor_premios
        self.Libro_ISBN = Libro_ISBN
        self.Libro_titulo = Libro_titulo
        self.Libro_año= Libro_año

class AutorSinRelacion: #constructor relacion n  :n autor y libro
    def __init__(self, Autor_cod, Autor_nombre, Autor_premios):
        self.Autor_cod = Autor_cod
        self.Autor_nombre = Autor_nombre
        self.Autor_premios = Autor_premios

class Editorial: #constructor relacion n  :n autor y libro
    def __init__(self, Editorial_cod, Editorial_nombre, Editorial_direccion,Libro_ISBN):
        self.Editorial_cod = Editorial_cod
        self.Editorial_nombre = Editorial_nombre
        self.Editorial_direccion = Editorial_direccion
        self.Libro_ISBN = Libro_ISBN


class EditorialSinRelacion: #constructor relacion n  :n autor y libro
    def __init__(self, Editorial_cod, Editorial_nombre, Editorial_direccion):
        self.Editorial_cod = Editorial_cod
        self.Editorial_nombre = Editorial_nombre
        self.Editorial_direccion = Editorial_direccion

class Pais:
    def __init__(self, Pais_cod, Pais_nombre, Autor_cod,Editorial_cod):#Constructor con relación 1:n entre pais ,autor,editorial
        self.Pais_cod = Pais_cod
        self.Pais_nombre = Pais_nombre
        self.Autor_cod = Autor_cod
        self.Editorial_cod = Editorial_cod
class PaisSinRelacion:
    def __init__(self, Pais_cod, Pais_nombre):#Constructor con relación 1:n entre pais ,autor,editorial
        self.Pais_cod = Pais_cod
        self.Pais_nombre = Pais_nombre


#Función para pedir datos de un usuario e insertarlos en la BBDD
def insertUsuario ():
    #Pedimos al usuario del programa los datos del usuario
    Usuario_DNI = input ("Dame el dni del Usuario ")
    Usuario_nombre = input ("Dame nombre del Usuario ")
    Usuario_calle = input("Dame calle del Usuario ") 
    Usuario_ciudad = input("Dame ciudad del Usuario ")


    c = Usuario (Usuario_DNI, Usuario_nombre, Usuario_calle, Usuario_ciudad)
    insertStatement = session.prepare ("INSERT INTO SoporteUsuario (Usuario_DNI, Usuario_nombre, Usuario_calle, Usuario_ciudad) VALUES (?, ?, ?, ?)")
    session.execute (insertStatement, [c.Usuario_DNI, c.Usuario_nombre, c.Usuario_calle, c.Usuario_ciudad])
    #consulta 5 
    insertStatementconsulta5 = session.prepare ("INSERT INTO tabla5 (Usuario_ciudad,Usuario_DNI, Usuario_nombre, Usuario_calle ) VALUES (?, ?, ?, ?)")
    session.execute (insertStatementconsulta5, [c.Usuario_ciudad, c.Usuario_DNI, c.Usuario_nombre, c.Usuario_calle])
    



#Función para pedir datos de un libro  e insertarlos en la BBDD
def insertLibro ():
    #Pedimos al usuario del programa los datos del libro
    Libro_titulo = input ("Dame el titulo del Libro ")
    Libro_anio = input ("Dame año del Libro ")
    while not Libro_anio.isnumeric():
        Libro_anio = input("Dame ISBN del Libro ")
    Libro_anio = int(Libro_anio)

    Libro_ISBN = input("Dame ISBN del Libro ") 
    while not Libro_ISBN.isalnum():
        Libro_ISBN = input("Dame ISBN del Libro ")
    Libro_temas = set() #iniciamos la colección (set) que contendra las temas de los libros  a insertar
    tema = input ("Introduzca una tema del libro, vacío para parar ")
    while (tema != ""):
        Libro_temas.add(tema)
        tema =  input ("Introduzca una tema del libro, vacío para parar ")

    c = Libro (Libro_ISBN, Libro_anio, Libro_titulo, Libro_temas)
    insertStatement = session.prepare ("INSERT INTO SoporteLibro (Libro_ISBN, Libro_titulo, Libro_anio, Libro_temas) VALUES (?, ?, ?, ?)")
    session.execute (insertStatement, [c.Libro_ISBN, c.Libro_titulo, c.Libro_anio, c.Libro_temas])


    insertStatementconsulta1 = session.prepare ("INSERT INTO tabla1 (Libro_anio, Libro_ISBN, Libro_titulo) VALUES (?, ?, ?)")
    session.execute (insertStatementconsulta1, [ c.Libro_anio,c.Libro_ISBN, c.Libro_titulo])


#Función para pedir datos de un autor e insertarlos en la BBDD
def insertAutor ():
    #Pedimos al usuario del programa los datos del autor
    Autor_nombre = input ("Dame el nombre del Autor ")

    Autor_cod = input ("Dame el codigo del Autor ")

    while not Autor_cod.isnumeric():
        Autor_cod = input ("Dame el codigo del Autor ")
    Autor_cod =int (Autor_cod)
    Autor_premios = set() #iniciamos la colección (set) que contendra los premios a insertar
    premio = input ("Introduzca una premio del Autor, vacío para parar ")
    while (premio != ""):
        Autor_premios.add(premio)
        premio = input("Introduzca una premio del Autor, vacío para parar ")

    c = AutorSinRelacion (Autor_cod, Autor_nombre, Autor_premios)

    insertStatementPrem = session.prepare ("INSERT INTO tabla7 (Autor_premio, Autor_cod, Autor_nombre, Autor_premios) VALUES (?,  ?, ?, ?)")

    #insertar en premios por autor
    for prem in Autor_premios:
         session.execute(insertStatementPrem, [prem, c.Autor_cod, c.Autor_nombre, c.Autor_premios])


#insertar ejemplar es prestado
def insertEjemplarUsuario ():
    #Pedimos al usuario del programa los datos del ejemplar
    status = input ("Dame estatus del Ejemplar ")
    nro = input("Dame el numero del Ejemplar ")
    while not nro.isnumeric():
        nro = input("Dame el numero del Ejemplar ")
    nro = int(nro)
  
    fecha = date.today()
  
    #Pedimos al usuario del programa los datos del usuario
    DNI = input("Dame DNI del usuario ")
  
    nombre = input ("Dame nombre del usuario ")
    calle = input ("Dame  calle del usuario ")
    ciudad = input ("Dame ciudad del usuario ")

    

    insertStatementEjemplar_Usuario = session.prepare ("INSERT INTO Ejemplar_Usuario (Ejemplar_status,Ejemplar_nro, Es_prestado, Usuario_DNI, Usuario_nombre, Usuario_calle,Usuario_ciudad) VALUES (?, ?, ?, ?, ?, ?,?)")
    insertStatementNumPrestamos = session.prepare ("UPDATE tabla6 SET NumPrestamos = NumPrestamos + 1 WHERE Ejemplar_nro = ?")
    session.execute(insertStatementEjemplar_Usuario, [status, nro, fecha, DNI, nombre, calle,ciudad])
    session.execute(insertStatementNumPrestamos, [nro, ])
    
    insertStatement2 = session.prepare("INSERT INTO tabla8 (Es_prestado, Ejemplar_nro,  Usuario_DNI,Usuario_nombre) VALUES (?, ?, ?, ?)")
    session.execute(insertStatement2, [fecha, nro,  DNI, nombre])

	
#insertar • Relación Corresponde-Es_prestado 
def insertLibroEjemplarUsuario ():
    
    # insertar libro
    ISBN = input("Dame el  ISBN Del Libro ")
    titulo = input("Damte el titulo del Libro ")
    año = input("Dame el año del Libro ")

    
    #insertar Ejemplar
    status = input ("Dame estatus del Ejemplar ")
    nro = input("Dame el numero del Ejemplar ")
    while not nro.isnumeric():
        nro = input("Dame el numero del Ejemplar ")
    nro = int(nro)
    #insertar es prestado
    fecha = date.today()
  
  
    DNI = input("Dame DNI del usuario ")
  
    nombre = input ("Dame nombre del usuario ")
    calle = input ("Dame  calle del usuario ")
    ciudad = input ("Dame ciudad del usuario ")

    

    insertStatementLibro_Ejemplar = session.prepare ("INSERT INTO Libro_Ejemplar (Ejemplar_status,Ejemplar_nro,Es_prestado,Libro_ISBN,Libro_titulo,Libro_anio) VALUES (?, ?, ?, ?, ?, ?)")
    insertStatementLibro_Usuario = session.prepare ("INSERT INTO Libro_Usuario (Usuario_DNI, Usuario_nombre,Usuario_calle, Usuario_ciudad,Libro_ISBN,Libro_titulo,Libro_anio) VALUES (?, ?, ?, ?, ?,?,?)")
    insertStatementNumPrestamos = session.prepare ("UPDATE tabla6 SET NumPrestamos = NumPrestamos + 1 WHERE Ejemplar_nro = ?")
    insertStatementtabla2 = session.prepare("INSERT INTO tabla2(Libro_titulo,Ejemplar_nro,Ejemplar_status) VALUES (?, ?, ?)")

    session.execute(insertStatementLibro_Ejemplar, [status, nro, fecha, ISBN, titulo, año])
    session.execute(insertStatementLibro_Usuario, [DNI,nombre,calle,ciudad,ISBN, titulo, año])
    session.execute(insertStatementNumPrestamos, [nro, ])
    session.execute(insertStatementtabla2, [titulo,nro,status])

    insertStatement2 = session.prepare("INSERT INTO tabla8 (Es_prestado, Ejemplar_nro,  Usuario_DNI,Usuario_nombre) VALUES (?, ?, ?, ?)")
    session.execute(insertStatement2, [fecha, nro,  DNI, nombre])





#insertar • Relación Corresponde-Es_prestado 
def insertLibroAutor():
    
    #insertar libro
    ISBN = input("Dame el  ISBN Del Libro ")
    titulo = input("Damte el titulo del Libro ")
    año = input("Dame el año del Libro ")
    temas = set()
    tema =input ("Dame tema del libro")
    while (tema!=''):
            temas.append(tema)
    
    #insertar Autor
    cod = input ("Dame el codigo del autor ")
    while not cod.isnumeric():
        cod = input("Dame el numero del Ejemplar ")
    nombre = input("Dame el nombre del autor ")
    premios = set()
    premio =input ("Dame tema del libro")
    while (premio!=''):
            premios.append(premio)


    

    insertStatementLibro_Ejemplar = session.prepare ("INSERT INTO tabla3 (Autor_nombre,Autor_cod,Libro_ISBN,Libro_titulo,Libro_anio) VALUES (?, ?, ?, ?, ?)")
    insertStatementLibro_Usuario = session.prepare ("INSERT INTO tabla1 (Libro_anio, Libro_ISBN,Libro_titulo) VALUES (?, ?, ?)")
  

    session.execute(insertStatementLibro_Ejemplar, [nombre, cod, ISBN, titulo, año])
    session.execute(insertStatementLibro_Usuario, [año,ISBN,titulo])


#extraer datos de los libros por ISBN
def extraerDatosLibro(Libro_ISBN):
    select = session.prepare ("SELECT * FROM SoporteLibro  WHERE Libro_ISBN = ?") #solo va a devolver una filia pero lo tratamos como si fuesen varias
    filas = session.execute (select, [Libro_ISBN,])#Importante, aunque solo haya un valor a reemplazar en el preparedstatemente, hay que poner la ','

    for fila in filas:
        c = Libro (Libro_ISBN, fila.libro_anio, fila.libro_titulo,  fila.libro_temas) #creamos instancia del cliente
        return c
#extraer datos de los libros por AÑO
    
def extraerDatosLibroaño(Libro_anio):
    select = session.prepare ("SELECT * FROM tabla1  WHERE Libro_anio = ?") #solo va a devolver una filia pero lo tratamos como si fuesen varias
    filas = session.execute (select, [Libro_anio,])#Importante, aunque solo haya un valor a reemplazar en el preparedstatemente, hay que poner la ','
    Libros = []
    for fila in filas:
        c = Libro ( fila.libro_isbn, Libro_anio,fila.libro_titulo,'') #creamos instancia del cliente
        Libros.append(c)
    
    return Libros
#extraer datos de los libros Y Ejemplar por titulo
def extraerDatosLibroEjemplarportitulo(titulo):
    select = session.prepare ("SELECT * FROM tabla2  WHERE Libro_titulo = ?") #solo va a devolver una filia pero lo tratamos como si fuesen varias
    filas = session.execute (select, [titulo,])#Importante, aunque solo haya un valor a reemplazar en el preparedstatemente, hay que poner la ','

    for fila in filas:
        c = Ejemplar (fila.ejemplar_nro, fila.ejemplar_status, '',  titulo) #creamos instancia del ejemplar
        return c       
#extraer datos de autor por el premio
     
def extraerDatosAutor(Autor_premio) :
    select = session.prepare ("SELECT * FROM tabla7  WHERE Autor_premio = ?") #solo va a devolver una filia pero lo tratamos como si fuesen varias
    filas = session.execute (select, [Autor_premio,])#Importante, aunque solo haya un valor a reemplazar en el preparedstatemente, hay que poner la ','
    autores = []
    for fila in filas:
        a = AutorSinRelacion(fila.autor_cod, fila.autor_nombre, fila.autor_premios) #creamos instancia del autor sin relacion
        autores.append(a)
    return autores
#Función que procesa la información de un libro dado por el usuario y la muestra
def consultaLibroPorId():
    id = input("Dame ID del libro ") #Esto puede ser sustituido por uuid automatico o extraer MAX (id)
    while not id.isalnum():
        id = input("Dame ID del libro ")
    #id =int (id)
    Libro = extraerDatosLibro (id)
    if (Libro != None): #si el cliente no existe no mostramos nada
        print ("Año: ", Libro.Libro_anio)
        print ("Titulo: ", Libro.Libro_titulo)
        print ("Temas: ", Libro.Libro_temas)

#Función que extrae informacion de datos de un autor y el libro por el nombre del autor
def extraerDatosAutorLibro(Autorlibro):
    select = session.prepare("select  * from tabla3 where Autor_nombre = ?")
    filas = session.execute(select,[Autorlibro,])
    libros = []
    for fila in filas :
        a = Autor(fila.Autor_cod,fila.Autor_nombre,'',fila.Libro_ISBN,fila.Libro_titulo,fila.Libro_anio)
        libros.append(a)
    return libros
#funcion para consultar la tabla 3 
def consulta3LibroEscritosporunAutor():
    Autor = input("Dame nombre del autor del libro ") #Esto puede ser sustituido por uuid automatico o extraer MAX (id)

    
    AutorLibros = extraerDatosAutorLibro(Autor)

    for   AutorLibro  in AutorLibros:
        if (AutorLibro != None): #si el cliente no existe no mostramos nada
                print ("Nombre : ", AutorLibro.Autor_nombre)
                print ("codigo: ", AutorLibro.Autor_cod)
                print ("Libro ISBN: ", AutorLibro.Libro_ISBN)
                print ("Libro Titutlo: ", AutorLibro.Libro_titulo)
                print ("Libro año : ", AutorLibro.Libro_año)
#funcion para consultar la tabla 7

def consulta7Autorpremio():
    Premio = input("Dame el premio del autor ") #Esto puede ser sustituido por uuid automatico o extraer MAX (id)

    
    Autores= extraerDatosAutor(Premio)

    for   Autor  in Autores:
        if (Autor != None): #si el autor no existe no mostramos nada
                print ("Nombre : ", Autor.Autor_nombre)
                print ("codigo: ", Autor.Autor_cod)
                print ("premios: ", Autor.Autor_premios)
#funcion para consultar la tabla 2

def consulta2LibroEjemplarportitulo():
    titulo = input("Dame titulo del libro ") #Esto puede ser sustituido por uuid automatico o extraer MAX (id)

    
    LibroEjemplar = extraerDatosLibroEjemplarportitulo(titulo)
    if (LibroEjemplar != None): #si el cliente no existe no mostramos nada
            print ("Titulo: ", LibroEjemplar.Libro_titulo)
            print ("nro: ", LibroEjemplar.Ejemplar_numero)
            print ("Status: ", LibroEjemplar.Ejemplar_status)
#funcion para consultar la tabla 1
def consultaLibroPoraño():
    anio = input("Dame año del libro ") #Esto puede ser sustituido por uuid automatico o extraer MAX (id)
    while not anio.isnumeric():
        anio = input("Dame ID del libro ")
    anio =int (anio)
    Libros = extraerDatosLibroaño (anio)

    for Libro in Libros:
        if (Libro != None): #si el cliente no existe no mostramos nada
            print ("Año: ", Libro.Libro_anio)
            print ("ISBN: ", Libro.Libro_ISBN)
            print ("Titulo: ", Libro.Libro_titulo)

#extraer datos de usuario por dni            
def extraerDatosUsuario(Usuario_DNI):
    select = session.prepare ("SELECT * FROM SoporteUsuario  WHERE Usuario_DNI = ?") #solo va a devolver una filia pero lo tratamos como si fuesen varias
    filas = session.execute (select, [Usuario_DNI,])#Importante, aunque solo haya un valor a reemplazar en el preparedstatemente, hay que poner la ','
    for fila in filas:
        c = Usuario (Usuario_DNI, fila.usuario_nombre, fila.usuario_calle,  fila.usuario_ciudad) #creamos instancia del cliente
        return c
#Función que muestra la informacion de un usuario por su dni
def consultaUsuarioPorId():
    id = input("Dame Dni del Usuario ") #Esto puede ser sustituido por uuid automatico o extraer MAX (id)
    
    #id =int (id)
    Usuario = extraerDatosUsuario (id)
    if (Usuario != None): #si el cliente no existe no mostramos nada
        print ("Nombre: ", Usuario.Usuario_nombre)
        print ("Calle: ", Usuario.Usuario_calle)
        print ("Ciudad: ", Usuario.Usuario_ciudad)        

#Función que  extrae los datos de un libro por año
def extraerañoLibro (idProducto):
    select = session.prepare ("SELECT Libro_anio FROM SoporteLibro WHERE Libro_ISBN = ?") #solo va a devolver una filia pero lo tratamos como si fuesen varias
    años = [] #donde almacenaremos el retorno de la consulta
    filas = session.execute (select, [idProducto,]) #Importante, aunque solo haya un valor a reemplazar en el preparedstatemente, hay que poner la ','
    for fila in filas: #procesando todos los clientes que compraron ese producto
        años.append(fila.Libro_anio) #como solo queremos los Ids, simplemente vamos añadiendo los valores
    return años


#Función que actualzia el año de un libro dando el isbn del libro
def actualizarAñoLibro ():
    año = input("Dame año del libro ")
    while not año.isnumeric():
        año = input("Dame año del libro ")
    año = int(año)
    ISBN = input("Dame ISBN del Libro ")
    
    infoLibro = extraerDatosLibro(ISBN) 

    
    borrarSoporteLibro = session.prepare ("DELETE FROM SoporteLibro  WHERE Libro_ISBN = ? ")
    session.execute(borrarSoporteLibro, [ISBN,])
    borrarConsulta1 = session.prepare ("DELETE FROM tabla1  WHERE Libro_ISBN = ? and Libro_anio = ? ")
    session.execute(borrarConsulta1, [ISBN,int(infoLibro.Libro_anio)])

    insertStatementSoporteLibro = session.prepare("INSERT INTO SoporteLibro (Libro_ISBN, Libro_titulo, Libro_anio, Libro_temas) VALUES (?, ?, ?, ?)")
    session.execute(insertStatementSoporteLibro, [ISBN,infoLibro.Libro_titulo,año,infoLibro.Libro_temas])

    insertStatementConsulta1  = session.prepare("INSERT INTO tabla1 (Libro_anio, Libro_ISBN, Libro_titulo) VALUES (?, ?, ?)")
    session.execute(insertStatementConsulta1, [año, ISBN, infoLibro.Libro_titulo])
# Borrar todos los autores que hayan ganado un premio en específico
def BorrarAutores() :
    premio = input("dame el premio en especifico ")
    infoAutores  = extraerDatosAutor(premio)
    for infoAutor in infoAutores :
        print(infoAutor.Autor_cod)
        borrarTabla7premio = session.prepare ("DELETE FROM tabla7  WHERE Autor_premio = ? and Autor_cod= ? ")
        session.execute(borrarTabla7premio, [premio,infoAutor.Autor_cod])
while (numero != 0):
    print ("Introduzca un número para ejecutar una de las siguientes operaciones:")
    print ("1. Insertar un libro")
    print ("2. Insertar un usuario")
    print ("3. Insertar insertAutor")
    print ("4. Insertar relación entre ejemplar es prestado usuario (todos datos)")
    print ("5. Consultar datos libro según su id")
    print ("6. Consultar datos de usuario por DNI")
    print ("7. Insertar relación entre Libro Relación Corresponde Ejemplar  -Es_prestado Usuario (todos datos)")
    print ("8. Actualizar año libro por ISBN")
    print ("9. Borrar Autores por premio")
    print ("10. Consultar datos libro según su año(consulta 1)")
    print ("11. Consultar ejemplares de un libro según el titulo de este(consulta 2)")
    print ("12. obtener toda la información de los libros escritor por un autor buscando por el nombre del autor (consulta3)")
    print ("13. insertar libro autor (tabla3)")
    print ("14.Obtener la información de los autores que hayan ganado un premio específico (consulta 7)")

    # print ("9. Insertar pedido producto")

    print ("0. Cerrar aplicación")

    numero = int (input()) #Pedimos numero al usuario
    if (numero == 1):
        insertLibro()
    elif (numero == 2):
         insertUsuario()
    elif (numero == 3):
         insertAutor()
    elif (numero == 4):
          insertEjemplarUsuario()
    #     insertClientePedidosProductosSelectCliente()
    elif (numero == 5):
       consultaLibroPorId()
    elif (numero == 6):
         consultaUsuarioPorId()
    elif (numero == 7):
         insertLibroEjemplarUsuario()
    elif (numero == 8):
         actualizarAñoLibro()
    elif (numero ==9):
        BorrarAutores()
    elif (numero ==10):
        consultaLibroPoraño()
    elif (numero ==11):
        consulta2LibroEjemplarportitulo()
    elif(numero==12 ):
        consulta3LibroEscritosporunAutor()
    elif(numero==13) :
        insertLibroAutor()
    elif (numero ==14):
        consulta7Autorpremio()
    else:
        print ("Número incorrecto")
cluster.shutdown() #cerramos conexion
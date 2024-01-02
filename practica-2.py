#práctica 2
#alumno: Canaza Chagua Yoel Nhelio

import csv

class ErrorLibroNoEncontrado(Exception):
    pass

class ErrorLibroNoDisponible(Exception):
    pass

class ErrorLibroYaDisponible(Exception):
    pass

class Libro:
    def __init__(self, titulo, autor, anio_publicacion):
        self.titulo = titulo
        self.autor = autor
        
        self.disponible = True

        if isinstance(anio_publicacion, int) and anio_publicacion > 0:
            self.anio_publicacion = anio_publicacion
        else:
            print("El año de publicación debe ser un número entero positivo.")
            self.anio_publicacion = int(input('vuelve a ingresar el año de publicación: '))

    def __str__(self):
        disponibilidad = "disponible" if self.disponible else "prestado"
        return f"{self.titulo} - {self.autor} ({self.anio_publicacion}), {disponibilidad}"
    
    def actualizar_informacion(self, new_titulo, new_autor, new_year_pub):
        self.titulo = new_titulo
        self.autor = new_autor
        self.anio_publicacion = new_year_pub

class Biblioteca:
    def __init__(self):
        self.libros = []

    def __str__(self):
        return f"{self.conteo_libros()}"

    def agregar_libro(self, libro):
        self.libros.append(libro)
        print(f"Libro '{libro.titulo}' agregado a la biblioteca.")

    def conteo_libros(self):
        num_libros = len(self.libros)
        return f"Número de libros en la biblioteca: {num_libros}"

    def buscar_libro(self, titulo):
        # ejercicio: hacer que el método sea insensible a mayúsculas
        # o minúsculas al buscar por título
        
        for libro in self.libros:
            if libro.titulo.lower() == titulo.lower():
                return libro
        raise ErrorLibroNoEncontrado(f'No se encontró ningún libro llamado {titulo}')
        # return None
    
    def buscar_libro_autor(self, autor):
        # ejercicio búsqueda por autor
        for libro in self.libros:
            if libro.autor.lower() == autor.lower():
                return libro
        raise ErrorLibroNoEncontrado(f'No se encontró ningún libro de autor {autor}')

    
    def actualizar_informacion_libros(self, titulo, new_titulo, new_autor, new_year_pub):
        try:
            libro = self.buscar_libro(titulo)
        except ErrorLibroNoEncontrado as e:
            print(f'Error {e}')
        else:
            libro.actualizar_informacion(new_titulo, new_autor, new_year_pub)

        '''if libro:
        else:
            print(f"No se encontró el libro con título '{titulo}' en la biblioteca.")'''



    def prestar_libro(self, titulo):

        try:
            libro = self.buscar_libro(titulo)
        except ErrorLibroNoEncontrado:
            libro = None

        try:
            libro_autor = self.buscar_libro_autor(titulo)
        except ErrorLibroNoEncontrado:
            libro_autor = None

        try:
            if libro:
                if libro.disponible:
                    libro.disponible = False
                    print(f"Libro '{libro.titulo}' prestado.")
                else:
                    raise ErrorLibroNoDisponible(f'El libro {libro.titulo} no está disponible para ser prestado')
            elif libro_autor:
                if libro_autor.disponible:
                    libro_autor.disponible = False
                    print(f"Libro '{libro_autor.titulo}' prestado.")
                else:
                    print(f"El libro de autor '{libro_autor.titulo}' no está disponible en este momento.")
                    raise ErrorLibroNoDisponible(f'El libro {libro_autor.titulo} no está disponible para ser prestado')
            else:
                raise ErrorLibroNoEncontrado(f'No se encontró el libro con nombre o autor {titulo} en la biblioteca')
        except (ErrorLibroNoDisponible, ErrorLibroNoEncontrado) as e:
            print(f'Error {e}')

    def devolver_libro(self, titulo):

        try:
            libro = self.buscar_libro(titulo)
        except ErrorLibroNoEncontrado:
            libro = None

        try:
            libro_autor = self.buscar_libro(titulo)
        except ErrorLibroNoEncontrado:
            libro_autor = None

        try:
            if libro:
                if not libro.disponible:
                    libro.disponible = True
                    print(f"Libro '{libro.titulo}' devuelto.")
                else:
                    raise ErrorLibroYaDisponible(f"El libro '{libro.titulo} ya está disponible en la biblioteca")
            elif libro_autor:
                if not libro_autor.disponible:
                    libro_autor.disponible = True
                    print(f"Libro '{libro_autor.titulo}' devuelto.")
                else:
                    raise ErrorLibroYaDisponible(f"El libro '{libro_autor.titulo} ya está disponible en la biblioteca")
            else:
                raise ErrorLibroNoEncontrado(f"No se encontró el libro con título o autor '{titulo}' en la biblioteca.")
        except (ErrorLibroYaDisponible, ErrorLibroNoEncontrado) as e:
            print(f'Error {e}')
    
    def ordenar_libros_titulo(self):
        return sorted(self.libros, key=lambda libro: libro.titulo)
    
    def ordenar_libros_publicacion(self):
        return sorted(self.libros, key=lambda libro: libro.anio_publicacion)
    

    def guardar_biblioteca_csv(self, archivo):
        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Escribir el encabezado
                writer.writerow(["Titulo", "Autor", "Anio de Publicacion", "Disponible"])
                # Escribir los datos de cada libro
                for libro in self.libros:
                    writer.writerow([libro.titulo, libro.autor, libro.anio_publicacion, libro.disponible])
            print("Información de la biblioteca guardada en formato CSV con éxito.")
        except Exception as e:
            print(f"Error al guardar la biblioteca en formato CSV: {e}")

    def cargar_biblioteca_csv(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Ignorar el encabezado
                next(reader)
                # Leer los datos de cada libro
                for row in reader:
                    titulo, autor, anio_publicacion, disponible = row
                    anio_publicacion = int(anio_publicacion)
                    disponible = disponible.lower() == 'true'
                    libro = Libro(titulo, autor, anio_publicacion)
                    libro.disponible = disponible
                    self.libros.append(libro)
            print("Información de la biblioteca cargada desde formato CSV con éxito.")
        except FileNotFoundError:
            print("No se encontró el archivo. La biblioteca se mantendrá vacía.")
        except Exception as e:
            print(f"Error al cargar la biblioteca desde formato CSV: {e}")

# Crear algunos libros
libro1 = Libro("Python Crash Course", "Eric Matthes", 2015)
libro2 = Libro("Clean Code", "Robert C. Martin", 2008)
libro3 = Libro("The Art of Computer Programming", "Donald E. Knuth", 1968)

# Crear una biblioteca
biblioteca = Biblioteca()

# Agregar libros a la biblioteca
biblioteca.agregar_libro(libro1)
biblioteca.agregar_libro(libro2)
biblioteca.agregar_libro(libro3)
# Ejercicio: agregar dos libros más a la biblioteca:
libro4 = Libro("Introduction to Algorithms", "Thomas Cormen", 1989)
libro5 = Libro("Competitive Programming Book", "Halim", 2018)
biblioteca.agregar_libro(libro4)
biblioteca.agregar_libro(libro5)
biblioteca.prestar_libro("introduction to algorithms")
biblioteca.devolver_libro("competitive programming Book")


# Realizar operaciones de préstamo y devolución
biblioteca.prestar_libro("Clean Code")
biblioteca.devolver_libro("Python Crash Course")
biblioteca.prestar_libro("The Art of Computer Programming")
biblioteca.devolver_libro("eric matthes")

# actualizando informacion
biblioteca.actualizar_informacion_libros("Competitive Programming Book", "CompProgBook", "Hal", 8102)

# Mostrar información de los libros en la biblioteca
print("\nEstado actual de la biblioteca:")
for libro in biblioteca.libros:
    print(libro)

print(biblioteca)



print('\n------')
print('BIBLIOTECA')
print('1. Buscar libro por autor')
print('2. Buscar libro por título')
print('3. Cambiar la información de un libro')
print('4. Prestar libro')
print('5. Devolver libro')

opcion = int(input('\n Escribe un número del 1 al 5 para seleccionar tu opción: '))

if opcion == 1:
    nombre_autor = input('Ingrese el nombre del autor: ')
    try:
        libro_encontrado = biblioteca.buscar_libro_autor(nombre_autor)
    except ErrorLibroNoEncontrado as e:
        print(f'Error: {e}')
        libro_encontrado = None
    else:
        print('El libro con ese autor es: ', biblioteca.buscar_libro_autor(nombre_autor))

elif opcion == 2:
    nombre_libro = input('Ingrese el nombre del libro: ')
    try:
        libro_encontrado = biblioteca.buscar_libro(nombre_libro)
    except ErrorLibroNoEncontrado as e:
        print(f'Error: {e}')
        libro_encontrado = None
    else:
        print('El libro con ese nombre es: ', biblioteca.buscar_libro(nombre_libro))
elif opcion == 3:
    nombre_libro = input('Ingrese el nombre del libro: ')
    print(f"El libro que has escogido es {biblioteca.buscar_libro(nombre_libro)}")
    new_titulo = input('Ingrese el nuevo nombre de libro: ')
    new_autor = input('Ingrese el nuevo nombre de autor: ')
    new_year_pub = input('Ingrese el nuevo anio de publicación: ')
    biblioteca.actualizar_informacion_libros(nombre_libro, new_titulo, new_autor, new_year_pub)
    print(f"Los nuevos datos del libro son {biblioteca.buscar_libro(new_titulo)}")
elif opcion == 4:
    for libro in biblioteca.libros:
        print(libro)

    nombre_titulo_autor = input('\n Ingrese el nombre o el autor del libro que quiere prestar: ')
    biblioteca.prestar_libro(nombre_titulo_autor)
elif opcion == 5:
    for libro in biblioteca.libros:
        print(libro)
        
    nombre_titulo_autor = input('\n Ingrese el nombre o el autor del libro que quiere devolver: ')
    biblioteca.devolver_libro(nombre_titulo_autor)


biblioteca_ordenada_titulo = biblioteca.ordenar_libros_titulo()
print("\nLIBROS ORDENADOS POR TÍTULO:")
for libro in biblioteca_ordenada_titulo:
    print(libro)

biblioteca_ordenada_publicacion = biblioteca.ordenar_libros_publicacion()
print("\nLIBROS ORDENADOS POR FECHA DE PUBLICACIÓN:")
for libro in biblioteca_ordenada_publicacion:
    print(libro)

print('\n')
# Guardamos la biblioteca en un archivo CSV
biblioteca.guardar_biblioteca_csv("biblioteca.csv")



# Cargamos la información desde el archivo CSV
biblioteca_importada = Biblioteca()
biblioteca_importada.cargar_biblioteca_csv("biblioteca.csv")

print('-' * 8)
print('MOSTRANDO LOS LIBROS DE LA BIBLIOTECA IMPORTADA:')
for libro in biblioteca_importada.libros:
    print(libro)
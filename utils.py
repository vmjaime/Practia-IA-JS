def carga(filename):
    try:
        with open(filename,"rb") as archivo:
            datos=archivo.read()
            return datos
    except IOError as e:
        print(f"Error al cargar el archivo:{e}")
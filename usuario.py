class Usuario:
    def __init__(self, nombre: str, dni: str, ruta_imagen: str = None, encoding: list = None):
        self.nombre = nombre.lower()
        self.dni = dni.upper()
        self.ruta_imagen = ruta_imagen
        self.encoding = encoding

    "Convierte el usuario a un diccionario listo para almacenar en JSON"
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "dni": self.dni,
            "ruta_imagen": self.ruta_imagen,
            "encoding": self.encoding
        }


    "Crea un objeto Usuario a partir de un diccionario cargado de JSON"
    @staticmethod
    def from_dict(data: dict):
        return Usuario(
            nombre=data.get("nombre"),
            dni=data.get("dni"),
            ruta_imagen=data.get("ruta_imagen"),
            encoding=data.get("encoding")
        )

    def __str__(self):
        return f"Usuario(nombre={self.nombre}, dni={self.dni})"
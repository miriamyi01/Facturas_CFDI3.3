# models/usuario.py

"""
Este archivo define la clase Usuario, que representa a los usuarios en la base de datos.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Crear una clase base declarativa de SQLAlchemy
# Esta clase será la superclase de todos los modelos de la base de datos
Base = declarative_base()

class Usuario(Base):
    """
    Clase que representa la tabla 'usuarios' en la base de datos.

    Atributos:
        id (int): La clave primaria de la tabla.
        nombre_usuario (str): El nombre de usuario del usuario.
        contraseña_hash (str): El hash de la contraseña del usuario.
        correo_electronico (str): El correo electrónico del usuario.
        rfc_receptor (str): El RFC del receptor del usuario.
        domicilio (str): El domicilio del usuario.
    """
    # El nombre de la tabla en la base de datos
    __tablename__ = 'usuarios'

    # Las columnas de la tabla
    # Cada atributo representa una columna en la tabla de la base de datos
    id = Column(Integer, primary_key=True)  # La columna id es la clave primaria
    nombre_usuario = Column(String(255), unique=True, nullable=False)  # La columna nombre_usuario debe ser única y no puede ser nula
    contraseña_hash = Column(String(255), nullable=False)  # La columna contraseña_hash no puede ser nula
    correo_electronico = Column(String(255), unique=True, nullable=False)  # La columna correo_electronico debe ser única y no puede ser nula
    rfc_receptor = Column(String(20), unique=True, nullable=False)  # La columna rfc_receptor debe ser única, no puede ser nula y debe tener exactamente 13 caracteres
    domicilio = Column(String(255), nullable=False)  # La columna domicilio no puede ser nula
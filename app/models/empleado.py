# models/empleado.py

"""
Este archivo define la clase Empleado, que representa a los empleados en la base de datos.
"""

from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Crear una clase base declarativa de SQLAlchemy
# Esta clase será la superclase de todos los modelos de la base de datos
Base = declarative_base()


class Puesto(Base):
    """
    Clase para representar el Puesto de un Empleado.
    """
    __tablename__ = 'puestos'

    id = Column(Integer, primary_key=True)  # Identificador único para cada puesto
    nombre = Column(String(255), nullable=False)  # Nombre del puesto
    departamento_id = Column(String(3), ForeignKey('departamento.id'))  # ID del departamento al que pertenece el puesto
    riesgo_clave = Column(String(3), ForeignKey('riesgo.clave'))  # ID del riesgo al que pertenece el puesto

    empleados = relationship("Empleado", back_populates="puesto")  # Relación con la tabla Empleado: un puesto puede tener múltiples empleados


class Departamento(Base):
    """
    Clase para representar el Departamento de un Empleado.
    """
    __tablename__ = 'departamento'

    id = Column(String(3), primary_key=True, unique=True, nullable=False)  # Clave única del departamento
    nombre = Column(String(255), nullable=False)  # Nombre del departamento

    empleados = relationship("Empleado", back_populates="departamento")  # Relación con la tabla Empleado: un departamento puede tener múltiples empleados


class Riesgo(Base):
    """
    Clase para representar el Riesgo asociado a un Puesto.
    """
    __tablename__ = 'riesgo'

    clave = Column(String(3), primary_key=True, unique=True, nullable=False)  # Clave única del riesgo
    descripcion = Column(String(255), nullable=False)  # Descripción del riesgo

    empleados = relationship("Empleado", back_populates="riesgo")  # Relación con la tabla Empleado: un riesgo puede estar asociado a múltiples empleados


class Jornada(Base):
    """
    Clase para representar la Jornada de un Empleado.
    """
    __tablename__ = 'jornada'

    clave = Column(String(3), primary_key=True, unique=True, nullable=False)  # Clave única de la jornada
    descripcion = Column(String(255), nullable=False)  # Descripción de la jornada

    empleados = relationship("Empleado", back_populates="jornada")  # Relación con la tabla Empleado: una jornada puede estar asociada a múltiples empleados


class Contrato(Base):
    """
    Clase para representar el Contrato de un Empleado.
    """
    __tablename__ = 'contrato'

    clave = Column(String(3), primary_key=True, unique=True, nullable=False)  # Clave única del contrato
    descripcion = Column(String(255), nullable=False)  # Descripción del contrato

    empleados = relationship("Empleado", back_populates="contrato")  # Relación con la tabla Empleado: un contrato puede estar asociado a múltiples empleados


class Periodicidad(Base):
    """
    Clase para representar la Periodicidad de pago de un Empleado.
    """
    __tablename__ = 'periodicidad'

    clave = Column(String(3), primary_key=True, unique=True, nullable=False)  # Clave única de la periodicidad
    descripcion = Column(String(255), nullable=False)  # Descripción de la periodicidad

    empleados = relationship("Empleado", back_populates="periodicidad")  # Relación con la tabla Empleado: una periodicidad puede estar asociada a múltiples empleadospulates="periodicidad")  # Relación con la tabla Empleado


class Empleado(Base):
    """
    Representa a un empleado en el sistema.

    Atributos:
        numero_empleado (str): Identificador único para cada empleado.
        curp (str): CURP (Clave Única de Registro de Población) del empleado.
        nss (str): NSS (Número de Seguridad Social) del empleado.
        fecha_ingreso (datetime.date): Fecha de ingreso del empleado.
        sueldo_base (decimal.Decimal): Sueldo base del empleado.
        puesto_id (int): ID del puesto del empleado.
        departamento_id (str): ID del departamento del empleado.
        riesgo_id (str): ID del nivel de riesgo del empleado.
        tipo_jornada (str): Tipo de jornada laboral del empleado.
        tipo_contrato (str): Tipo de contrato del empleado.
        periodicidad_pago (str): Periodicidad de pago del empleado.

    Relaciones:
        puesto (Puesto): El puesto del empleado.
        departamento (Departamento): El departamento del empleado.
        riesgo (Riesgo): El nivel de riesgo del empleado.
        jornada (Jornada): La jornada laboral del empleado.
        contrato (Contrato): El tipo de contrato del empleado.
        periodicidad (Periodicidad): La periodicidad de pago del empleado.
    """

    # El nombre de la tabla en la base de datos
    __tablename__ = 'empleados'

    # Las columnas de la tabla
    # Cada atributo representa una columna en la tabla de la base de datos
    numero_empleado = Column(String(18), primary_key=True, unique=True)  # Identificador único para cada empleado
    curp = Column(String(18), unique=True, nullable=False)  # CURP del empleado
    nss = Column(String(11), unique=True, nullable=False)  # NSS del empleado
    fecha_ingreso = Column(Date, nullable=False)  # Fecha de ingreso del empleado
    sueldo_base = Column(DECIMAL(10, 2), nullable=False)  # Sueldo base del empleado
    puesto_id = Column(Integer, ForeignKey('puestos.id'), nullable=False)  # ID del puesto del empleado
    departamento_id = Column(String(3), ForeignKey('departamento.id'), nullable=False)  # ID del departamento del empleado
    riesgo_id = Column(String(3), ForeignKey('riesgo.clave'), nullable=False)  # ID del riesgo del empleado
    tipo_jornada = Column(String(3), ForeignKey('jornada.clave'), nullable=False)  # Tipo de jornada del empleado
    tipo_contrato = Column(String(3), ForeignKey('contrato.clave'), nullable=False)  # Tipo de contrato del empleado
    periodicidad_pago = Column(String(3), ForeignKey('periodicidad.clave'), nullable=False)  # Periodicidad de pago del empleado

    puesto = relationship("Puesto", back_populates="empleados")  # Relación con la tabla 'puestos'
    departamento = relationship("Departamento", back_populates="empleados")  # Relación con la tabla 'departamento'
    riesgo = relationship("Riesgo", back_populates="empleados")  # Relación con la tabla 'riesgo'
    jornada = relationship("Jornada", back_populates="empleados")  # Relación con la tabla 'jornada'
    contrato = relationship("Contrato", back_populates="empleados")  # Relación con la tabla 'contrato'
    periodicidad = relationship("Periodicidad", back_populates="empleados")  # Relación con la tabla 'periodicidad'
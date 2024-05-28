# models/recibo.py

"""
Este archivo define las clases que representan entidades relacionadas con los recibos de nómina en la aplicación.
Cada clase define una tabla en la base de datos utilizando SQLAlchemy para el mapeo objeto-relacional (ORM).
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, LargeBinary, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Declaramos una base para las clases de SQLAlchemy
Base = declarative_base()

class Empleado(Base):
    """
    Clase para representar a un empleado en la empresa.
    """
    __tablename__ = 'empleados'

    numero_empleado = Column(String(18), primary_key=True)  # Identificador único para cada empleado
    curp = Column(String(18), unique=True, nullable=False)  # CURP del empleado
    nss = Column(String(11), unique=True, nullable=False)  # NSS del empleado
    fecha_ingreso = Column(Date, nullable=False)  # Fecha de ingreso del empleado
    sueldo_base = Column(Numeric(10, 2), nullable=False)  # Sueldo base del empleado
    puesto_id = Column(Integer, ForeignKey('puestos.id'), nullable=False)  # ID del puesto del empleado
    departamento_id = Column(String(3), ForeignKey('departamento.id'), nullable=False)  # ID del departamento del empleado
    riesgo_id = Column(String(3), ForeignKey('riesgo.clave'), nullable=False)  # ID del riesgo del empleado
    tipo_jornada = Column(String(3), ForeignKey('jornada.clave'), nullable=False)  # Tipo de jornada del empleado
    tipo_contrato = Column(String(3), ForeignKey('contrato.clave'), nullable=False)  # Tipo de contrato del empleado
    periodicidad_pago = Column(String(3), ForeignKey('periodicidad.clave'), nullable=False)  # Periodicidad de pago del empleado

    recibos_nomina = relationship("ReciboNomina", back_populates="empleado")  # Relación con la tabla ReciboNomina: un empleado puede tener múltiples recibos de nómina


# class UsoDestinoCfdi(Base):
#     """
#     Clase para representar el uso o destino de un CFDI en una factura.
#     """
#     __tablename__ = 'uso_destino_cfdi'
#     
#     clave = Column(Integer, primary_key=True)  # Clave única del uso o destino CFDI
#     descripcion = Column(String(255), nullable=False)  # Descripción del uso o destino CFDI
#     
#     recibos_nomina = relationship("ReciboNomina", back_populates="uso_destino_cfdi")  # Relación con la tabla ReciboNomina: un uso o destino CFDI puede estar asociado a múltiples recibos de nómina
# 
# 
# class TipoComprobante(Base):
#     """
#     Clase para representar el tipo de comprobante de un recibo de nómina.
#     """
#     __tablename__ = 'tipo_comprobante'
#     
#     clave = Column(Integer, primary_key=True)  # Clave única del tipo de comprobante
#     descripcion = Column(String(255), nullable=False)  # Descripción del tipo de comprobante
#     
#     recibos_nomina = relationship("ReciboNomina", back_populates="tipo_comprobante")  # Relación con la tabla ReciboNomina: un tipo de comprobante puede estar asociado a múltiples recibos de nómina


class RegimenLaboral(Base):
    """
    Clase para representar el régimen laboral de un empleado.
    """
    __tablename__ = 'regimen_laboral'
    
    clave = Column(String(3), primary_key=True, unique=True)  # Clave única del régimen laboral
    descripcion = Column(String(255), nullable=False)  # Descripción del régimen laboral

    recibos_nomina = relationship("ReciboNomina", back_populates="regimen_laboral")  # Relación con la tabla ReciboNomina: un régimen laboral puede estar asociado a múltiples recibos de nómina


# class MetodoPago(Base):
#     """
#     Clase para representar los métodos de pago que pueden ser utilizados en un recibo de nómina.
#     """
#     __tablename__ = 'metodos_pago'
# 
#     clave = Column(String(3), primary_key=True, unique=True, nullable=False)  # Clave única del método de pago
#     descripcion = Column(String(255), nullable=False)  # Descripción del método de pago
#     
#     recibos_nomina = relationship("ReciboNomina", back_populates="metodo_pago")  # Relación con la tabla ReciboNomina: un método de pago puede estar asociado a múltiples recibos de nómina
# 
# 
# class FormaPago(Base):
#     """
#     Clase para representar las formas de pago que pueden ser utilizadas en un recibo de nómina.
#     """
#     __tablename__ = 'formas_pago'
# 
#     clave = Column(String(2), primary_key=True, unique=True, nullable=False)  # Clave única de la forma de pago
#     descripcion = Column(String(255), nullable=False)  # Descripción de la forma de pago
#     
#     recibos_nomina = relationship("ReciboNomina", back_populates="forma_pago")  # Relación con la tabla ReciboNomina: una forma de pago puede estar asociada a múltiples recibos de nómina


class Banco(Base):
    """
    Clase para representar el banco de un empleado.
    """
    __tablename__ = 'banco'
    
    clave = Column(String(3), primary_key=True, unique=True)  # Clave única del banco
    descripcion = Column(String(255), nullable=False)  # Descripción del banco

    recibos_nomina = relationship("ReciboNomina", back_populates="banco")  # Relación con la tabla ReciboNomina: un banco puede estar asociado a múltiples recibos de nómina
    
    
class Percepcion(Base):
    """
    Clase para representar las percepciones de un recibo de nómina.
    """
    __tablename__ = 'percepciones'
    
    clave = Column(String(3), primary_key=True, unique=True)  # Clave única de la percepción
    descripcion = Column(String(255), nullable=False)  # Descripción de la percepción

    recibos_nomina = relationship("ReciboNomina", back_populates="percepciones")  # Relación con la tabla ReciboNomina: una percepción puede estar asociada a múltiples recibos de nómina


class Deduccion(Base):
    """
    Clase para representar las deducciones de un recibo de nómina.
    """
    __tablename__ = 'deducciones'
    
    clave = Column(String(3), primary_key=True, unique=True)  # Clave única de la deducción
    descripcion = Column(String(255), nullable=False)  # Descripción de la deducción

    recibos_nomina = relationship("ReciboNomina", back_populates="deducciones")  # Relación con la tabla ReciboNomina: una deducción puede estar asociada a múltiples recibos de nómina


class ReciboPDF(Base):
    """
    Clase para representar el PDF de un recibo de nómina.
    """
    __tablename__ = 'recibos_pdf'
    
    id = Column(Integer, primary_key=True)  # Identificador único para cada recibo PDF
    id_recibo = Column(Integer, ForeignKey('recibos_nomina.id'), nullable=False)  # ID del recibo de nómina asociado
    pdf = Column(LargeBinary, nullable=False)  # PDF del recibo de nómina
    
    recibos_nomina = relationship("ReciboNomina", back_populates="recibos_pdf")  # Relación con la tabla ReciboNomina: un recibo PDF puede estar asociado a múltiples recibos de nómina


class Recibo(Base):
    """
    Clase para representar las facturas en la aplicación.
    """
    __tablename__ = 'recibos_nomina'

    class ReciboNomina(Base):
        __tablename__ = 'recibos_nomina'
    
        id = Column(Integer, primary_key=True)  # Identificador único para cada recibo
        nombre_empresa = Column(String(50), default='FARMACIAS DE DIOS', nullable=False)  # Nombre de la empresa
        # uso_destino_cfdi_clave = Column(Integer, ForeignKey('uso_destino_cfdi.clave'), nullable=False)  # Clave del uso o destino CFDI
        lugar_expedicion = Column(String(20), default='CIUDAD DE MÉXICO', nullable=False)  # Lugar de expedición de la factura
        fecha_expedicion = Column(DateTime, nullable=False)  # Fecha de expedición de la factura    
        rfc_emisor = Column(String(20), default='FARA2402035H8', nullable=False)  # RFC del emisor
        # tipo_comprobante_clave = Column(Integer, ForeignKey('tipo_comprobante.clave'), nullable=False)  # Clave del tipo de comprobante
        regimen_laboral_clave = Column(Integer, ForeignKey('regimen_laboral.clave'), nullable=False)  # Clave del régimen laboral
        empleado = Column(String(10), ForeignKey('empleados.numero_empleado'), nullable=False)  # Numero de empleado
        fecha_pago = Column(DateTime, nullable=False)  # Fecha de pago
        # metodo_pago_clave = Column(Integer, ForeignKey('metodos_pago.clave'), nullable=False)  # Clave del método de pago
        # forma_pago_clave = Column(Integer, ForeignKey('formas_pago.clave'), nullable=False)  # Clave de la forma de pago
        banco_clave = Column(String(2), ForeignKey('banco.clave'))  # Clave del banco
        percepciones_recibo = Column(String(3), ForeignKey('percepciones.clave'), nullable=False)  # Percepciones
        valor_percepciones = Column(Float, nullable=False)  # Valor de percepciones
        total_percepciones = Column(Float, nullable=False)  # Total de percepciones
        deducciones_recibo = Column(String(3), ForeignKey('deducciones.clave'), nullable=False)  # Deducciones
        valor_deducciones = Column(Float, nullable=False)  # Valor de deducciones
        total_deducciones = Column(Float, nullable=False)  # Total de deducciones
        importe = Column(Float, nullable=False)  # Importe total (Percepciones - Deducciones)
        importe_con_letra = Column(String(255), nullable=False)  # Importe con letra
        moneda = Column(String(20), default='MXN PESOS MEXICANOS', nullable=False)  # Moneda
        tipo_cambio = Column(Float, default=0.00, nullable=False)  # Tipo de cambio
        sello_digital_cfdi = Column(Text, nullable=False)  # Sello digital CFDI
        sello_digital_sat = Column(Text, nullable=False)  # Sello digital SAT
        cadena_original_complemento_certificacion = Column(Text, nullable=False)  # Cadena original complemento certificación
        codigo_qr = Column(String, nullable=False)  # Código QR
    
        # Relaciones con otras tablas
        empleado = relationship("Empleado", back_populates="recibos_nomina")
        # uso_destino_cfdi = relationship("UsoDestinoCfdi", back_populates="recibos_nomina")
        # tipo_comprobante = relationship("TipoComprobante", back_populates="recibos_nomina")
        regimen_laboral = relationship("RegimenLaboral", back_populates="recibos_nomina")
        # metodo_pago = relationship("MetodoPago", back_populates="recibos_nomina")
        # forma_pago = relationship("FormaPago", back_populates="recibos_nomina")
        banco = relationship("Banco", back_populates="recibos_nomina")
        percepciones = relationship("Percepciones", back_populates="recibos_nomina")
        deducciones = relationship("Deducciones", back_populates="recibos_nomina")
        recibos_pdf = relationship("ReciboPDF", back_populates="recibo")
# models/factura.py

"""
Este archivo define las clases que representan entidades relacionadas con las facturas en la aplicación.
Cada clase define una tabla en la base de datos utilizando SQLAlchemy para el mapeo objeto-relacional (ORM).
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Declaramos una base para las clases de SQLAlchemy
Base = declarative_base()

class Usuario(Base):
    """
    Clase para representar a los usuarios en la aplicación.
    Cada usuario puede tener asociadas múltiples facturas.
    """
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)  # Identificador único del usuario
    nombre_usuario = Column(String(255), nullable=False)  # Nombre del usuario
    contraseña_hash = Column(String(255), nullable=False)  # Hash de la contraseña del usuario
    correo_electronico = Column(String(255), unique=True, nullable=False)  # Correo electrónico del usuario
    rfc_receptor = Column(String(13), unique=True, nullable=False)  # RFC (Registro Federal de Contribuyentes) del receptor asociado al usuario
    domicilio = Column(String(255), nullable=False)  # Domicilio del usuario

    facturas = relationship("Factura", back_populates="usuario")  # Relación con la tabla Factura: un usuario puede tener múltiples facturas

class ProductoServicio(Base):
    """
    Clase para representar productos o servicios que pueden ser incluidos en una factura.
    """
    __tablename__ = 'productos_servicios'

    clave_producto_servicio = Column(String(10), primary_key=True, unique=True, nullable=False)  # Clave única del producto o servicio
    unidad = Column(String(255), nullable=False)  # Unidad del producto o servicio
    descripcion = Column(String(255), nullable=False)  # Descripción del producto o servicio
    precio_unitario = Column(Float, nullable=False)  # Precio unitario del producto o servicio

    facturas = relationship("Factura", back_populates="producto_servicio")  # Relación con la tabla Factura: un producto o servicio puede estar asociado a múltiples facturas

class TipoComprobante(Base):
    """
    Clase para representar los tipos de comprobantes que pueden tener las facturas.
    """
    __tablename__ = 'tipo_comprobante'

    clave = Column(String(1), primary_key=True, unique=True, nullable=False)  # Clave única del tipo de comprobante
    descripcion = Column(String(255), nullable=False)  # Descripción del tipo de comprobante
    
    facturas = relationship("Factura", back_populates="tipo_comprobante")  # Relación con la tabla Factura: un tipo de comprobante puede estar asociado a múltiples facturas

class UsoDestinoCfdi(Base):
    """
    Clase para representar el uso o destino de un CFDI (Comprobante Fiscal Digital por Internet).
    """
    __tablename__ = 'uso_destino_cfdi'

    clave = Column(String(4), primary_key=True, unique=True, nullable=False)  # Clave única del uso o destino de un CFDI
    descripcion = Column(String(255), nullable=False)  # Descripción del uso o destino de un CFDI
    
    facturas = relationship("Factura", back_populates="uso_destino_cfdi")  # Relación con la tabla Factura: un uso o destino de CFDI puede estar asociado a múltiples facturas

class RegimenFiscal(Base):
    """
    Clase para representar el régimen fiscal del emisor de una factura.
    """
    __tablename__ = 'regimen_fiscal'

    clave = Column(String(3), primary_key=True, unique=True, nullable=False)  # Clave única del régimen fiscal
    descripcion = Column(String(255), nullable=False)  # Descripción del régimen fiscal
    
    facturas = relationship("Factura", back_populates="regimen_fiscal")  # Relación con la tabla Factura: un régimen fiscal puede estar asociado a múltiples facturas

class MetodoPago(Base):
    """
    Clase para representar los métodos de pago que pueden ser utilizados en una factura.
    """
    __tablename__ = 'metodos_pago'

    clave = Column(String(3), primary_key=True, unique=True, nullable=False)  # Clave única del método de pago
    descripcion = Column(String(255), nullable=False)  # Descripción del método de pago
    
    facturas = relationship("Factura", back_populates="metodo_pago")  # Relación con la tabla Factura: un método de pago puede estar asociado a múltiples facturas

class FormaPago(Base):
    """
    Clase para representar las formas de pago que pueden ser utilizadas en una factura.
    """
    __tablename__ = 'formas_pago'

    clave = Column(String(2), primary_key=True, unique=True, nullable=False)  # Clave única de la forma de pago
    descripcion = Column(String(255), nullable=False)  # Descripción de la forma de pago
    
    facturas = relationship("Factura", back_populates="forma_pago")  # Relación con la tabla Factura: una forma de pago puede estar asociada a múltiples facturas

class FacturaPDF(Base):
    """
    Clase para representar las facturas en formato PDF.
    """
    __tablename__ = "facturas_pdf"

    id = Column(Integer, primary_key=True, index=True)  # Identificador único del PDF de la factura
    id_factura = Column(Integer, ForeignKey("facturas.id"))  # Identificador de la factura asociada al PDF
    pdf = Column(LargeBinary)  # Contenido binario del PDF
    
    facturas = relationship("Factura", back_populates="facturas_pdf")  # Relación con la tabla Factura: un PDF de factura está asociado a una factura

class Factura(Base):
    """
    Clase para representar las facturas en la aplicación.
    """
    __tablename__ = 'facturas'

    id = Column(Integer, primary_key=True)  # Identificador único de la factura
    nombre_empresa = Column(String(50), default='FARMACIAS DE DIOS', nullable=False)  # Nombre de la empresa emisora de la factura
    uso_destino_cfdi_clave = Column(Integer, ForeignKey('uso_destino_cfdi.clave'), nullable=False)  # Clave del uso o destino del CFDI
    lugar_expedicion = Column(String(20), default='CIUDAD DE MÉXICO', nullable=False)  # Lugar de expedición de la factura
    fecha_expedicion = Column(DateTime, nullable=False)  # Fecha de expedición de la factura
    rfc_emisor = Column(String(20), default='FARA2402035H8', nullable=False)  # RFC del emisor de la factura
    tipo_comprobante_clave = Column(Integer, ForeignKey('tipo_comprobante.clave'), nullable=False)  # Clave del tipo de comprobante
    regimen_fiscal_clave = Column(Integer, ForeignKey('regimen_fiscal.clave'), nullable=False)  # Clave del régimen fiscal del emisor
    rfc_receptor = Column(String(20), ForeignKey('usuarios.rfc_receptor'), nullable=False)  # RFC del receptor asociado a la factura
    clave_producto_servicio = Column(String(10), ForeignKey('productos_servicios.clave_producto_servicio'), nullable=False)  # Clave del producto o servicio incluido en la factura
    cantidad = Column(Integer, nullable=False)  # Cantidad de productos o servicios incluidos en la factura
    importe = Column(Float, nullable=False)  # Importe total de la factura
    subtotal = Column(Float, nullable=False)  # Subtotal de la factura
    iva = Column(Float, nullable=False)  # IVA (Impuesto al Valor Agregado) de la factura
    total = Column(Float, nullable=False)  # Total de la factura
    total_con_letra = Column(String(255), nullable=False)  # Total en letra de la factura
    moneda = Column(String(20), default='MXN PESOS MEXICANOS', nullable=False)  # Moneda en la que está expresada la factura
    tipo_cambio = Column(Float, default=0.00, nullable=False)  # Tipo de cambio en caso de que la moneda sea distinta de pesos mexicanos
    metodo_pago_clave = Column(Integer, ForeignKey('metodos_pago.clave'), nullable=False)  # Clave del método de pago
    forma_pago_clave = Column(Integer, ForeignKey('formas_pago.clave'), nullable=False)  # Clave de la forma de pago
    sello_digital_cfdi = Column(Text, nullable=False)  # Sello digital del CFDI (Comprobante Fiscal Digital por Internet)
    sello_digital_sat = Column(Text, nullable=False)  # Sello digital del SAT (Servicio de Administración Tributaria)
    cadena_original_complemento_certificacion = Column(Text, nullable=False)  # Cadena original del complemento de certificación
    codigo_qr = Column(String, nullable=False)  # Código QR de la factura

    # Relaciones con otras tablas
    usuario = relationship("Usuario", back_populates="facturas")
    producto_servicio = relationship("ProductoServicio", back_populates="facturas")
    tipo_comprobante = relationship("TipoComprobante", back_populates="facturas")
    uso_destino_cfdi = relationship("UsoDestinoCfdi", back_populates="facturas")
    regimen_fiscal = relationship("RegimenFiscal", back_populates="facturas")
    metodo_pago = relationship("MetodoPago", back_populates="facturas")
    forma_pago = relationship("FormaPago", back_populates="facturas")
    facturas_pdf = relationship("FacturaPDF", back_populates="facturas")
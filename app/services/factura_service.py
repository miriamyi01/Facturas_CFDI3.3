# services/factura_service.py

"""
Este archivo define funciones relacionadas con la gestión de facturas y la interacción con la base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from contextlib import contextmanager
import random, string, qrcode, io
from num2words import num2words
from models import Factura, TipoComprobante, UsoDestinoCfdi, RegimenFiscal, MetodoPago, FormaPago, ProductoServicio
from datetime import datetime

# Crear un motor de base de datos
# Aquí se establece la conexión con la base de datos PostgreSQL
engine = create_engine('postgresql://postgres:root12345@localhost/cfdi_facturas')

# Crear una fábrica de sesiones
# Esto se utiliza para crear nuevas sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Este es un administrador de contexto que se utiliza para manejar las sesiones de base de datos
@contextmanager
def get_db():
    """
    Administrador de contexto para manejar las sesiones de base de datos.

    Returns:
        Session: Una nueva sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generar_cadena_aleatoria(longitud):
    """
    Genera una cadena aleatoria de caracteres.

    Args:
        longitud (int): La longitud de la cadena a generar.

    Returns:
        str: La cadena aleatoria generada.
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def generar_codigo_qr():
    """
    Genera un código QR aleatorio.

    Returns:
        bytes: Los bytes de la imagen del código QR.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    contenido_qr = generar_cadena_aleatoria(500)
    
    qr.add_data(contenido_qr)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return bytearray(img_io.getvalue())

def obtener_tipo_comprobante(db):
    """
    Obtiene los tipos de comprobante disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con los tipos de comprobante disponibles.
    """
    tipos_comprobante = db.query(TipoComprobante).all()
    return [f"{tipos_comprobante.clave} - {tipos_comprobante.descripcion}" for tipos_comprobante in tipos_comprobante]

def obtener_uso_destino_cfdi(db):
    """
    Obtiene los usos o destinos de un CFDI disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con los usos o destinos de un CFDI disponibles.
    """
    usos_destino_cfdi = db.query(UsoDestinoCfdi).all()
    return [f"{uso_destino_cfdi.clave} - {uso_destino_cfdi.descripcion}" for uso_destino_cfdi in usos_destino_cfdi]

def obtener_regimen_fiscal(db):
    """
    Obtiene los regímenes fiscales disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con los regímenes fiscales disponibles.
    """
    regimenes_fiscales = db.query(RegimenFiscal).all()
    return [f"{regimen_fiscal.clave} - {regimen_fiscal.descripcion}" for regimen_fiscal in regimenes_fiscales]

def obtener_metodos_pago(db):
    """
    Obtiene los métodos de pago disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con los métodos de pago disponibles.
    """
    metodos_pago = db.query(MetodoPago).all()
    return [f"{metodo_pago.clave} - {metodo_pago.descripcion}" for metodo_pago in metodos_pago]

def obtener_formas_pago(db):
    """
    Obtiene las formas de pago disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con las formas de pago disponibles.
    """
    formas_pago = db.query(FormaPago).all()
    return [f"{forma_pago.clave} - {forma_pago.descripcion}" for forma_pago in formas_pago]

def obtener_productos_servicios(db):
    """
    Obtiene los productos o servicios disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con los productos o servicios disponibles.
    """
    productos_servicios = db.query(ProductoServicio).all()
    return [f"{producto_servicio.clave_producto_servicio} - {producto_servicio.descripcion}" for producto_servicio in productos_servicios]

def obtener_precio_unitario(db: Session, clave_producto_servicio: str):
    """
    Obtiene el precio unitario de un producto o servicio.

    Args:
        db (Session): La sesión de la base de datos.
        clave_producto_servicio (str): La clave del producto o servicio.

    Returns:
        float: El precio unitario del producto o servicio.
    """
    clave, _ = clave_producto_servicio.split(" - ")
    producto_servicio = db.query(ProductoServicio).filter(ProductoServicio.clave_producto_servicio == clave).first()
    return producto_servicio.precio_unitario

def calcular_valores_factura(db: Session, datos_factura):
    """
    Calcula los valores de una factura.

    Args:
        db (Session): La sesión de la base de datos.
        datos_factura (dict): Un diccionario con los datos de la factura.

    Returns:
        dict: Un diccionario con los valores calculados de la factura.
    """
    precio_unitario = obtener_precio_unitario(db, datos_factura['clave_producto_servicio'])
    importe = datos_factura['cantidad'] * precio_unitario
    subtotal = importe
    iva = subtotal * 0.16
    total = subtotal + iva

    return {
        'precio_unitario': precio_unitario,
        'importe': importe,
        'subtotal': subtotal,
        'iva': iva,
        'total': total
    }

def crear_factura(db, datos_factura):
    """
    Crea una nueva factura en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        datos_factura (dict): Un diccionario con los datos de la factura.

    Returns:
        Factura: El objeto de factura creado.
    """
    clave_tipo_comprobante, _ = datos_factura['tipo_comprobante_clave'].split(" - ")
    clave_uso_destino_cfdi, _ = datos_factura['uso_destino_cfdi_clave'].split(" - ")
    clave_regimen_fiscal, _ = datos_factura['regimen_fiscal_clave'].split(" - ")
    clave_metodo_pago, _ = datos_factura['metodo_pago_clave'].split(" - ")
    clave_forma_pago, _ = datos_factura['forma_pago_clave'].split(" - ")
    clave_producto_servicio, _ = datos_factura['clave_producto_servicio'].split(" - ")

    factura = Factura(
        uso_destino_cfdi_clave=clave_uso_destino_cfdi,
        fecha_expedicion=datetime.now(),
        tipo_comprobante_clave=clave_tipo_comprobante,
        regimen_fiscal_clave=clave_regimen_fiscal,
        rfc_receptor=datos_factura['rfc_receptor'],
        clave_producto_servicio=clave_producto_servicio,
        cantidad=datos_factura['cantidad'],
        importe=datos_factura['importe'],
        subtotal=datos_factura['subtotal'],
        iva=datos_factura['iva'],
        total=datos_factura['total'],
        total_con_letra=num2words(datos_factura['total'], lang='es').upper() + ", 00/100 M.N.",
        metodo_pago_clave=clave_metodo_pago,
        forma_pago_clave=clave_forma_pago,
        sello_digital_cfdi=generar_cadena_aleatoria(100),
        sello_digital_sat=generar_cadena_aleatoria(100),
        cadena_original_complemento_certificacion=generar_cadena_aleatoria(100),
        codigo_qr=generar_codigo_qr()
    )

    db.add(factura)
    db.commit()

    return factura
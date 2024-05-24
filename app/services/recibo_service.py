# services/recibo_service.py

"""
Este archivo define funciones relacionadas con la gestión de recibos de nómina y la interacción con la base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from contextlib import contextmanager
import random, string, qrcode, io
from num2words import num2words
from models import Recibo, Empleado, UsoDestinoCfdi, TipoComprobante, RegimenLaboral, MetodoPago, FormaPago, Banco, Percepcion, Deduccion
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

def obtener_empleado(db):
    """
    Obtiene los tipos de comprobante disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con los tipos de comprobante disponibles.
    """
    empleados = db.query(Empleado).all()


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

def obtener_regimen_laboral(db):
    """
    Obtiene los regímenes laborales disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con los regímenes laborales disponibles.
    """
    regimenes_laborales = db.query(RegimenLaboral).all()
    return [f"{regimen_laboral.clave} - {regimen_laboral.descripcion}" for regimen_laboral in regimenes_laborales]

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

def obtener_banco(db):
    """
    Obtiene los bancos disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con los bancos disponibles.
    """
    bancos = db.query(Banco).all()
    return [f"{banco.clave_producto_servicio} - {banco.descripcion}" for banco in bancos]


def obtener_persepciones(db):
    """
    Obtiene las persepciones disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con las persepciones disponibles.
    """
    percepciones = db.query(Percepcion).all()
    return [f"{percepcion.clave_percepcion} - {percepcion.descripcion}" for percepcion in percepciones]


def obtener_deducciones(db):
    """
    Obtiene las deducciones disponibles en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.

    Returns:
        list: Una lista de cadenas con las deducciones disponibles.
    """
    deducciones = db.query(Deduccion).all()
    return [f"{deduccion.clave_deduccion} - {deduccion.descripcion}" for deduccion in deducciones]

def calcular_valores_recibo(db: Session, datos_recibo):
    """
    Calcula los valores del recibo de nómina.

    Args:
        db (Session): La sesión de la base de datos.
        datos_factura (dict): Un diccionario con los datos del recibo.

    Returns:
        dict: Un diccionario con los valores calculados de la factura.
    """
    valor_percepciones = datos_recibo['valor_percepciones']
    total_percepciones = sum(percepcion['valor'] for percepcion in datos_recibo['percepciones_recibo'])
    valor_deducciones = datos_recibo['valor_deduccion']
    total_deducciones = sum(deduccion['valor'] for deduccion in datos_recibo['deducciones_recibo'])
    importe = sum(total_percepciones, total_deducciones)

    return {
        'valor_percepciones': valor_percepciones,
        'total_percepciones': total_percepciones,
        'valor_deducciones': valor_deducciones,
        'total_deducciones': total_deducciones,
        'importe': importe
    }

def crear_recibo(db, datos_recibo):
    """
    Crea un nuevo recibo en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        datos_recibo (dict): Un diccionario con los datos del recibo.

    Returns:
        Recibo: El objeto de recibo creado.
    """
    empleado = obtener_empleado(db, datos_recibo['numero_empleado'])
    clave_tipo_comprobante, _ = datos_recibo['tipo_comprobante_clave'].split(" - ")
    clave_uso_destino_cfdi, _ = datos_recibo['uso_destino_cfdi_clave'].split(" - ")
    clave_regimen_laboral, _ = datos_recibo['regimen_laboral_clave'].split(" - ")
    clave_metodo_pago, _ = datos_recibo['metodo_pago_clave'].split(" - ")
    clave_forma_pago, _ = datos_recibo['forma_pago_clave'].split(" - ")
    clave_banco, _ = datos_recibo['banco_clave'].split(" - ")
    clave_percepcion, _ = datos_recibo['percepcion_clave'].split(" - ")
    clave_deduccion, _ = datos_recibo['deduccion_clave'].split(" - ")



    recibo = Recibo(
        uso_destino_cfdi_clave=clave_uso_destino_cfdi,
        fecha_expedicion = datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        fecha_pago = datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        tipo_comprobante_clave=clave_tipo_comprobante,
        regimen_laboral_clave=clave_regimen_laboral,
        numero_empleado=empleado.numero_empleado,
        curp=empleado.curp,
        nss=empleado.nss,
        fecha_ingreso=empleado.fecha_ingreso,
        sueldo_base=empleado.sueldo_base,
        puesto_id=empleado.puesto_id,
        departamento_id=empleado.departamento_id,
        riesgo_id=empleado.riesgo_id,
        tipo_jornada=empleado.tipo_jornada,
        tipo_contrato=empleado.tipo_contrato,
        periodicidad_pago=empleado.periodicidad_pago,
        metodo_pago_clave=clave_metodo_pago,
        forma_pago_clave=clave_forma_pago,
        banco_clave=clave_banco,
        clave_percepcion=clave_percepcion,
        valor_percepciones=datos_recibo['valor_percepciones'],
        total_percepciones=datos_recibo['total_percepciones'],
        clave_deduccion=clave_deduccion,
        valor_deducciones=datos_recibo['valor_deducciones'],
        total_deducciones=datos_recibo['total_deducciones'],
        importe=datos_recibo['importe'],
        importe_con_letra=num2words(datos_recibo['importe'], lang='es').upper() + ", 00/100 M.N.",
        sello_digital_cfdi=generar_cadena_aleatoria(100),
        sello_digital_sat=generar_cadena_aleatoria(100),
        cadena_original_complemento_certificacion=generar_cadena_aleatoria(100),
        codigo_qr=generar_codigo_qr()
    )

    db.add(recibo)
    db.commit()

    return recibo
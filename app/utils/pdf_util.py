# utils/pdf_utils.py

"""
Este archivo proporciona funciones para generar y guardar archivos PDF de facturas.
"""

from fpdf import FPDF
from models import Factura, FacturaPDF
from sqlalchemy.orm import joinedload
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from PIL import Image
import io
from io import BytesIO

# Crear un motor de base de datos
# Aquí se establece la conexión con la base de datos PostgreSQL
engine = create_engine('postgresql://postgres:minora0811@localhost/cfdi_facturas')

# Crear una fábrica de sesiones
# Esto se utiliza para crear nuevas sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Este es un administrador de contexto que se utiliza para manejar las sesiones de base de datos
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def obtener_datos(session, id_factura):
    """
    Obtiene los datos de una factura de la base de datos.

    Args:
        session (Session): La sesión de la base de datos.
        id_factura (int): El ID de la factura.

    Returns:
        dict: Un diccionario con los datos de la factura.
    """
    # Obtener la factura con el ID dado
    factura = session.query(Factura).options(joinedload('*')).filter(Factura.id == id_factura).first()

    # Si la factura existe, devolver sus datos
    if factura:
        def convert_qr_code(qr_bytes):
            if qr_bytes is not None:
                return Image.open(BytesIO(qr_bytes))

        return {
            "nombre_empresa": factura.nombre_empresa,
            "uso_destino_cfdi_clave": factura.uso_destino_cfdi.clave,
            "uso_destino_cfdi_descripcion": factura.uso_destino_cfdi.descripcion,
            "lugar_expedicion": factura.lugar_expedicion,
            "fecha_expedicion": factura.fecha_expedicion,
            "rfc_emisor": factura.rfc_emisor,
            "tipo_comprobante_clave": factura.tipo_comprobante.clave,
            "tipo_comprobante_descripcion": factura.tipo_comprobante.descripcion,
            "regimen_fiscal_clave": factura.regimen_fiscal.clave,
            "regimen_fiscal_descripcion": factura.regimen_fiscal.descripcion,
            "rfc_receptor": factura.rfc_receptor,
            "clave_producto_servicio": factura.producto_servicio.clave_producto_servicio,
            "descripcion_producto_servicio": factura.producto_servicio.descripcion,
            "cantidad": factura.cantidad,
            "importe": factura.importe,
            "subtotal": factura.subtotal,
            "iva": factura.iva,
            "total": factura.total,
            "total_con_letra": factura.total_con_letra,
            "moneda": factura.moneda,
            "tipo_cambio": factura.tipo_cambio,
            "metodo_pago_clave": factura.metodo_pago.clave,
            "metodo_pago_descripcion": factura.metodo_pago.descripcion,
            "forma_pago_clave": factura.forma_pago.clave,
            "forma_pago_descripcion": factura.forma_pago.descripcion,
            "sello_digital_cfdi": factura.sello_digital_cfdi,
            "sello_digital_sat": factura.sello_digital_sat,
            "cadena_original_complemento_certificacion": factura.cadena_original_complemento_certificacion,
            "codigo_qr": convert_qr_code(factura.codigo_qr),
        }

def generar_pdf(datos):
    """
    Genera un archivo PDF con los datos de la factura.

    Args:
        datos (dict): Un diccionario con los datos de la factura.

    Returns:
        bytes: Los bytes del archivo PDF generado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in datos.items():
        if key == 'codigo_qr':
            # Convertir la imagen PIL a bytes
            img_byte_arr = io.BytesIO()
            value.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Guardar los bytes de la imagen en un archivo temporal
            with open('temp.png', 'wb') as f:
                f.write(img_byte_arr)

            # Agregar la imagen al PDF
            pdf.image('temp.png')
        else:
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    return pdf.output(dest='S').encode('latin1')

def guardar_factura_pdf(session, id_factura, pdf_bytes):
    """
    Guarda un archivo PDF de factura en la base de datos.

    Args:
        session (Session): La sesión de la base de datos.
        id_factura (int): El ID de la factura.
        pdf_bytes (bytes): Los bytes del archivo PDF.

    Returns:
        None
    """
    # Crear un nuevo objeto FacturaPDF
    factura_pdf = FacturaPDF(id_factura=id_factura, pdf=pdf_bytes)

    # Agregar el objeto FacturaPDF a la sesión
    session.add(factura_pdf)

    # Guardar los cambios en la base de datos
    session.commit()
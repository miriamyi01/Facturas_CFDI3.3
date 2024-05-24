# utils/factura_pdf_utils.py

"""
Este archivo proporciona funciones para generar y guardar archivos PDF de facturas.
"""

from fpdf import FPDF
from models import Recibo, ReciboPDF
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

def obtener_datos(session, id_recibo):
    """
    Obtiene los datos de un recibo de nómina de la base de datos.

    Args:
        session (Session): La sesión de la base de datos.
        id_recibo (int): El ID del recibo de nómina.

    Returns:
        dict: Un diccionario con los datos del recibo de nómina.
    """
    # Obtener el recibo de nómina con el ID dado
    recibo = session.query(Recibo).options(joinedload('*')).filter(Recibo.id == id_recibo).first()

    # Si el recibo de nómina existe, devolver sus datos
    if recibo:
        def convert_qr_code(qr_bytes):
            if qr_bytes is not None:
                return Image.open(BytesIO(qr_bytes))

        return {
            "id": recibo.id,
            "nombre_empresa": recibo.nombre_empresa,
            "uso_destino_cfdi_clave": recibo.uso_destino_cfdi.clave,
            "lugar_expedicion": recibo.lugar_expedicion,
            "fecha_expedicion": recibo.fecha_expedicion,
            "rfc_emisor": recibo.rfc_emisor,
            "tipo_comprobante_clave": recibo.tipo_comprobante.clave,
            "regimen_laboral_clave": recibo.regimen_laboral.clave,
            "empleado": {
                "numero_empleado": recibo.empleado.numero_empleado,
                "curp": recibo.empleado.curp,
                "nss": recibo.empleado.nss,
                "fecha_ingreso": recibo.empleado.fecha_ingreso,
                "sueldo_base": recibo.empleado.sueldo_base,
                "puesto_id": recibo.empleado.puesto_id,
                "departamento_id": recibo.empleado.departamento_id,
                "riesgo_id": recibo.empleado.riesgo_id,
                "tipo_jornada": recibo.empleado.tipo_jornada,
                "tipo_contrato": recibo.empleado.tipo_contrato,
                "periodicidad_pago": recibo.empleado.periodicidad_pago
            },
            "fecha_pago": recibo.fecha_pago,
            "metodo_pago_clave": recibo.metodo_pago.clave,
            "forma_pago_clave": recibo.forma_pago.clave,
            "banco_clave": recibo.banco_clave,
            "percepciones_recibo": recibo.percepciones_recibo,
            "valor_percepciones": recibo.valor_percepciones,
            "total_percepciones": recibo.total_percepciones,
            "deducciones_recibo": recibo.deducciones_recibo,
            "valor_deducciones": recibo.valor_deducciones,
            "total_deducciones": recibo.total_deducciones,
            "importe": recibo.importe,
            "importe_con_letra": recibo.importe_con_letra,
            "moneda": recibo.moneda,
            "tipo_cambio": recibo.tipo_cambio,
            "sello_digital_cfdi": recibo.sello_digital_cfdi,
            "sello_digital_sat": recibo.sello_digital_sat,
            "cadena_original_complemento_certificacion": recibo.cadena_original_complemento_certificacion,
            "codigo_qr": convert_qr_code(recibo.codigo_qr),
        }

def generar_pdf(datos):
    """
    Genera un archivo PDF con los datos de el recibo de nómina.

    Args:
        datos (dict): Un diccionario con los datos de el recibo de nómina.

    Returns:
        bytes: Los bytes del archivo PDF generado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Diccionario de mapeo para los textos específicos
    mapeo_texto = {
        "nombre_empresa": "Empresa",
        "uso_destino_cfdi_clave": "Clave Uso CFDI",
        "uso_destino_cfdi_descripcion": "Descripción Uso CFDI",
    }

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
            pdf.image('temp.png', w=20, h=20)
        else:
            # Encabezado - Nombre y logotipo

            # Cuerpo - Datos

            # Final - Sellos
            texto_completo = f"{mapeo_texto[key]}: {value}"
            pdf.cell(200, 10, txt=texto_completo, ln=True)

    return pdf.output(dest='S').encode('latin1')

def guardar_recibo_pdf(session, id_recibo, pdf_bytes):
    """
    Guarda un archivo PDF de recibo de nómina en la base de datos.

    Args:
        session (Session): La sesión de la base de datos.
        id_recibo (int): El ID de recibo de nómina.
        pdf_bytes (bytes): Los bytes del archivo PDF.

    Returns:
        None
    """
    # Crear un nuevo objeto ReciboPDF
    recibo_pdf = ReciboPDF(id_recibo=id_recibo, pdf=pdf_bytes)

    # Agregar el objeto ReciboPDF a la sesión
    session.add(recibo_pdf)

    # Guardar los cambios en la base de datos
    session.commit()
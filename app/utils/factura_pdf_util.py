# utils/factura_pdf_utils.py

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

class PDF(FPDF):
    def header(self):
        # Margen superior en azul
        self.set_fill_color(0, 0, 255)
        self.rect(0, 0, 210, 15, 'F')

    def footer(self):
        # Margen inferior en azul
        self.set_y(-15)
        self.set_fill_color(0, 0, 255)
        self.rect(0, 285, 210, 15, 'F')

    def chapter_title(self, title):
        # Título de capítulo
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        # Cuerpo del capítulo
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 10, body)
        self.ln()

def generar_pdf(datos):
    """
    Genera un archivo PDF con los datos de la factura.

    Args:
        datos (dict): Un diccionario con los datos de la factura.

    Returns:
        bytes: Los bytes del archivo PDF generado.
    """
    pdf = PDF()
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Encabezado - Datos del Emisor
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, datos['nombre_empresa'], 0, 1, 'C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"RFC: {datos['rfc_emisor']}", 0, 1, 'C')
    pdf.cell(0, 10, f"Régimen Fiscal: {datos['regimen_fiscal_clave']} - {datos['regimen_fiscal_descripcion']}", 0, 1, 'C')
    pdf.ln(10)

    # Primera columna
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(95, 10, 'Datos del Receptor', 0, 0, 'L')
    pdf.cell(95, 10, 'Detalles de la Factura', 0, 1, 'L')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 10, f"RFC: {datos['rfc_receptor']}", 0, 0, 'L')
    pdf.cell(95, 10, f"Tipo de Comprobante: {datos['tipo_comprobante_clave']} - {datos['tipo_comprobante_descripcion']}", 0, 1, 'L')
    
    pdf.cell(95, 10, '', 0, 0, 'L')
    pdf.cell(95, 10, f"Uso de CFDI: {datos['uso_destino_cfdi_clave']} - {datos['uso_destino_cfdi_descripcion']}", 0, 1, 'L')

    pdf.cell(95, 10, '', 0, 0, 'L')
    pdf.cell(95, 10, f"Fecha de Expedición: {datos['fecha_expedicion']}", 0, 1, 'L')
    
    pdf.cell(95, 10, '', 0, 0, 'L')
    pdf.cell(95, 10, f"Lugar de Expedición: {datos['lugar_expedicion']}", 0, 1, 'L')

    pdf.cell(95, 10, '', 0, 0, 'L')
    pdf.cell(95, 10, f"Forma de Pago: {datos['forma_pago_clave']} - {datos['forma_pago_descripcion']}", 0, 1, 'L')

    pdf.cell(95, 10, '', 0, 0, 'L')
    pdf.cell(95, 10, f"Método de Pago: {datos['metodo_pago_clave']} - {datos['metodo_pago_descripcion']}", 0, 1, 'L')

    pdf.cell(95, 10, '', 0, 0, 'L')
    pdf.cell(95, 10, f"Moneda: {datos['moneda']} - Tipo de Cambio: {datos['tipo_cambio']}", 0, 1, 'L')
    pdf.ln(10)

    # Segunda columna
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, 'Conceptos', 0, 1, 'L')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Clave Producto/Servicio: {datos['clave_producto_servicio']}", 0, 1, 'L')
    pdf.cell(0, 10, f"Descripción: {datos['descripcion_producto_servicio']}", 0, 1, 'L')
    pdf.cell(0, 10, f"Cantidad: {datos['cantidad']}", 0, 1, 'L')
    pdf.cell(0, 10, f"Importe: {datos['importe']}", 0, 1, 'L')
    pdf.ln(10)

    # Totales
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, 'Totales', 0, 1, 'L')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Subtotal: {datos['subtotal']}", 0, 1, 'L')
    pdf.cell(0, 10, f"IVA: {datos['iva']}", 0, 1, 'L')
    pdf.cell(0, 10, f"Total: {datos['total']}", 0, 1, 'L')
    pdf.cell(0, 10, f"Total con letra: {datos['total_con_letra']}", 0, 1, 'L')
    pdf.ln(10)

    # Sellos digitales
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, 'Sellos Digitales', 0, 1, 'L')
    
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, f"Sello Digital del CFDI:\n{datos['sello_digital_cfdi']}", 0, 1, 'L')
    pdf.multi_cell(0, 10, f"Sello Digital del SAT:\n{datos['sello_digital_sat']}", 0, 1, 'L')
    pdf.multi_cell(0, 10, f"Cadena Original del Complemento de Certificación:\n{datos['cadena_original_complemento_certificacion']}", 0, 1, 'L')

    # Segunda hoja para el código QR
    '''
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, 'Código QR', 0, 1, 'C')
    if datos['codigo_qr']:
        img_byte_arr = io.BytesIO()
        datos['codigo_qr'].save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        with open('/mnt/data/temp.png', 'wb') as f:
            f.write(img_byte_arr)
        pdf.image('/mnt/data/temp.png', x=60, y=60, w=90, h=90)
    '''
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
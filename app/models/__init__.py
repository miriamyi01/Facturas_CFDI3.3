# models/__init__.py

"""
Este archivo __init__.py sirve para convertir este directorio en un paquete de Python.
Los paquetes de Python son una forma de organizar módulos relacionados en un directorio.

Este archivo en particular está importando varias clases desde otros módulos en el mismo paquete.
Estas clases se utilizan para representar diferentes entidades en nuestra aplicación.
"""

# Importamos la clase Usuario del módulo usuario
# Esta clase se utiliza para representar a un usuario en nuestra aplicación.
from .usuario import Usuario

# Importamos varias clases del módulo factura
# Estas clases se utilizan para representar diferentes aspectos de una factura en nuestra aplicación.
from .factura import (
    Factura,  # Clase para representar una factura
    TipoComprobante,  # Clase para representar el tipo de comprobante de una factura
    UsoDestinoCfdi,  # Clase para representar el uso o destino de un CFDI (Comprobante Fiscal Digital por Internet)
    RegimenFiscal,  # Clase para representar el régimen fiscal del emisor de una factura
    MetodoPago,  # Clase para representar el método de pago de una factura
    FormaPago,  # Clase para representar la forma de pago de una factura
    ProductoServicio,  # Clase para representar un producto o servicio en una factura
    FacturaPDF  # Clase para representar facturas en formato PDF
)

# Importamos la clase Empleado del módulo empleado
# Esta clase se utiliza para representar a un empleado en nuestra aplicación.
from .empleado import Empleado (
    
)

# Importamos varias clases del módulo recibo
# Estas clases se utilizan para representar diferentes aspectos de un recibo en nuestra aplicación.
from .recibo import (
    Recibo,  # Clase para representar un recibo
    Empleado,  # Clase para representar un empleado en un recibo
    UsoDestinoCfdi,  # Clase para representar el uso o destino de un CFDI en un recibo
    TipoComprobante,  # Clase para representar el tipo de comprobante de un recibo
    RegimenLaboral,  # Clase para representar el régimen laboral en un recibo
    MetodoPago,  # Clase para representar el método de pago de un recibo
    FormaPago,  # Clase para representar la forma de pago de un recibo
    Banco,  # Clase para representar el banco en un recibo
    Percepcion,  # Clase para representar una percepción en un recibo
    Deduccion,  # Clase para representar una deducción en un recibo
    ReciboPDF  # Clase para representar recibos en formato PDF
)
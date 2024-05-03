# services/auth_service.py

"""
Este archivo define funciones relacionadas con la autenticación de usuarios y la interacción con la base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager
from models import Usuario

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

# Esta función se utiliza para registrar un nuevo usuario en la base de datos
def registrar_usuario(db: Session, nombre_usuario: str, contraseña: str, correo_electronico: str, rfc_receptor: str, domicilio: str, es_empleado: bool = False):
    """
    Registra un nuevo usuario en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        nombre_usuario (str): El nombre de usuario del nuevo usuario.
        contraseña (str): La contraseña del nuevo usuario.
        correo_electronico (str): El correo electrónico del nuevo usuario.
        rfc_receptor (str): El RFC del nuevo usuario.
        domicilio (str): El domicilio del nuevo usuario.
        es_empleado (bool): Indica si el usuario es un empleado.

    Returns:
        Usuario: El objeto de usuario recién registrado o un mensaje de error si el correo electrónico o el RFC ya están en uso.
    """
    # Primero, verificamos si el correo electrónico o el RFC ya están en uso
    usuario_existente = db.query(Usuario).filter((Usuario.correo_electronico == correo_electronico) | (Usuario.rfc_receptor == rfc_receptor)).first()
    if usuario_existente:
        if usuario_existente.correo_electronico == correo_electronico:
            return "El correo electrónico ya está en uso."
        if usuario_existente.rfc_receptor == rfc_receptor:
            return "El RFC ya está en uso."
    # Si el correo electrónico y el RFC no están en uso, procedemos a registrar al usuario
    contraseña_hash = generate_password_hash(contraseña)
    usuario = Usuario(nombre_usuario=nombre_usuario, contraseña_hash=contraseña_hash, correo_electronico=correo_electronico, rfc_receptor=rfc_receptor, domicilio=domicilio, es_empleado=es_empleado)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

# Esta función se utiliza para verificar las credenciales de un usuario que intenta iniciar sesión
def verificar_usuario(db: Session, correo_electronico: str, contraseña: str):
    """
    Verifica las credenciales de un usuario que intenta iniciar sesión.

    Args:
        db (Session): La sesión de la base de datos.
        correo_electronico (str): El correo electrónico del usuario.
        contraseña (str): La contraseña del usuario.

    Returns:
        Usuario: El objeto de usuario si las credenciales son válidas, None si no lo son.
    """
    usuario = db.query(Usuario).filter(Usuario.correo_electronico == correo_electronico).first()
    if usuario and check_password_hash(usuario.contraseña_hash, contraseña):
        return usuario
    return None

def obtener_rfc(db: Session, correo_electronico: str):
    """
    Obtiene el RFC asociado al correo electrónico del usuario.

    Args:
        db (Session): La sesión de la base de datos.
        correo_electronico (str): El correo electrónico del usuario.

    Returns:
        str: El RFC del usuario.
    """
    usuario = db.query(Usuario).filter(Usuario.correo_electronico == correo_electronico).first()
    return usuario.rfc_receptor
# main.py
import re
import streamlit as st
import time
from services.auth_service import get_db, registrar_usuario, verificar_usuario, obtener_rfc
from models import Usuario
from services.factura_service import (
    crear_factura, 
    obtener_tipo_comprobante, 
    obtener_uso_destino_cfdi, 
    obtener_regimen_fiscal, 
    obtener_metodos_pago, 
    obtener_formas_pago, 
    obtener_productos_servicios,
    obtener_precio_unitario,
    calcular_valores_factura
)
from utils.factura_pdf_util import generar_pdf, obtener_datos, guardar_factura_pdf

# Definir la función principal que se ejecutará cuando se inicie el script
def main():
    """
    Función principal que maneja el proceso de inicio de sesión y registro.

    La función muestra un menú con opciones para iniciar sesión y registrarse.
    Dependiendo de la elección del usuario, solicita una entrada y realiza las acciones correspondientes.

    Returns:
        None
    """

    # Encabezado
    with st.container():
        col1, col2 = st.columns([6, 1])
        with col1:
            st.title("FACTURAS CFDI 3.3")
            st.write("FARMACIAS DE DIOS")
        with col2:
            st.image("app/utils/logo.png", width=100)

    # Si el usuario ha iniciado sesión
    if "usuario" in st.session_state:
        col1, col2 = st.columns([7.5, 2])
        with col2:
            # Agregar un botón para cerrar la sesión
            if st.button("📤 Cerrar sesión"):
                # Eliminar "usuario" del st.session_state para cerrar la sesión
                del st.session_state["usuario"]
                # Redirigir al usuario a la pantalla de inicio
                with st.spinner('Cerrando sesión'):
                    time.sleep(2)
                st.rerun()

        # Llamar a la función para generar la factura
        generar_factura()
    
    else:
        # Crear dos pestañas, una para mostrar el inicio de sesión y otra para mostrar el registro
        col1, col2 = st.columns([1, 2])
        with col2:
            with st.expander("🔓 Iniciar sesión o registrarse:"):
                tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
                with tab1:
                    mostrar_inicio_sesión()
                with tab2:
                    tab1, tab2 = st.tabs(["Cliente", "Empleado"])
                    if tab1:
                        mostrar_registro(es_empleado=False)
                    elif tab2:
                        mostrar_registro(es_empleado=True)

# Si el usuario selecciona "Inicio de sesión"
def mostrar_inicio_sesión():
    """
    Muestra la interfaz de inicio de sesión y realiza la validación de las credenciales ingresadas.

    Returns:
        None
    """
    # Mostrar un subencabezado
    st.subheader("👤 Iniciar sesión")
    # Crear marcadores de posición para los campos de entrada de correo electrónico y contraseña
    correo_electronico_placeholder = st.empty()
    contraseña_placeholder = st.empty()

    # Crear campos de entrada para el correo electrónico y la contraseña
    correo_electronico = correo_electronico_placeholder.text_input("Correo electrónico")
    contraseña = contraseña_placeholder.text_input("Contraseña", type='password')

    # Si el usuario hace clic en el botón "Iniciar sesión"
    if st.button("Iniciar sesión"):
        # Abrir una nueva sesión de base de datos
        with get_db() as db:
            # Buscar al usuario en la base de datos por correo electrónico
            usuario = db.query(Usuario).filter(Usuario.correo_electronico == correo_electronico).first()
            # Si el usuario existe
            if usuario:
                # Verificar la contraseña del usuario
                usuario = verificar_usuario(db, correo_electronico, contraseña)
                
                # Si la contraseña es correcta
                if usuario:
                    # Obtener el rfc_receptor del usuario
                    rfc_receptor = obtener_rfc(db, correo_electronico)
                    # Almacenar el estado de inicio de sesión en la sesión
                    st.session_state["usuario"] = usuario
                    # Mostrar un mensaje de éxito
                    st.success("Has iniciado sesión correctamente")
                    # Refrescar la página para mostrar solo la pestaña de generar factura
                    st.experimental_rerun()
                # Si la contraseña es incorrecta
                else:
                    # Mostrar un mensaje de error
                    st.error("El correo electrónico o la contraseña son incorrectos")
            # Si el correo electrónico es incorrecto
            else:
                # Mostrar un mensaje de error
                st.error("El correo electrónico o la contraseña son incorrectos")


# Si el usuario selecciona "Registro"
def mostrar_registro(es_empleado: bool = False):
    """
    Muestra el formulario de registro y realiza la validación de los campos ingresados.

    Args:
        es_empleado (bool): Indica si el usuario es un empleado.

    Returns:
        None
    """
    st.subheader("✍🏼 Registrarse")

    # Crear marcadores de posición para los campos de entrada
    nombre_usuario_placeholder = st.empty()
    contraseña_placeholder = st.empty()
    correo_electronico_placeholder = st.empty()
    rfc_receptor_placeholder = st.empty()

    with st.popover("Domicilio"):
        calle_placeholder = st.empty()
        numero_exterior_placeholder = st.empty()
        numero_interior_placeholder = st.empty()
        colonia_placeholder = st.empty()
        municipio_placeholder = st.empty()
        codigo_postal_placeholder = st.empty()
        estado_placeholder = st.empty()
        pais_placeholder = st.empty()

    # Crear campos de entrada para el nombre de usuario, la contraseña, el correo electrónico, el RFC y el domicilio
    nombre_usuario = nombre_usuario_placeholder.text_input("Nombre completo").upper()
    contraseña = contraseña_placeholder.text_input("Contraseña", type='password', key="contraseña_registro")
    correo_electronico = correo_electronico_placeholder.text_input("Correo electrónico", key="correo_electronico_registro")
    rfc_receptor = rfc_receptor_placeholder.text_input("RFC").upper()

    # Crear campos de entrada para los detalles del domicilio
    calle = calle_placeholder.text_input("Calle").upper()
    numero_exterior = numero_exterior_placeholder.text_input("Número exterior").upper()
    numero_interior = numero_interior_placeholder.text_input("Número interior (opcional)").upper()
    colonia = colonia_placeholder.text_input("Colonia").upper()
    municipio = municipio_placeholder.text_input("Municipio").upper()
    codigo_postal = codigo_postal_placeholder.text_input("Código postal").upper()
    estado = estado_placeholder.text_input("Estado").upper()
    pais = pais_placeholder.text_input("País").upper()

    # Unir los detalles del domicilio con ", " como separador
    domicilio = ", ".join([calle, numero_exterior, numero_interior, colonia, municipio, codigo_postal, estado, pais])

    # Si el usuario hace clic en el botón "Finalizar registro"
    if st.button("Finalizar registro"):
        # Si todos los campos están llenos
        if nombre_usuario and contraseña and correo_electronico and rfc_receptor and calle and numero_exterior and colonia and codigo_postal and municipio and estado and pais:
            # Si el usuario no ha ingresado al menos tres nombres, mostrar un mensaje de error
            if len(nombre_usuario.split(' ')) < 3:
                st.error("Ingresa tu nombre completo")
            # Si el RFC no tiene 13 caracteres, mostrar un mensaje de error
            elif len(rfc_receptor) != 13:
                st.error("El RFC debe tener exactamente 13 caracteres")
            # Si el correo electrónico no tiene una estructura válida, mostrar un mensaje de error
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo_electronico):
                st.error("El correo electrónico no tiene una estructura válida")
            else:
                # Abrir una nueva sesión de base de datos
                with get_db() as db:
                    # Buscar al usuario en la base de datos por correo electrónico o RFC
                    usuario_existente = db.query(Usuario).filter((Usuario.correo_electronico == correo_electronico) | (Usuario.rfc_receptor == rfc_receptor)).first()
                    # Si el usuario existe, mostrar un mensaje de error específico
                    if usuario_existente:
                        if usuario_existente.correo_electronico == correo_electronico:
                            st.error("El correo electrónico ya está registrado.")
                        if usuario_existente.rfc_receptor == rfc_receptor:
                            st.error("El RFC ya está registrado.")
                    else:
                        # Registrar al usuario
                        usuario = registrar_usuario(db, nombre_usuario, contraseña, correo_electronico, rfc_receptor, domicilio, es_empleado)
                        # Si el registro fue exitoso
                        if isinstance(usuario, str):
                            # Mostrar un mensaje de error
                            st.error(usuario)
                        else:
                            # Mostrar un mensaje de éxito
                            st.success("Usuario registrado con éxito. Puedes regresar a la pantalla de inicio de sesión para ingresar.")
                            # Borrar los campos de entrada
                            nombre_usuario_placeholder.empty()
                            contraseña_placeholder.empty()
                            correo_electronico_placeholder.empty()
                            rfc_receptor_placeholder.empty()
                            calle_placeholder = st.empty()
                            numero_exterior_placeholder = st.empty()
                            numero_interior_placeholder = st.empty()
                            colonia_placeholder = st.empty()
                            municipio_placeholder = st.empty()
                            codigo_postal_placeholder = st.empty()
                            estado_placeholder = st.empty()
                            pais_placeholder = st.empty()
        else:
            # Si no todos los campos están llenos, mostrar un mensaje de error
            st.error("Todos los campos son obligatorios")

# Función para generar una factura
def generar_factura():
    """
    Genera una factura con los datos ingresados por el usuario.

    Esta función obtiene los datos necesarios para generar una factura, como el uso destino CFDI,
    el tipo de comprobante, el régimen fiscal, etc. Luego, calcula los valores de la factura
    y agrega los datos a la base de datos. Si la generación de la factura es exitosa, se muestra
    un mensaje de éxito y se ofrece la opción de descargar el PDF de la factura o enviarla por correo.

    Args:
        None

    Returns:
        None
    """
    # Obtener el usuario de la sesión
    usuario = st.session_state["usuario"]
    # Abrir una nueva sesión de base de datos
    with get_db() as db:
        # Redirigir a un nuevo menú para generar facturas
        st.subheader("📝 Factura")

        # Crear marcadores de posición para los campos de entrada
        uso_destino_cfdi_placeholder = st.empty()
        tipo_comprobante_clave_placeholder = st.empty()
        regimen_fiscal_clave_placeholder = st.empty()
        clave_producto_servicio_placeholder = st.empty()
        cantidad_placeholder = st.empty()
        metodo_pago_clave_placeholder = st.empty()
        forma_pago_clave_placeholder = st.empty()

        # Crear campos de entrada para los datos de la factura
        uso_destino_cfdi_opciones = obtener_uso_destino_cfdi(db)
        uso_destino_cfdi = uso_destino_cfdi_placeholder.selectbox("Uso Destino CFDI", uso_destino_cfdi_opciones)

        tipo_comprobante_clave_opciones = obtener_tipo_comprobante(db)
        tipo_comprobante_clave = tipo_comprobante_clave_placeholder.selectbox("Tipo de Comprobante", tipo_comprobante_clave_opciones)

        regimen_fiscal_clave_opciones = obtener_regimen_fiscal(db)
        regimen_fiscal_clave = regimen_fiscal_clave_placeholder.selectbox("Regimen Fiscal", regimen_fiscal_clave_opciones)

        rfc_receptor = usuario.rfc_receptor

        clave_producto_servicio_opciones = obtener_productos_servicios(db)
        clave_producto_servicio = clave_producto_servicio_placeholder.selectbox("Clave Producto o Servicio", clave_producto_servicio_opciones)

        cantidad = cantidad_placeholder.number_input("Cantidad", min_value=1)

        metodo_pago_clave_opciones = obtener_metodos_pago(db)
        metodo_pago_clave = metodo_pago_clave_placeholder.selectbox("Metodo de Pago", metodo_pago_clave_opciones)

        formas_pago = obtener_formas_pago(db)
        forma_pago_clave = forma_pago_clave_placeholder.selectbox("Forma de Pago", formas_pago)

        precio_unitario = obtener_precio_unitario(db, clave_producto_servicio)
            
        # Calcula los valores de la factura
        valores_factura = calcular_valores_factura(db, {
            'clave_producto_servicio': clave_producto_servicio,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario
        })

        col1, col2 = st.columns([8, 2.5])
        with col2:
            # Si el usuario hace clic en el botón "Generar Factura"
            if st.button("✅ Generar Factura"):

                # Agregar los datos de la factura a la base de datos
                factura = crear_factura(db, {
                    'uso_destino_cfdi_clave': uso_destino_cfdi,
                    'tipo_comprobante_clave': tipo_comprobante_clave,
                    'regimen_fiscal_clave': regimen_fiscal_clave,
                    'rfc_receptor': rfc_receptor,
                    'clave_producto_servicio': clave_producto_servicio,
                    'cantidad': cantidad,
                    'metodo_pago_clave': metodo_pago_clave,
                    'forma_pago_clave': forma_pago_clave,
                    'precio_unitario': precio_unitario,
                    'importe': valores_factura['importe'],
                    'subtotal': valores_factura['subtotal'],
                    'iva': valores_factura['iva'],
                    'total': valores_factura['total']
                })
                # Si la generación de la factura fue exitosa
                if factura:
                    id_factura = factura.id
                    datos_factura = obtener_datos(db, id_factura)
                        
                    pdf_bytes = generar_pdf(datos_factura)
                    guardar_factura_pdf(db, id_factura, pdf_bytes)
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        # Mostrar un mensaje de éxito
                        st.success("Factura generada con éxito")
                    
                    with col2:
                        st.download_button('⬇️ Descargar PDF', pdf_bytes, file_name='Factura.pdf', mime='application/pdf')

                    # Borrar los campos de entrada
                    uso_destino_cfdi_placeholder.empty()
                    tipo_comprobante_clave_placeholder.empty()
                    regimen_fiscal_clave_placeholder.empty()
                    clave_producto_servicio_placeholder.empty()
                    cantidad_placeholder.empty()
                    metodo_pago_clave_placeholder.empty()
                    forma_pago_clave_placeholder.empty()
                else:
                    # Si la generación de la factura falló, mostrar un mensaje de error
                    st.error("Error al generar la factura")

# Si el script se ejecuta como el script principal, llamar a la función main
if __name__ == "__main__":
    main()
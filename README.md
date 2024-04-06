# 💻 FACTURA CDFI 3.3
Este proyecto es una aplicación web para generar facturas electrónicas (CFDI 3.3) de manera sencilla y eficiente. Está diseñada para pequeñas empresas, autónomos y freelancers que necesitan crear facturas de forma rápida y precisa.


## 📌 Características principales
- **Inicio de sesión y registro de usuarios:** Permite a los usuarios crear una cuenta o iniciar sesión para acceder a la funcionalidad de generación de facturas.
- **Generación de facturas:** Permite a los usuarios generar facturas electrónicas utilizando un formulario intuitivo. Los usuarios pueden especificar detalles como el tipo de comprobante, el uso destino CFDI, el método de pago, la forma de pago, entre otros.
- **Descarga de PDF y envío por correo electrónico:** Después de generar una factura, los usuarios tienen la opción de descargar el PDF de la factura o enviarlo por correo electrónico directamente desde la aplicación.
- **Validación de datos:** La aplicación realiza validaciones en tiempo real para garantizar que los datos ingresados por los usuarios sean correctos y cumplan con los requisitos del SAT (Servicio de Administración Tributaria) de México.
- **Diseño intuitivo y amigable:** La interfaz de usuario está diseñada para ser fácil de usar, con indicaciones claras y elementos visuales que guían al usuario a través del proceso de generación de facturas.


## 🔏 Tecnologías utilizadas
- **Python:** El backend de la aplicación está escrito en Python, utilizando Streamlit para crear la interfaz de usuario y gestionar las funcionalidades.
- **PostgreSQL:** Se utiliza PostgreSQL como base de datos relacional para almacenar la información de los usuarios y las facturas generadas.
- **SQLAlchemy:** Se utiliza SQLAlchemy como ORM (Mapeo Objeto-Relacional) para interactuar con la base de datos PostgreSQL desde Python de manera eficiente y segura.


## ⬇️ Instalación y ejecución
Para ejecutar la aplicación localmente, sigue estos pasos:

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias utilizando el archivo `requirements.txt`.
3. Configura una base de datos PostgreSQL y actualiza las credenciales en el archivo de configuración.
4. Ejecuta el script `main.py` para iniciar la aplicación.
5. Abre tu navegador web y accede a la dirección proporcionada por Streamlit para interactuar con la aplicación.

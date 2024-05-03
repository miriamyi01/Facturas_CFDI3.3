-- Tabla para el login de clientes
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,  -- Identificador único para cada usuario
    nombre_usuario VARCHAR(255) NOT NULL,  -- Nombre de usuario
    contraseña_hash VARCHAR(255) NOT NULL,  -- Contraseña hasheada
    correo_electronico VARCHAR(255) UNIQUE NOT NULL,  -- Correo electrónico del usuario (único)
    rfc_receptor VARCHAR(20) UNIQUE NOT NULL,  -- RFC del receptor (único)
    domicilio VARCHAR(255) NOT NULL  -- Domicilio del usuario
    es_empleado BOOLEAN NOT NULL DEFAULT FALSE;
);

-- Tabla para el inventario
CREATE TABLE productos_servicios (
    clave_producto_servicio VARCHAR(10) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del producto o servicio (única)
    unidad VARCHAR(255) NOT NULL,  -- Unidad de medida del producto o servicio
    descripcion VARCHAR(255) NOT NULL,  -- Descripción del producto o servicio
    precio_unitario DECIMAL(10, 2) NOT NULL  -- Precio unitario del producto o servicio
);

-- Tablas para la información de la factura
CREATE TABLE tipo_comprobante (
    clave VARCHAR(1) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de comprobante (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de comprobante
);

CREATE TABLE uso_destino_cfdi (
    clave VARCHAR(4) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del uso o destino CFDI (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del uso o destino CFDI
);

CREATE TABLE regimen_fiscal (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del régimen fiscal (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del régimen fiscal
);

CREATE TABLE metodos_pago (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del método de pago (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del método de pago
);

CREATE TABLE formas_pago (
    clave VARCHAR(2) PRIMARY KEY NOT NULL UNIQUE,  -- Clave de la forma de pago (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción de la forma de pago
);

-- Opciones usadas en el CFDI 3.3
-- Se insertan valores en las tablas de tipo_comprobante, uso_destino_cfdi, regimen_fiscal, metodos_pago y formas_pago.
-- Datos del tipo de comprobante
INSERT INTO formas_pago (clave, descripcion) VALUES
('01', 'EFECTIVO'),
('02', 'CHEQUE NOMINATIVO'),
('03', 'TRANSFERENCIA ELECTRÓNICA DE FONDOS'),
('04', 'TARJETA DE CRÉDITO'),
('05', 'MONEDERO ELECTRÓNICO'),
('06', 'DINERO ELECTRÓNICO'),
('08', 'VALES DE DESPENSA'),
('12', 'DACIÓN EN PAGO'),
('13', 'PAGO POR SUBROGACIÓN'),
('14', 'PAGO POR CONSIGNACIÓN'),
('15', 'CONDONACIÓN'),
('17', 'COMPENSACIÓN'),
('23', 'NOVACIÓN'),
('24', 'CONFUSIÓN'),
('25', 'REMITIÓ DEUDA'),
('26', 'PRESCRIPCIÓN O CADUCIDAD'),
('27', 'A SATISFACCIÓN DEL ACREEDOR'),
('28', 'TARJETA DE DÉBITO'),
('29', 'TARJETA DE SERVICIOS'),
('30', 'APLICACIÓN DE ANTICIPOS'),
('99', 'POR DEFINIR');

-- Datos del método de pago
INSERT INTO metodos_pago (clave, descripcion) VALUES
('PUE', 'PAGO EN UNA SOLA EXHIBICIÓN'),
('PPD', 'PAGO EN PARCIALIDADES O DIFERIDO');

-- Datos del régimen fiscal
INSERT INTO regimen_fiscal (clave, descripcion) VALUES
('601', 'GENERAL DE LEY PERSONAS MORALES'),
('603', 'PERSONAS MORALES CON FINES NO LUCRATIVOS'),
('605', 'SUELDOS Y SALARIOS E INGRESOS ASIMILADOS A SALARIOS'),
('606', 'ARRENDAMIENTO'),
('607', 'RÉGIMEN DE ENAJENACIÓN O ADQUISICIÓN DE BIENES'),
('608', 'DEMÁS INGRESOS'),
('609', 'CONSOLIDACIÓN'),
('610', 'RESIDENTES EN EL EXTRANJERO SIN ESTABLECIMIENTO PERMANENTE EN MÉXICO'),
('611', 'INGRESOS POR DIVIDENDOS (SOCIOS Y ACCIONISTAS)'),
('612', 'PERSONAS FÍSICAS CON ACTIVIDADES EMPRESARIALES Y PROFESIONALES'),
('614', 'INGRESOS POR INTERESES'),
('615', 'RÉGIMEN DE LOS INGRESOS POR OBTENCIÓN DE PREMIOS'),
('616', 'SIN OBLIGACIONES FISCALES'),
('620', 'SOCIEDADES COOPERATIVAS DE PRODUCCIÓN QUE OPTAN POR DIFERIR SUS INGRESOS'),
('621', 'INCORPORACIÓN FISCAL'),
('622', 'ACTIVIDADES AGRÍCOLAS, GANADERAS, SILVÍCOLAS Y PESQUERAS'),
('623', 'OPCIONAL PARA GRUPOS DE SOCIEDADES'),
('624', 'COORDINADOS'),
('625', 'RÉGIMEN DE LAS ACTIVIDADES EMPRESARIALES CON INGRESOS A TRAVÉS DE PLATAFORMAS TECNOLÓGICAS'),
('626', 'RÉGIMEN SIMPLIFICADO DE CONFIANZA'),
('628', 'HIDROCARBUROS'),
('629', 'DE LOS REGÍMENES FISCALES PREFERENTES Y DE LAS EMPRESAS MULTINACIONALES'),
('630', 'ENAJENACIÓN DE ACCIONES EN BOLSA DE VALORES');

-- Datos del tipo de comprobante
INSERT INTO tipo_comprobantes (clave, descripcion) VALUES
('I', 'INGRESO'),
('E', 'EGRESO');

-- Datos del uso o destino CFDI
INSERT INTO uso_destino_cfdi (clave, descripcion) VALUES
('G01', 'ADQUISICIÓN DE MERCANCÍAS'),
('G02', 'DEVOLUCIONES, DESCUENTOS O BONIFICACIONES'),
('G03', 'GASTOS EN GENERAL'),
('I01', 'CONSTRUCCIONES'),
('I02', 'MOBILIARIO Y EQUIPO DE OFICINA POR INVERSIONES'),
('I03', 'EQUIPO DE TRANSPORTE'),
('I04', 'EQUIPO DE CÓMPUTO Y ACCESORIOS'),
('I05', 'DADOS, TROQUELES, MOLDES, MATRICES Y HERRAMENTAL'),
('I06', 'COMUNICACIONES TELEFÓNICAS'),
('I07', 'COMUNICACIONES SATELITALES'),
('I08', 'OTRA MAQUINARIA Y EQUIPO'),
('D01', 'HONORARIOS MÉDICOS, DENTALES Y GASTOS HOSPITALARIOS'),
('D02', 'GASTOS MÉDICOS POR INCAPACIDAD O DISCAPACIDAD'),
('D03', 'GASTOS FUNERALES'),
('D04', 'DONATIVOS'),
('D05', 'INTERESES REALES EFECTIVAMENTE PAGADOS POR CRÉDITOS HIPOTECARIOS (CASA HABITACIÓN)'),
('D06', 'APORTACIONES VOLUNTARIAS AL SAR'),
('D07', 'PRIMAS POR SEGUROS DE GASTOS MÉDICOS'),
('D08', 'GASTOS DE TRANSPORTACIÓN ESCOLAR OBLIGATORIA'),
('D09', 'DEPÓSITOS EN CUENTAS PARA EL AHORRO, PRIMAS QUE TENGAN COMO BASE PLANES DE PENSIONES'),
('D10', 'PAGOS POR SERVICIOS EDUCATIVOS (COLEGIATURAS)'),
('CP01', 'PAGOS'),
('CN01', 'NÓMINA'),
('S01', 'SIN EFECTOS FISCALES');



-- Tabla principal para la creación de facturas
CREATE TABLE facturas (
    -- Encabezado
    id SERIAL PRIMARY KEY,  -- Identificador único para cada factura
    nombre_empresa VARCHAR(50) DEFAULT 'FARMACIAS DE DIOS' NOT NULL,  -- Nombre de la empresa

    -- Primera sección
    uso_destino_cfdi_clave VARCHAR(4) NOT NULL REFERENCES uso_destino_cfdi(clave),  -- Clave del uso o destino CFDI
    lugar_expedicion VARCHAR(20) DEFAULT 'CIUDAD DE MÉXICO' NOT NULL,  -- Lugar de expedición
    fecha_expedicion TIMESTAMP NOT NULL,  -- Fecha de expedición
    rfc_emisor VARCHAR(20) DEFAULT 'FARA2402035H8' NOT NULL,  -- RFC del emisor
    tipo_comprobante_clave VARCHAR(1) NOT NULL REFERENCES tipo_comprobante(clave),  -- Clave del tipo de comprobante
    regimen_fiscal_clave VARCHAR(3) NOT NULL REFERENCES regimen_fiscal(clave),  -- Clave del régimen fiscal

    -- Segunda sección
    rfc_receptor VARCHAR(20) NOT NULL REFERENCES usuarios(rfc_receptor),  -- RFC del receptor

    -- Tercera sección
    clave_producto_servicio VARCHAR(255) NOT NULL REFERENCES productos_servicios(clave_producto_servicio),  -- Clave del producto o servicio
    cantidad INTEGER NOT NULL,  -- Cantidad de productos o servicios
    importe DECIMAL (10, 2) NOT NULL,  -- Importe

    -- Cuarta sección
    subtotal DECIMAL(10, 2) NOT NULL,  -- Subtotal
    iva DECIMAL(10, 2) NOT NULL,  -- IVA
    total DECIMAL(10, 2) NOT NULL,  -- Total
    total_con_letra VARCHAR(255) NOT NULL,  -- Total con letra
    moneda VARCHAR(20) DEFAULT 'MXN Pesos Mexicanos' NOT NULL,  -- Moneda
    tipo_cambio DECIMAL(10, 2) DEFAULT 0.00 NOT NULL,  -- Tipo de cambio
    metodo_pago_clave VARCHAR(3) NOT NULL REFERENCES metodos_pago(clave),  -- Clave del método de pago
    forma_pago_clave VARCHAR(2) NOT NULL REFERENCES formas_pago(clave),  -- Clave de la forma de pago

    -- Quinta sección
    sello_digital_cfdi TEXT NOT NULL,  -- Sello digital CFDI
    sello_digital_sat TEXT NOT NULL,  -- Sello digital SAT
    cadena_original_complemento_certificacion TEXT NOT NULL,  -- Cadena original complemento certificación
    codigo_qr BYTEA NOT NULL  -- Código QR
);

CREATE TABLE facturas_pdf (
    id SERIAL PRIMARY KEY,  -- Identificador único para cada factura PDF
    id_factura INTEGER NOT NULL REFERENCES facturas(id),  -- ID de la factura asociada
    pdf BYTEA NOT NULL  -- PDF de la factura
);



-- Datos del inventario (ejemplos)
-- Se insertan algunos productos de ejemplo en la tabla de productos_servicios.
INSERT INTO productos_servicios (clave_producto_servicio, unidad, descripcion, precio_unitario) VALUES
('1A1B1', 'PIEZA', 'PARACETAMOL', 10.00),
('2B2C2', 'PIEZA', 'IBUPROFENO', 15.00),
('3C3D3', 'PIEZA', 'ASPIRINA', 5.00),
('4D4E4', 'PIEZA', 'DICLOFENACO', 20.00),
('5E5F5', 'PIEZA', 'OMEPRAZOL', 25.00),
('6F6G6', 'PIEZA', 'RANITIDINA', 30.00),
('7G7H7', 'PIEZA', 'LORATADINA', 35.00),
('8H8I8', 'PIEZA', 'CLORFENAMINA', 40.00),
('9I9J9', 'PIEZA', 'DEXTROMETORFANO', 45.00),
('0J0K0', 'PIEZA', 'AMBROXOL', 50.00);
-- CÁTALOGOS: https://apisandbox.facturama.mx/ --
-- NOMBRE: cfdi_facturas --

------------------------------------------------------------
-------------------- BASE PARA FACTURAS --------------------
-----------------------------------------------------------

-- Tabla para el login de clientes
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,  -- Identificador único para cada usuario
    nombre_usuario VARCHAR(255) NOT NULL,  -- Nombre de usuario
    contraseña_hash VARCHAR(255) NOT NULL,  -- Contraseña hasheada
    correo_electronico VARCHAR(255) UNIQUE NOT NULL,  -- Correo electrónico del usuario (único)
    rfc_receptor VARCHAR(20) UNIQUE NOT NULL,  -- RFC del receptor (único)
    domicilio VARCHAR(255) NOT NULL,  -- Domicilio del usuario
    es_empleado BOOLEAN NOT NULL DEFAULT FALSE
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
INSERT INTO tipo_comprobante (clave, descripcion) VALUES
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
    moneda VARCHAR(20) DEFAULT 'MXN PESOS MEXICANOS' NOT NULL,  -- Moneda
    tipo_cambio DECIMAL(10, 2) DEFAULT 0.00 NOT NULL,  -- Tipo de cambio
    metodo_pago_clave VARCHAR(3) NOT NULL REFERENCES metodos_pago(clave),  -- Clave del método de pago
    forma_pago_clave VARCHAR(2) NOT NULL REFERENCES formas_pago(clave),  -- Clave de la forma de pago

    -- Quinta sección
    sello_digital_cfdi TEXT NOT NULL,  -- Sello digital CFDI
    sello_digital_sat TEXT NOT NULL,  -- Sello digital SAT
    cadena_original_complemento_certificacion TEXT NOT NULL,  -- Cadena original complemento certificación
    codigo_qr BYTEA NOT NULL  -- Código QR
);

-- Tabla para almacenar los PDF de las facturas
CREATE TABLE facturas_pdf (
    id SERIAL PRIMARY KEY,  -- Identificador único para cada factura PDF
    id_factura INTEGER NOT NULL REFERENCES facturas(id),  -- ID de la factura asociada
    pdf BYTEA NOT NULL  -- PDF de la factura
);


-- Ejemplos de datos del inventario
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





------------------------------------------------------------
--------------------- BASE PARA NÓMINA ---------------------
-----------------------------------------------------------

-- Tablas para la información del empleado
CREATE TABLE departamento (
    id VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del departamento (única)
    nombre VARCHAR(255) NOT NULL  -- Nombre del departamento
);

CREATE TABLE riesgo (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de riesgo (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de riesgo
);

CREATE TABLE puestos (
    id SERIAL PRIMARY KEY,  -- Identificador único para cada puesto
    nombre VARCHAR(255) NOT NULL,  -- Nombre del puesto
    departamento_id VARCHAR(255) NOT NULL,  -- ID del departamento al que pertenece el puesto
    riesgo_clave VARCHAR(255) NOT NULL,  -- ID del riesgo al que pertenece el puesto
    FOREIGN KEY (departamento_id) REFERENCES departamento(id),  -- Relación con la tabla de departamentos
    FOREIGN KEY (riesgo_clave) REFERENCES riesgo(clave)  -- Relación con la tabla de riesgos
);

CREATE TABLE jornada (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de jornada (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de jornada
);

CREATE TABLE contrato (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de contrato (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de contrato
);

CREATE TABLE periodicidad (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de periodicidad (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de periodicidad
);


-- Tabla para el login de empleados
CREATE TABLE empleados (
    numero_empleado VARCHAR(18) NOT NULL UNIQUE PRIMARY KEY,  -- Identificador único para cada empleado
    curp VARCHAR(18) NOT NULL UNIQUE,  -- CURP del empleado
    nss VARCHAR(11) NOT NULL UNIQUE,  -- NSS del empleado
    fecha_ingreso DATE NOT NULL,  -- Fecha de ingreso del empleado
    sueldo_base DECIMAL(10, 2) NOT NULL,  -- Sueldo base del empleado
    puesto_id INT NOT NULL REFERENCES puestos(id),  -- ID del puesto del empleado
    departamento_id VARCHAR(3) NOT NULL REFERENCES departamento(id),  -- ID del departamento del empleado
    riesgo_id VARCHAR(3) NOT NULL REFERENCES riesgo(clave),  -- ID del riesgo del empleado
    tipo_jornada VARCHAR(3) NOT NULL REFERENCES jornada(clave), -- Tipo de jornada del empleado
    tipo_contrato VARCHAR(3) NOT NULL REFERENCES contrato(clave), -- Tipo de contrato del empleado
    periodicidad_pago VARCHAR(3) NOT NULL REFERENCES periodicidad(clave) -- periodicidad de pago del empleado
);


-- Opciones usadas en el CFDI 3.3
-- Se insertan valores en las tablas de departamento, riesgo, puestos, jornada, contrato y periodicidad.
-- Datos del empleado
-- Ejemplos de departamentos
INSERT INTO departamento (id, nombre) VALUES
('D1', 'RECURSOS HUMANOS'),
('D2', 'FINANZAS'),
('D3', 'MARKETING'),
('D4', 'VENTAS'),
('D5', 'PRODUCCIÓN'),
('D6', 'INVESTIGACIÓN Y DESARROLLO'),
('D7', 'SERVICIO AL CLIENTE'),
('D8', 'LOGÍSTICA'),
('D9', 'TECNOLOGÍA DE LA INFORMACIÓN'),
('D10', 'ADMINISTRACIÓN');

-- Tipos de riesgos
INSERT INTO riesgo (clave, descripcion) VALUES
('01', 'CLASE I'),
('02', 'CLASE II'),
('03', 'CLASE III'),
('04', 'CLASE IV'),
('05', 'CLASE V'),
('99', 'NO APLICA');

-- Ejemplos de 2 puestos específicos para cada departamento con riesgos asignados
INSERT INTO puestos (nombre, departamento_id, riesgo_clave) VALUES
('DIRECTOR DE RECURSOS HUMANOS', 'D1', '01'),
('ESPECIALISTA EN RECLUTAMIENTO', 'D1', '02'),
('DIRECTOR FINANCIERO', 'D2', '03'),
('ANALISTA FINANCIERO', 'D2', '04'),
('DIRECTOR DE MARKETING', 'D3', '05'),
('ESPECIALISTA EN MARKETING DIGITAL', 'D3', '01'),
('DIRECTOR DE VENTAS', 'D4', '02'),
('REPRESENTANTE DE VENTAS', 'D4', '03'),
('DIRECTOR DE PRODUCCIÓN', 'D5', '04'),
('SUPERVISOR DE PRODUCCIÓN', 'D5', '05'),
('DIRECTOR DE DESAROLLO', 'D6', '01'),
('CIENTÍFICO DE DATOS', 'D6', '02'),
('DIRECTOR DE SERVICIO AL CLIENTE', 'D7', '03'),
('REPRESENTANTE DE SERVICIO AL CLIENTE', 'D7', '04'),
('DIRECTOR DE LOGÍSTICA', 'D8', '05'),
('ANALISTA DE LOGÍSTICA', 'D8', '01'),
('DIRECTOR DE TI', 'D9', '02'),
('INGENIERO DE SOFTWARE', 'D9', '03'),
('DIRECTOR ADMINISTRATIVO', 'D10', '04'),
('ASISTENTE ADMINISTRATIVO', 'D10', '05');

-- Tipo de jornada
INSERT INTO jornada (clave, descripcion) VALUES
('01', 'DIURNA'),
('02', 'NOCTURNA'),
('03', 'MIXTA'),
('04', 'POR HORA'),
('05', 'REDUCIDA'),
('06', 'CONTINUADA'),
('07', 'PARTIDA'),
('08', 'POR TURNOS'),
('99', 'OTRA JORNADA');

-- Tipo de contrato
INSERT INTO contrato (clave, descripcion) VALUES
('01', 'CONTRATO DE TRABAJO POR TIEMPO INDETERMINADO'),
('02', 'CONTRATO DE TRABAJO PARA OBRA DETERMINADA'),
('03', 'CONTRATO DE TRABAJO POR TIEMPO DETERMINADO'),
('04', 'CONTRATO DE TRABAJO POR TEMPORADA'),
('05', 'CONTRATO DE TRABAJO SUJETO A PRUEBA'),
('06', 'CONTRATO DE TRABAJO CON CAPACITACIÓN INICIAL'),
('07', 'MODALIDAD DE CONTRATACIÓN POR PAGO DE HORA LABORADA'),
('08', 'MODALIDAD DE TRABAJO POR COMISIÓN LABORAL'),
('09', 'MODALIDADES DE CONTRATACIÓN DONDE NO EXISTE RELACIÓN DE TRABAJO'),
('10', 'JUBILACIÓN, PENSIÓN, RETIRO'),
('99', 'OTRO CONTRATO');

-- Tipo de periodicidad
INSERT INTO periodicidad (clave, descripcion) VALUES
('01', 'DIARIO'),
('02', 'SEMANAL'),
('03', 'CATORCENAL'),
('04', 'QUINCENAL'),
('05', 'MENSUAL'),
('06', 'BIMESTRAL'),
('07', 'UNIDAD OBRA'),
('08', 'COMISIÓN'),
('09', 'PRECIO ALZADO'),
('10', 'DECENAL'),
('99', 'OTRA PERIODICIDAD');


-- Se insertan valores en las tablas de percepciones y deducciones.
-- Datos del recibo
CREATE TABLE regimen_laboral (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de periodicidad (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de periodicidad
);

CREATE TABLE percepciones (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de periodicidad (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de periodicidad
);

CREATE TABLE deducciones (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de periodicidad (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de periodicidad
);

CREATE TABLE banco (
    clave VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,  -- Clave del tipo de periodicidad (única)
    descripcion VARCHAR(255) NOT NULL  -- Descripción del tipo de periodicidad
);

-- Tipo de regimen laboral
INSERT INTO regimen_laboral (clave, descripcion) VALUES
('02', 'SUELDOS'),
('03', 'JUBILADOS'),
('04', 'PENSIONADOS'),
('05', 'ASIMILADOS MIEMBROS SOCIEDADES COOPERATIVAS PRODUCCION'),
('06', 'ASIMILADOS INTEGRANTES SOCIEDADES ASOCIACIONES CIVILES'),
('07', 'ASIMILADOS MIEMBROS CONSEJOS'),
('08', 'ASIMILADOS COMISIONISTAS'),
('09', 'ASIMILADOS HONORARIOS'),
('10', 'ASIMILADOS ACCIONES'),
('11', 'ASIMILADOS OTROS'),
('12', 'JUBILADOS O PENSIONADOS'),
('13', 'INDEMNIZACIÓN O SEPARACIÓN'),
('99', 'OTRO REGIMEN');

-- Tipo de percepciones
INSERT INTO percepciones (clave, descripcion) VALUES
('001', 'SUELDOS, SALARIOS, RAYAS Y JORNALES'),
('002', 'GRATIFICACIÓN ANUAL (AGUINALDO)'),
('003', 'PARTICIPACIÓN DE LOS TRABAJADORES EN LAS UTILIDADES PTU'),
('004', 'REEMBOLSO DE GASTOS MÉDICOS DENTALES Y HOSPITALARIOS'),
('005', 'FONDO DE AHORRO'),
('006', 'CAJA DE AHORRO'),
('009', 'CONTRIBUCIONES A CARGO DEL TRABAJADOR PAGADAS POR EL PATRÓN'),
('010', 'PREMIOS POR PUNTUALIDAD'),
('011', 'PRIMA DE SEGURO DE VIDA'),
('012', 'SEGURO DE GASTOS MÉDICOS MAYORES'),
('013', 'CUOTAS SINDICALES PAGADAS POR EL PATRÓN'),
('014', 'SUBSIDIOS POR INCAPACIDAD'),
('015', 'BECAS PARA TRABAJADORES Y/O HIJOS'),
('019', 'HORAS EXTRA'),
('020', 'PRIMA DOMINICAL'),
('021', 'PRIMA VACACIONAL'),
('022', 'PRIMA POR ANTIGÜEDAD'),
('023', 'PAGOS POR SEPARACIÓN'),
('024', 'SEGURO DE RETIRO'),
('025', 'INDEMNIZACIONES'),
('026', 'REEMBOLSO POR FUNERAL'),
('027', 'CUOTAS DE SEGURIDAD SOCIAL PAGADAS POR EL PATRÓN'),
('028', 'COMISIONES'),
('029', 'VALES DE DESPENSA'),
('030', 'VALES DE RESTAURANTE'),
('031', 'VALES DE GASOLINA'),
('032', 'VALES DE ROPA'),
('033', 'AYUDA PARA RENTA'),
('034', 'AYUDA PARA ARTÍCULOS ESCOLARES'),
('035', 'AYUDA PARA ANTEOJOS'),
('036', 'AYUDA PARA TRANSPORTE'),
('037', 'AYUDA PARA GASTOS DE FUNERAL'),
('038', 'OTROS INGRESOS POR SALARIOS'),
('039', 'JUBILACIONES, PENSIONES O HABERES DE RETIRO'),
('044', 'JUBILACIONES, PENSIONES O HABERES DE RETIRO EN PARCIALIDADES'),
('045', 'INGRESOS EN ACCIONES O TÍTULOS VALOR QUE REPRESENTAN BIENES'),
('046', 'INGRESOS ASIMILADOS A SALARIOS'),
('047', 'ALIMENTACIÓN'),
('048', 'HABITACIÓN'),
('049', 'PREMIOS POR ASISTENCIA'),
('050', 'VIÁTICOS'),
('051', 'PAGOS POR GRATIFICACIONES, PRIMAS, COMPENSACIONES, RECOMPENSAS U OTROS A EXTRABAJADORES DERIVADOS DE JUBILACIÓN EN PARCIALIDADES'),
('052', 'PAGOS QUE SE REALICEN A EXTRABAJADORES QUE OBTENGAN UNA JUBILACIÓN EN PARCIALIDADES DERIVADOS DE LA EJECUCIÓN DE RESOLUCIONES JUDICIALES O DE UN LAUDO'),
('053', 'PAGOS QUE SE REALICEN A EXTRABAJADORES QUE OBTENGAN UNA JUBILACIÓN EN UNA SOLA EXHIBICIÓN DERIVADOS DE LA EJECUCIÓN DE RESOLUCIONES JUDICIALES O DE UN LAUDO');

-- Tipo de deducciones
INSERT INTO deducciones (clave, descripcion) VALUES
('001', 'SEGURIDAD SOCIAL'),
('002', 'ISR'),
('003', 'APORTACIONES A RETIRO, CESANTÍA EN EDAD AVANZADA Y VEJEZ.'),
('004', 'OTROS'),
('005', 'APORTACIONES A FONDO DE VIVIENDA'),
('006', 'DESCUENTO POR INCAPACIDAD'),
('007', 'PENSIÓN ALIMENTICIA'),
('008', 'RENTA'),
('009', 'PRÉSTAMOS PROVENIENTES DEL FONDO NACIONAL DE LA VIVIENDA PARA LOS TRABAJADORES'),
('010', 'PAGO POR CRÉDITO DE VIVIENDA'),
('011', 'PAGO DE ABONOS INFONACOT'),
('012', 'ANTICIPO DE SALARIOS'),
('013', 'PAGOS HECHOS CON EXCESO AL TRABAJADOR'),
('014', 'ERRORES'),
('015', 'PÉRDIDAS'),
('016', 'AVERÍAS'),
('017', 'ADQUISICIÓN DE ARTÍCULOS PRODUCIDOS POR LA EMPRESA O ESTABLECIMIENTO'),
('018', 'CUOTAS PARA LA CONSTITUCIÓN Y FOMENTO DE SOCIEDADES COOPERATIVAS Y DE CAJAS DE AHORRO'),
('019', 'CUOTAS SINDICALES'),
('020', 'AUSENCIA (AUSENTISMO)'),
('021', 'CUOTAS OBRERO PATRONALES'),
('022', 'IMPUESTOS LOCALES'),
('023', 'APORTACIONES VOLUNTARIAS'),
('024', 'AJUSTE EN GRATIFICACIÓN ANUAL (AGUINALDO) EXENTO'),
('025', 'AJUSTE EN GRATIFICACIÓN ANUAL (AGUINALDO) GRAVADO'),
('026', 'AJUSTE EN PARTICIPACIÓN DE LOS TRABAJADORES EN LAS UTILIDADES PTU EXENTO'),
('027', 'AJUSTE EN PARTICIPACIÓN DE LOS TRABAJADORES EN LAS UTILIDADES PTU GRAVADO'),
('028', 'AJUSTE EN REEMBOLSO DE GASTOS MÉDICOS DENTALES Y HOSPITALARIOS EXENTO'),
('029', 'AJUSTE EN FONDO DE AHORRO EXENTO'),
('030', 'AJUSTE EN CAJA DE AHORRO EXENTO'),
('031', 'AJUSTE EN CONTRIBUCIONES A CARGO DEL TRABAJADOR PAGADAS POR EL PATRÓN EXENTO'),
('032', 'AJUSTE EN PREMIOS POR PUNTUALIDAD GRAVADO'),
('033', 'AJUSTE EN PRIMA DE SEGURO DE VIDA EXENTO'),
('034', 'AJUSTE EN SEGURO DE GASTOS MÉDICOS MAYORES EXENTO'),
('035', 'AJUSTE EN CUOTAS SINDICALES PAGADAS POR EL PATRÓN EXENTO'),
('036', 'AJUSTE EN SUBSIDIOS POR INCAPACIDAD EXENTO'),
('037', 'AJUSTE EN BECAS PARA TRABAJADORES Y/O HIJOS EXENTO'),
('038', 'AJUSTE EN HORAS EXTRA EXENTO'),
('039', 'AJUSTE EN HORAS EXTRA GRAVADO'),
('040', 'AJUSTE EN PRIMA DOMINICAL EXENTO'),
('041', 'AJUSTE EN PRIMA DOMINICAL GRAVADO'),
('042', 'AJUSTE EN PRIMA VACACIONAL EXENTO'),
('043', 'AJUSTE EN PRIMA VACACIONAL GRAVADO'),
('044', 'AJUSTE EN PRIMA POR ANTIGÜEDAD EXENTO'),
('045', 'AJUSTE EN PRIMA POR ANTIGÜEDAD GRAVADO'),
('046', 'AJUSTE EN PAGOS POR SEPARACIÓN EXENTO'),
('047', 'AJUSTE EN PAGOS POR SEPARACIÓN GRAVADO'),
('048', 'AJUSTE EN SEGURO DE RETIRO EXENTO'),
('049', 'AJUSTE EN INDEMNIZACIONES EXENTO'),
('050', 'AJUSTE EN INDEMNIZACIONES GRAVADO'),
('051', 'AJUSTE EN REEMBOLSO POR FUNERAL EXENTO'),
('052', 'AJUSTE EN CUOTAS DE SEGURIDAD SOCIAL PAGADAS POR EL PATRÓN EXENTO'),
('053', 'AJUSTE EN COMISIONES GRAVADO'),
('054', 'AJUSTE EN VALES DE DESPENSA EXENTO'),
('055', 'AJUSTE EN VALES DE RESTAURANTE EXENTO'),
('056', 'AJUSTE EN VALES DE GASOLINA EXENTO'),
('057', 'AJUSTE EN VALES DE ROPA EXENTO'),
('058', 'AJUSTE EN AYUDA PARA RENTA EXENTO'),
('059', 'AJUSTE EN AYUDA PARA ARTÍCULOS ESCOLARES EXENTO'),
('060', 'AJUSTE EN AYUDA PARA ANTEOJOS EXENTO'),
('061', 'AJUSTE EN AYUDA PARA TRANSPORTE EXENTO'),
('062', 'AJUSTE EN AYUDA PARA GASTOS DE FUNERAL EXENTO'),
('063', 'AJUSTE EN OTROS INGRESOS POR SALARIOS EXENTO'),
('064', 'AJUSTE EN OTROS INGRESOS POR SALARIOS GRAVADO'),
('065', 'AJUSTE EN JUBILACIONES, PENSIONES O HABERES DE RETIRO EN UNA SOLA EXHIBICIÓN EXENTO '),
('066', 'AJUSTE EN JUBILACIONES, PENSIONES O HABERES DE RETIRO EN UNA SOLA EXHIBICIÓN GRAVADO'),
('067', 'AJUSTE EN PAGOS POR SEPARACIÓN ACUMULABLE'),
('068', 'AJUSTE EN PAGOS POR SEPARACIÓN NO ACUMULABLE'),
('069', 'AJUSTE EN JUBILACIONES, PENSIONES O HABERES DE RETIRO EN PARCIALIDADES EXENTO'),
('070', 'AJUSTE EN JUBILACIONES, PENSIONES O HABERES DE RETIRO EN PARCIALIDADES GRAVADO'),
('071', 'AJUSTE EN SUBSIDIO PARA EL EMPLEO (EFECTIVAMENTE ENTREGADO AL TRABAJADOR)'),
('072', 'AJUSTE EN INGRESOS EN ACCIONES O TÍTULOS VALOR QUE REPRESENTAN BIENES EXENTO'),
('073', 'AJUSTE EN INGRESOS EN ACCIONES O TÍTULOS VALOR QUE REPRESENTAN BIENES GRAVADO'),
('074', 'AJUSTE EN ALIMENTACIÓN EXENTO'),
('075', 'AJUSTE EN ALIMENTACIÓN GRAVADO'),
('076', 'AJUSTE EN HABITACIÓN EXENTO'),
('077', 'AJUSTE EN HABITACIÓN GRAVADO'),
('078', 'AJUSTE EN PREMIOS POR ASISTENCIA'),
('079', 'AJUSTE EN PAGOS DISTINTOS A LOS LISTADOS Y QUE NO DEBEN CONSIDERARSE COMO INGRESO POR SUeldos, salarios O INGRESOS ASIMILADOS.'),
('080', 'AJUSTE EN VIÁTICOS GRAVADOS'),
('081', 'AJUSTE EN VIÁTICOS (ENTREGADOS AL TRABAJADOR)'),
('082', 'AJUSTE EN FONDO DE AHORRO GRAVADO'),
('083', 'AJUSTE EN CAJA DE AHORRO GRAVADO'),
('084', 'AJUSTE EN PRIMA DE SEGURO DE VIDA GRAVADO'),
('085', 'AJUSTE EN SEGURO DE GASTOS MÉDICOS MAYORES GRAVADO'),
('086', 'AJUSTE EN SUBSIDIOS POR INCAPACIDAD GRAVADO'),
('087', 'AJUSTE EN BECAS PARA TRABAJADORES Y/O HIJOS GRAVADO'),
('088', 'AJUSTE EN SEGURO DE RETIRO GRAVADO'),
('089', 'AJUSTE EN VALES DE DESPENSA GRAVADO'),
('090', 'AJUSTE EN VALES DE RESTAURANTE GRAVADO'),
('091', 'AJUSTE EN VALES DE GASOLINA GRAVADO'),
('092', 'AJUSTE EN VALES DE ROPA GRAVADO'),
('093', 'AJUSTE EN AYUDA PARA RENTA GRAVADO'),
('094', 'AJUSTE EN AYUDA PARA ARTÍCULOS ESCOLARES GRAVADO'),
('095', 'AJUSTE EN AYUDA PARA ANTEOJOS GRAVADO'),
('096', 'AJUSTE EN AYUDA PARA TRANSPORTE GRAVADO'),
('097', 'AJUSTE EN AYUDA PARA GASTOS DE FUNERAL GRAVADO'),
('098', 'AJUSTE A INGRESOS ASIMILADOS A SALARIOS GRAVADOS'),
('099', 'AJUSTE A INGRESOS POR SUELDOS Y SALARIOS GRAVADOS'),
('100', 'AJUSTE EN VIÁTICOS EXENTOS'),
('101', 'ISR RETENIDO DE EJERCICIO ANTERIOR'),
('102', 'AJUSTE A PAGOS POR GRATIFICACIONES, PRIMAS, COMPENSACIONES, RECOMPENSAS U OTROS A EXTRABAJADORES DERIVADOS DE JUBILACIÓN EN PARCIALIDADES, GRAVADOS'),
('103', 'AJUSTE A PAGOS QUE SE REALICEN A EXTRABAJADORES QUE OBTENGAN UNA JUBILACIÓN EN PARCIALIDADES DERIVADOS DE LA EJECUCIÓN DE UNA RESOLUCIÓN JUDICIAL O DE UN LAUDO GRAVADOS'),
('104', 'AJUSTE A PAGOS QUE SE REALICEN A EXTRABAJADORES QUE OBTENGAN UNA JUBILACIÓN EN PARCIALIDADES DERIVADOS DE LA EJECUCIÓN DE UNA RESOLUCIÓN JUDICIAL O DE UN LAUDO EXENTOS'),
('105', 'AJUSTE A PAGOS QUE SE REALICEN A EXTRABAJADORES QUE OBTENGAN UNA JUBILACIÓN EN UNA SOLA EXHIBICIÓN DERIVADOS DE LA EJECUCIÓN DE UNA RESOLUCIÓN JUDICIAL O DE UN LAUDO GRAVADOS'),
('106', 'AJUSTE A PAGOS QUE SE REALICEN A EXTRABAJADORES QUE OBTENGAN UNA JUBILACIÓN EN UNA SOLA EXHIBICIÓN DERIVADOS DE LA EJECUCIÓN DE UNA RESOLUCIÓN JUDICIAL O DE UN LAUDO EXENTOS'),
('107', 'AJUSTE AL SUBSIDIO CAUSADO');

-- Tipo de banco
INSERT INTO banco (clave, descripcion) VALUES
('002', 'BANAMEX'),
('006', 'BANCOMEXT'),
('009', 'BANOBRAS'),
('012', 'BBVA BANCOMER'),
('014', 'SANTANDER'),
('019', 'BANJERCITO'),
('021', 'HSBC'),
('030', 'BAJIO'),
('032', 'IXE'),
('036', 'INBURSA'),
('037', 'INTERACCIONES'),
('042', 'MIFEL'),
('044', 'SCOTIABANK'),
('058', 'BANREGIO'),
('059', 'INVEX'),
('060', 'BANSI'),
('062', 'AFIRME'),
('072', 'BANORTE'),
('102', 'THE ROYAL BANK'),
('103', 'AMERICAN EXPRESS'),
('106', 'BAMSA'),
('108', 'TOKYO'),
('110', 'JP MORGAN'),
('112', 'BMONEX'),
('113', 'VE POR MAS'),
('116', 'ING'),
('124', 'DEUTSCHE'),
('126', 'CREDIT SUISSE'),
('127', 'AZTECA'),
('128', 'AUTOFIN'),
('129', 'BARCLAYS'),
('130', 'COMPARTAMOS'),
('131', 'BANCO FAMSA'),
('132', 'BMULTIVA'),
('133', 'ACTINVER'),
('134', 'WAL-MART'),
('135', 'NAFIN'),
('136', 'INTERBANCO'),
('137', 'BANCOPPEL'),
('138', 'ABC CAPITAL'),
('139', 'UBS BANK'),
('140', 'CONSUBANCO'),
('141', 'VOLKSWAGEN'),
('143', 'CIBANCO'),
('145', 'BBASE'),
('166', 'BANSEFI'),
('168', 'HIPOTECARIA FEDERAL'),
('600', 'MONEXCB'),
('601', 'GBM'),
('602', 'MASARI'),
('605', 'VALUE'),
('606', 'ESTRUCTURADORES'),
('607', 'TIBER'),
('608', 'VECTOR'),
('610', 'B&B'),
('614', 'ACCIVAL'),
('615', 'MERRILL LYNCH'),
('616', 'FINAMEX'),
('617', 'VALMEX'),
('618', 'UNICA'),
('619', 'MAPFRE'),
('620', 'PROFUTURO'),
('621', 'CB ACTINVER'),
('622', 'OACTIN'),
('623', 'SKANDIA'),
('626', 'CBDEUTSCHE'),
('627', 'ZURICH'),
('628', 'ZURICHVI'),
('629', 'SU CASITA'),
('630', 'CB INTERCAM'),
('631', 'CI BOLSA'),
('632', 'BULLTICK CB'),
('633', 'STERLING'),
('634', 'FINCOMUN'),
('636', 'HDI SEGUROS'),
('637', 'ORDER'),
('638', 'AKALA'),
('640', 'CB JPMORGAN'),
('642', 'REFORMA'),
('646', 'STP'),
('647', 'TELECOMM'),
('648', 'EVERCORE'),
('649', 'SKANDIA'),
('651', 'SEGMTY'),
('652', 'ASEA'),
('653', 'KUSPIT'),
('655', 'SOFIEXPRESS'),
('656', 'UNAGRA'),
('659', 'OPCIONES EMPRESARIALES DEL NOROESTE'),
('901', 'CLS'),
('902', 'INDEVAL'),
('670', 'LIBERTAD');


-- Tabla principal para la creación de recibos de nómina
CREATE TABLE recibos_nomina (
    -- Encabezado
    id SERIAL PRIMARY KEY,  -- Identificador único para cada recibo
    nombre_empresa VARCHAR(50) DEFAULT 'FARMACIAS DE DIOS' NOT NULL,  -- Nombre de la empresa

    -- Primera sección
    uso_destino_cfdi_clave VARCHAR(4) NOT NULL REFERENCES uso_destino_cfdi(clave),  -- Clave del uso o destino CFDI
    lugar_expedicion VARCHAR(20) DEFAULT 'CIUDAD DE MÉXICO' NOT NULL,  -- Lugar de expedición
    fecha_expedicion TIMESTAMP NOT NULL,  -- Fecha de expedición
    rfc_emisor VARCHAR(20) DEFAULT 'FARA2402035H8' NOT NULL,  -- RFC del emisor
    tipo_comprobante_clave VARCHAR(1) NOT NULL REFERENCES tipo_comprobante(clave),  -- Clave del tipo de comprobante
    regimen_laboral_clave VARCHAR(3) NOT NULL REFERENCES regimen_laboral(clave),  -- Clave del régimen laboral

    -- Segunda sección
    empleado VARCHAR(10) NOT NULL REFERENCES empleados(numero_empleado), -- Numero de empleado

    -- Tercera sección
    fecha_pago TIMESTAMP NOT NULL,  -- Fecha de pago
    metodo_pago_clave VARCHAR(3) NOT NULL REFERENCES metodos_pago(clave),  -- Clave del método de pago
    forma_pago_clave VARCHAR(2) NOT NULL REFERENCES formas_pago(clave),  -- Clave de la forma de pago
    banco_clave VARCHAR(2) REFERENCES banco(clave),  -- Clave del banco

    -- Cuarta sección
    percepciones_recibo VARCHAR(3) NOT NULL REFERENCES percepciones(clave),  -- Percepciones
    valor_percepciones DECIMAL(10, 2) NOT NULL,  -- Valor de percepciones
    total_percepciones DECIMAL(10, 2) NOT NULL, -- Total de percepciones

    deducciones_recibo VARCHAR(3) NOT NULL REFERENCES deducciones(clave),  -- Deducciones
    valor_deducciones DECIMAL(10, 2) NOT NULL,  -- Valor de deducciones
    total_deducciones DECIMAL(10, 2) NOT NULL, -- Total de deducciones

    -- Quinta sección
    importe DECIMAL(10, 2) NOT NULL,  -- Importe total (Percepciones - Deducciones)
    importe_con_letra VARCHAR(255) NOT NULL,  -- Importe con letra
    moneda VARCHAR(20) DEFAULT 'MXN PESOS MEXICANOS' NOT NULL,  -- Moneda
    tipo_cambio DECIMAL(10, 2) DEFAULT 0.00 NOT NULL,  -- Tipo de cambio

    -- Sexta seccion
    sello_digital_cfdi TEXT NOT NULL,  -- Sello digital CFDI
    sello_digital_sat TEXT NOT NULL,  -- Sello digital SAT
    cadena_original_complemento_certificacion TEXT NOT NULL,  -- Cadena original complemento certificación
    codigo_qr BYTEA NOT NULL  -- Código QR
);


-- Tabla para almacenar los PDF de las recibos de nomina
CREATE TABLE recibos_pdf (
    id SERIAL PRIMARY KEY,  -- Identificador único para cada factura PDF
    id_recibo INTEGER NOT NULL REFERENCES recibos_nomina(id),  -- ID de la factura asociada
    pdf BYTEA NOT NULL  -- PDF de la factura
);
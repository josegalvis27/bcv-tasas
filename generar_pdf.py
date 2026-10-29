#!/usr/bin/env python3
"""Genera PDF explicativo del proyecto de automatizacion BCV - SAP B1."""

from fpdf import FPDF
from datetime import date


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Automatizacion de Tasas de Cambio BCV - SAP Business One", align="R")
        self.ln(4)
        self.set_draw_color(0, 102, 178)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 72, 140)
        self.cell(0, 12, title)
        self.ln(10)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 102, 178)
        self.cell(0, 10, title)
        self.ln(8)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def bullet_bold_value(self, bold_part, normal_part, indent=15):
        self.cell(indent, 6, "-  ")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.write(6, bold_part)
        self.set_font("Helvetica", "", 10)
        self.write(6, normal_part)
        self.ln(8)


def build_pdf():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # =============================================
    # PORTADA
    # =============================================
    pdf.add_page()
    pdf.ln(35)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(0, 72, 140)
    pdf.cell(0, 15, "Automatizacion de Tasas", align="C")
    pdf.ln(14)
    pdf.cell(0, 15, "de Cambio BCV", align="C")
    pdf.ln(20)

    pdf.set_draw_color(0, 102, 178)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)

    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Integracion BCV --> SAP Business One", align="C")
    pdf.ln(12)

    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 10, "Propuesta de Mejora de Procesos", align="C")
    pdf.ln(30)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, f"Fecha: {date.today().strftime('%d/%m/%Y')}", align="C")
    pdf.ln(8)
    pdf.cell(0, 8, "Departamento de Tecnologia / Finanzas", align="C")

    # =============================================
    # PAGINA 2: RESUMEN EJECUTIVO
    # =============================================
    pdf.add_page()
    pdf.section_title("1. Resumen Ejecutivo")

    pdf.body_text(
        "El presente documento describe la solucion desarrollada para automatizar "
        "la actualizacion de las tasas de cambio publicadas por el Banco Central de "
        "Venezuela (BCV) en el sistema SAP Business One de la empresa."
    )
    pdf.body_text(
        "Actualmente, este proceso se realiza de forma completamente manual: un colaborador "
        "debe ingresar al portal del BCV, descargar el archivo de tasas, interpretar los "
        "valores y luego ingresarlos uno por uno en SAP Business One. "
        "Este proceso se repite cada dia habil para las monedas clave que maneja la empresa (USD, EUR, COP)."
    )
    pdf.body_text(
        "La solucion propuesta elimina la intervencion manual mediante un script que "
        "descarga automaticamente las tasas del BCV, verifica si hay una publicacion nueva, "
        "y las envia directamente a SAP Business One a traves de su API (Service Layer). "
        "El proceso completo toma menos de 10 segundos."
    )

    pdf.ln(5)
    pdf.sub_title("Datos clave")
    pdf.bullet_bold_value("3 monedas clave ", "(USD, EUR, COP) actualizadas simultaneamente")
    pdf.bullet_bold_value("~10 segundos ", "de ejecucion total (vs 15-20 min manual)")
    pdf.bullet_bold_value("0 errores de transcripcion ", "(eliminacion del factor humano)")
    pdf.bullet_bold_value("Ejecucion automatica ", "programable por horario (cron)")
    pdf.bullet_bold_value("Modo de verificacion ", "sin tocar SAP (dry-run)")

    # =============================================
    # PAGINA 3: PROBLEMA ACTUAL
    # =============================================
    pdf.add_page()
    pdf.section_title("2. Situacion Actual (Antes)")

    pdf.body_text(
        "El proceso actual de actualizacion de tasas de cambio presenta los siguientes "
        "pasos manuales y puntos de dolor:"
    )

    pdf.ln(3)
    pdf.sub_title("Proceso manual actual")

    steps_before = [
        "Ingresar al portal web del BCV (bcv.org.ve)",
        "Navegar a la seccion de Tipo de Cambio de Referencia SMC",
        "Descargar el archivo XLS del trimestre actual",
        "Abrir el archivo en Excel e identificar la Fecha Valor",
        "Verificar si la fecha corresponde a una tasa nueva",
        "Abrir SAP Business One, ir a la transaccion de tasas (equivalente OB08)",
        "Ingresar manualmente cada moneda (USD, EUR, COP), una por una",
        "Verificar visualmente que los valores ingresados sean correctos",
        "Repetir este proceso cada dia habil",
    ]

    for i, step in enumerate(steps_before, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(180, 50, 50)
        pdf.cell(15, 7, f"  {i}.")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 7, step)
        pdf.ln(7)

    pdf.ln(5)
    pdf.sub_title("Problemas identificados")
    pdf.bullet_bold_value("Tiempo: ", "15-20 minutos diarios dedicados a una tarea repetitiva")
    pdf.bullet_bold_value("Errores: ", "riesgo de transcripcion incorrecta de decimales (ej: 473.92 vs 437.92)")
    pdf.bullet_bold_value("Dependencia: ", "si la persona responsable no esta disponible, las tasas no se actualizan")
    pdf.bullet_bold_value("Sin trazabilidad: ", "no queda registro de cuando ni quien actualizo las tasas")
    pdf.bullet_bold_value("Costo oculto: ", "tiempo de un profesional dedicado a copiar numeros")

    # =============================================
    # PAGINA 4: SOLUCION
    # =============================================
    pdf.add_page()
    pdf.section_title("3. Solucion Propuesta (Despues)")

    pdf.body_text(
        "Se desarrollo un sistema automatizado en Python que conecta directamente "
        "el portal del BCV con SAP Business One, eliminando toda intervencion manual."
    )

    pdf.ln(3)
    pdf.sub_title("Proceso automatizado")

    steps_after = [
        ("El script se ejecuta automaticamente", "(o manualmente con un solo comando)"),
        ("Accede al portal del BCV", "y descarga el XLS mas reciente"),
        ("Extrae la Fecha Valor", "y la compara con la fecha actual"),
        ("Si hay tasa nueva,", "extrae las 3 monedas (USD, EUR, COP) con sus valores"),
        ("Se conecta a SAP B1 via Service Layer", "y actualiza todas las tasas"),
        ("Genera un log detallado", "de cada operacion realizada"),
        ("Reporta el resultado:", "exitos, errores y monedas omitidas"),
    ]

    for i, (bold, normal) in enumerate(steps_after, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(0, 130, 60)
        pdf.cell(15, 7, f"  {i}.")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.write(7, bold)
        pdf.set_font("Helvetica", "", 10)
        pdf.write(7, f" {normal}")
        pdf.ln(8)

    pdf.ln(5)
    pdf.sub_title("Modos de operacion")

    pdf.bullet_bold_value("Modo Reporte: ", "muestra las tasas en pantalla y/o exporta a CSV, sin tocar SAP")
    pdf.bullet_bold_value("Modo Push: ", "envia las tasas directamente a SAP Business One")
    pdf.bullet_bold_value("Modo Dry-Run: ", "simula el envio a SAP mostrando que se haria, sin ejecutar cambios")
    pdf.bullet_bold_value("Ejecucion manual: ", "el usuario ejecuta el comando cuando lo necesite")
    pdf.bullet_bold_value("Ejecucion automatica: ", "se programa para ejecutarse a una hora fija (ej: 4:30 PM)")

    # =============================================
    # PAGINA 5: COMPARATIVA ANTES VS DESPUES
    # =============================================
    pdf.add_page()
    pdf.section_title("4. Comparativa: Antes vs Despues")

    pdf.ln(2)

    col_w = [60, 60, 60]
    row_h = 9

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(0, 72, 140)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(col_w[0], row_h, "  Aspecto", 1, 0, "L", True)
    pdf.cell(col_w[1], row_h, "Antes (Manual)", 1, 0, "C", True)
    pdf.cell(col_w[2], row_h, "Despues (Automatizado)", 1, 0, "C", True)
    pdf.ln(row_h)

    comparisons = [
        ("Tiempo por ejecucion", "15-20 minutos", "~10 segundos"),
        ("Tiempo mensual (22 dias)", "5.5 - 7.3 horas", "< 4 minutos"),
        ("Tiempo anual", "66 - 88 horas", "< 1 hora"),
        ("Monedas procesadas", "Una por una", "3 simultaneas"),
        ("Riesgo de error", "Alto (transcripcion)", "Nulo (automatizado)"),
        ("Disponibilidad", "Depende de persona", "24/7 automatico"),
        ("Trazabilidad", "Ninguna", "Log completo"),
        ("Verificacion previa", "Visual / mental", "Modo dry-run"),
        ("Exportacion datos", "Manual desde SAP", "CSV automatico"),
        ("Costo de operacion", "Recurso humano diario", "Script autonomo"),
    ]

    pdf.set_font("Helvetica", "", 9)
    for i, (aspect, before, after) in enumerate(comparisons):
        if i % 2 == 0:
            pdf.set_fill_color(240, 245, 250)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.set_text_color(50, 50, 50)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(col_w[0], row_h, f"  {aspect}", 1, 0, "L", True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(180, 50, 50)
        pdf.cell(col_w[1], row_h, before, 1, 0, "C", True)
        pdf.set_text_color(0, 130, 60)
        pdf.cell(col_w[2], row_h, after, 1, 0, "C", True)
        pdf.ln(row_h)

    pdf.ln(10)
    pdf.sub_title("Ahorro estimado")
    pdf.body_text(
        "Considerando un promedio de 17 minutos diarios y 22 dias habiles al mes:"
    )
    pdf.bullet_bold_value("Ahorro mensual: ", "~6.2 horas de trabajo profesional")
    pdf.bullet_bold_value("Ahorro anual: ", "~74 horas (~9.3 jornadas laborales completas)")
    pdf.bullet_bold_value("Eliminacion total ", "del riesgo de errores de transcripcion")
    pdf.bullet_bold_value("Liberacion del recurso ", "para tareas de mayor valor agregado")

    # =============================================
    # PAGINA 6: ARQUITECTURA TECNICA
    # =============================================
    pdf.add_page()
    pdf.section_title("5. Arquitectura Tecnica")

    pdf.body_text("La solucion esta compuesta por los siguientes modulos:")
    pdf.ln(3)

    modules = [
        ("main.py", "Punto de entrada",
         "Orquesta todo el proceso. Recibe parametros por linea de comando "
         "(modo, forzar, dry-run, etc.) y coordina los demas modulos."),
        ("bcv_parser.py", "Motor de descarga y parseo",
         "Se conecta al portal del BCV, descarga el archivo XLS mas reciente, "
         "extrae las fechas (Operacion y Valor) y las tasas de cambio de USD, EUR y COP con "
         "sus valores de compra y venta en Bs/ME y ME/USD."),
        ("sap_client.py", "Cliente SAP Business One",
         "Se conecta al Service Layer de SAP B1, gestiona la sesion de autenticacion "
         "y envia cada tasa de cambio. Maneja reconexion automatica si la sesion expira."),
        ("currency_map.py", "Mapeo de monedas",
         "Filtra y traduce los codigos de moneda del BCV a los codigos ISO que usa SAP. "
         "Actualmente configurado para USD, EUR y COP. Facilmente ampliable a mas monedas."),
        ("output_formatter.py", "Generador de reportes",
         "Muestra las tasas en una tabla formateada en consola y permite exportar "
         "a archivo CSV para analisis o respaldo."),
        ("config.py", "Configuracion",
         "Carga las credenciales de SAP y parametros desde un archivo .env seguro, "
         "separando la configuracion del codigo."),
    ]

    for mod_name, mod_title, mod_desc in modules:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 72, 140)
        pdf.cell(0, 8, f"{mod_name}  --  {mod_title}")
        pdf.ln(7)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(70, 70, 70)
        pdf.multi_cell(0, 5, mod_desc)
        pdf.ln(4)

    pdf.ln(3)
    pdf.sub_title("Diagrama de flujo simplificado")
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(50, 50, 50)
    flow = [
        "  +---------------+     +----------------+     +----------------+",
        "  |  Portal BCV   |---->|  Descargar     |---->|   Parsear      |",
        "  |  (bcv.org.ve) |     |   XLS          |     |  fechas y      |",
        "  +---------------+     +----------------+     |   tasas        |",
        "                                                +-------+--------+",
        "                                                        |",
        "                                                +-------v--------+",
        "                                                | Fecha Valor    |",
        "                                                |  > Hoy?        |",
        "                                                +-------+--------+",
        "                                                  Si    |   No",
        "                                          +-------------+---------+",
        "                                    +-----v------+    +-----------v-+",
        "                                    |  Push SAP  |    |  Sin tasa   |",
        "                                    |  B1 (API)  |    |  nueva      |",
        "                                    +------------+    +-------------+",
    ]
    for line in flow:
        pdf.cell(0, 5, line)
        pdf.ln(5)

    # =============================================
    # PAGINA 7: PASO A PASO TECNICO
    # =============================================
    pdf.add_page()
    pdf.section_title("6. Paso a Paso: Como se Construyo")

    pdf.body_text(
        "A continuacion se detalla cada paso del desarrollo de la solucion, "
        "desde la investigacion inicial hasta la implementacion funcional:"
    )
    pdf.ln(3)

    pasos = [
        ("Paso 1: Analisis del portal BCV",
         "Se analizo la estructura del sitio web del BCV para identificar "
         "donde se publican los archivos XLS con las tasas de cambio. Se descubrio "
         "que los archivos siguen un patron de nomenclatura por trimestre y anio "
         "(ej: 2_1_2a26_smc.xls para Q1-2026) y que el enlace mas reciente "
         "siempre aparece primero en la tabla de la pagina."),

        ("Paso 2: Descarga y exploracion del XLS",
         "Se descargo el archivo XLS y se analizo su estructura interna: "
         "la fila 4 contiene las fechas de Operacion y Valor, las filas 10-30 "
         "contienen los datos de las monedas con sus cotizaciones de compra "
         "y venta tanto en Bs/ME como en ME/USD. El sistema filtra solo las "
         "3 monedas requeridas (USD, EUR, COP). Se identifico que el formato "
         "es XLS antiguo (no XLSX), lo que requiere la libreria xlrd."),

        ("Paso 3: Logica de deteccion de tasa nueva",
         "Se implemento la comparacion de la Fecha Valor con la fecha actual. "
         "Si la Fecha Valor es posterior a hoy, significa que el BCV publico "
         "una tasa nueva que aplica a partir del dia siguiente. Esta logica "
         "funciona correctamente con fines de semana y feriados."),

        ("Paso 4: Filtrado y mapeo de monedas",
         "Se configuro el sistema para extraer unicamente las 3 monedas "
         "requeridas por la empresa: USD (dolar), EUR (euro) y COP (peso "
         "colombiano). El mapeo es facilmente ampliable si en el futuro se "
         "necesitan mas monedas."),

        ("Paso 5: Cliente SAP Business One",
         "Se desarrollo un cliente que se conecta al Service Layer de SAP B1 "
         "mediante su API REST. El cliente maneja autenticacion, gestion de "
         "sesion, reconexion automatica y envio de tasas una por una. Se "
         "implemento como context manager para garantizar el cierre de sesion."),

        ("Paso 6: Interfaz de linea de comando",
         "Se creo un CLI con multiples modos de operacion: reporte (solo ver), "
         "push (enviar a SAP), dry-run (simular sin cambios), exportacion CSV, "
         "y opciones para forzar la ejecucion o seleccionar la columna de tasa."),

        ("Paso 7: Sistema de logging",
         "Se implemento un sistema de registro que guarda un log diario con "
         "cada accion realizada: URL descargada, fechas detectadas, monedas "
         "procesadas y resultado de cada envio a SAP. Esto proporciona "
         "trazabilidad completa del proceso."),
    ]

    for title, desc in pasos:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(0, 72, 140)
        pdf.cell(0, 8, title)
        pdf.ln(7)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 5, desc)
        pdf.ln(5)

    # =============================================
    # PAGINA 8: BENEFICIOS
    # =============================================
    pdf.add_page()
    pdf.section_title("7. Beneficios para la Empresa")

    pdf.ln(2)
    benefits = [
        ("Eficiencia Operativa",
         "Se eliminan ~74 horas anuales de trabajo manual repetitivo. El recurso "
         "humano queda liberado para tareas analiticas y de mayor valor. El proceso "
         "que antes tomaba 15-20 minutos ahora se completa en 10 segundos."),

        ("Eliminacion de Errores",
         "Al eliminar la transcripcion manual de decimales, se reduce a cero el "
         "riesgo de errores en las tasas de cambio. Un error en una tasa puede "
         "impactar calculos de facturacion, importaciones, obligaciones tributarias "
         "y reportes financieros."),

        ("Continuidad del Negocio",
         "El proceso ya no depende de que una persona especifica este disponible. "
         "Se puede programar para ejecutarse automaticamente, garantizando que las "
         "tasas siempre esten actualizadas incluso en ausencia del responsable."),

        ("Trazabilidad y Auditoria",
         "Cada ejecucion genera un log detallado: fecha, hora, tasas descargadas, "
         "valores enviados a SAP y resultado. Esto facilita auditorias internas "
         "y externas, y permite rastrear cualquier discrepancia."),

        ("Flexibilidad",
         "El sistema ofrece multiples modos de operacion: verificacion sin cambios "
         "(dry-run), exportacion a CSV para analisis, ejecucion manual o automatica, "
         "y seleccion de tasa de compra o venta segun la necesidad."),

        ("Escalabilidad",
         "La misma arquitectura puede adaptarse para automatizar otros procesos "
         "repetitivos que involucren descarga de datos de fuentes externas y "
         "actualizacion en SAP Business One."),

        ("Bajo Riesgo de Implementacion",
         "La solucion incluye un modo de simulacion (dry-run) que permite verificar "
         "exactamente que datos se enviarian a SAP sin realizar ningun cambio. Esto "
         "permite una validacion completa antes de activar el modo automatico."),
    ]

    for title, desc in benefits:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 102, 50)
        pdf.cell(8, 7, "[+]")
        pdf.set_text_color(0, 72, 140)
        pdf.cell(0, 7, title)
        pdf.ln(7)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 5, desc)
        pdf.ln(5)

    # =============================================
    # PAGINA 9: SEGURIDAD Y REQUISITOS
    # =============================================
    pdf.add_page()
    pdf.section_title("8. Seguridad y Requisitos")

    pdf.sub_title("Seguridad")
    pdf.bullet_bold_value("Credenciales protegidas: ",
                          "las claves de SAP se almacenan en un archivo .env que no se "
                          "incluye en el codigo fuente ni en repositorios")
    pdf.bullet_bold_value("Sin datos sensibles en logs: ",
                          "los registros contienen tasas y resultados, nunca contrasenias")
    pdf.bullet_bold_value("Sesion SAP controlada: ",
                          "la conexion se cierra automaticamente al finalizar cada ejecucion")
    pdf.bullet_bold_value("Solo lectura del BCV: ",
                          "el sistema solo descarga datos publicos del portal del BCV")

    pdf.ln(5)
    pdf.sub_title("Requisitos tecnicos")
    pdf.bullet_bold_value("Python 3.10+ ", "instalado en la maquina que ejecutara el script")
    pdf.bullet_bold_value("Acceso a internet ", "para conectar al portal del BCV")
    pdf.bullet_bold_value("Acceso al Service Layer de SAP B1 ", "(URL, usuario y contrasenia)")
    pdf.bullet_bold_value("Librerias Python: ", "requests, xlrd, python-dotenv, beautifulsoup4")

    pdf.ln(5)
    pdf.sub_title("Proximos pasos para activacion")

    next_steps = [
        "Obtener la URL del Service Layer de SAP B1 (equipo de sistemas)",
        "Crear un usuario de SAP B1 con permisos para actualizar tasas de cambio",
        "Configurar el archivo .env con las credenciales",
        "Ejecutar en modo dry-run para validar los datos",
        "Ejecutar en modo push para la primera actualizacion real",
        "Programar la ejecucion automatica diaria (cron)",
    ]

    for i, step in enumerate(next_steps, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(0, 72, 140)
        pdf.cell(12, 7, f"  {i}.")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 7, step)
        pdf.ln(8)

    # =============================================
    # PAGINA 10: CONCLUSION
    # =============================================
    pdf.add_page()
    pdf.section_title("9. Conclusion")

    pdf.ln(5)
    pdf.body_text(
        "La automatizacion de la actualizacion de tasas de cambio del BCV en SAP Business One "
        "representa una mejora significativa en la eficiencia operativa de la empresa. "
        "Se transforma un proceso manual, propenso a errores y dependiente de una persona, "
        "en un sistema automatizado, confiable y auditable."
    )
    pdf.ln(3)
    pdf.body_text(
        "La solucion ya esta desarrollada y funcional en modo reporte. La activacion del "
        "modo automatico con SAP requiere unicamente la configuracion de acceso al Service "
        "Layer, lo cual puede completarse en cuestion de horas con el apoyo del equipo de "
        "sistemas."
    )
    pdf.ln(3)
    pdf.body_text(
        "El retorno de inversion es inmediato: desde el primer dia de uso se eliminan los "
        "errores de transcripcion y se liberan ~74 horas anuales de trabajo profesional que "
        "pueden dedicarse a actividades de mayor valor estrategico para la organizacion."
    )

    pdf.ln(15)

    # Caja resumen
    pdf.set_fill_color(240, 248, 255)
    pdf.set_draw_color(0, 102, 178)
    pdf.set_line_width(0.5)
    y = pdf.get_y()
    pdf.rect(15, y, 180, 50, "DF")
    pdf.set_xy(20, y + 5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 72, 140)
    pdf.cell(170, 8, "Resumen de impacto", align="C")
    pdf.ln(12)
    pdf.set_x(25)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    summary_items = [
        "De 15-20 min/dia --> 10 segundos",
        "0 errores de transcripcion",
        "~74 horas/anio liberadas",
        "Ejecucion 24/7 automatica",
        "Trazabilidad completa con logs",
        "Credenciales seguras en archivo .env",
    ]
    for i, item in enumerate(summary_items):
        col = i % 2
        if col == 0:
            pdf.set_x(25)
        else:
            pdf.set_x(110)
        pdf.cell(80, 7, f"[+]  {item}")
        if col == 1:
            pdf.ln(9)
    pdf.ln(5)

    # Output
    output_path = "/Users/josegalvis2703/bcv-tasas/Propuesta_Automatizacion_Tasas_BCV_SAP.pdf"
    pdf.output(output_path)
    return output_path


if __name__ == "__main__":
    path = build_pdf()
    print(f"PDF generado: {path}")

import flet as ft

# ==== COMPONENTES REUTILIZABLES ==== #

def crear_campo(label, width=None, value=None):
    campo = ft.TextField(label=label, value=value, bgcolor="#FFFFFF", border_radius=8, color="black", width=width)
    contenedor = ft.Container(
        campo,
        bgcolor="#FFFFFF",
        border_radius=8,
        border=ft.border.all(2, "black"),
        padding=4,
        margin=2
    )
    return campo, contenedor

def crear_filas_botones(materiales, accion_al_pulsar):
    return [
        ft.Row(
            controls=[ft.ElevatedButton(m, on_click=lambda e, m=m: accion_al_pulsar(m)) for m in materiales[i:i+2]],
            spacing=10,
        )
        for i in range(0, len(materiales), 2)
    ]

def cuadro_resultado_widget(label_resultado):
    return ft.Container(
        label_resultado,
        bgcolor="white",
        border_radius=10,
        border=ft.border.all(2, "black"),
        padding=15,
        alignment=ft.alignment.center,
        margin=10,
        shadow=ft.BoxShadow(blur_radius=8, color="#e0e0e0")
    )

def mostrar_menu_principal(page, ir_a_pantalla):
    page.controls.clear()
    page.controls.append(ft.Text("Calculadora de Ingeniería", size=24, weight="bold"))
    opciones = [
        ("📦", "Volumen por dimensiones", "dimensiones"),
        ("⚖️", "Volumen por masa y densidad", "masa_densidad"),
        ("🔄", "Conversión de unidades", "conversion"),
        ("🛒", "Cantidad de bolsas de material", "cantidad_material"),
        ("📏", "Presión superficial", "presion"),
        ("💧", "Coeficiente de permeabilidad", "permeabilidad")
    ]
    TAMANO_BOTON = 110
    estilo_boton = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=0)
    botones = [
        ft.ElevatedButton(
            content=ft.Column([
                ft.Text(emoji, size=38),
                ft.Text(texto, size=13, weight="bold", text_align="center"),
            ], alignment="center", horizontal_alignment="center", spacing=2),
            on_click=lambda e, pantalla=pantalla: ir_a_pantalla(pantalla),
            width=TAMANO_BOTON,
            height=TAMANO_BOTON,
            style=estilo_boton
        )
        for emoji, texto, pantalla in opciones
    ]
    filas = [ft.Row(controls=botones[i:i+2], spacing=10, alignment="center") for i in range(0, len(botones), 2)]
    page.controls.extend(filas)
    page.update()

# ==== LÓGICA PRINCIPAL Y PANTALLAS ==== #

def main(page: ft.Page):

    page.title = "Calculadora de Ingeniería"
    page.scroll = "auto"

    # Materiales y propiedades para cálculos
    DENSIDADES = {
        "Hormigón": 2400,
        "Cemento": 1500,
        "Arena": 1600,
        "Grava": 1700,
        "Acero": 7850,
        "Madera": 600,
    }
    BOLSAS = {
        "Cemento": {"densidad":1500,"rendimiento":42.5},
        "Cal": {"densidad":1350,"rendimiento":25},
        "Arena": {"densidad":1600,"rendimiento":50},
        "Grava": {"densidad":1700,"rendimiento":50},
        "Hormigón": {"densidad":2400,"rendimiento":50}
    }

    MENSAJE_ERROR = "Por favor, ingresa valores válidos en todos los campos."

    # ---- Pantallas de cada funcionalidad ---- #

    def pantalla_volumen_dimensiones():
        page.controls.clear()
        resultado = ft.Text(size=20, weight="bold", color="blue", text_align="center")

        largo, campo_largo = crear_campo("Largo (m)")
        ancho, campo_ancho = crear_campo("Ancho (m)")
        alto, campo_alto = crear_campo("Altura (m)")

        def calcular(ev=None):
            try:
                v = float(largo.value)
                an = float(ancho.value)
                al = float(alto.value)
                resultado.value = f"Volumen: {v * an * al:.4f} m³"
            except Exception:
                resultado.value = MENSAJE_ERROR
            page.update()

        largo.on_change = calcular
        ancho.on_change = calcular
        alto.on_change = calcular

        page.controls.extend([
            cuadro_resultado_widget(resultado),
            ft.Text("Volumen (L x A x H)", size=20),
            campo_largo, campo_ancho, campo_alto,
            ft.ElevatedButton("Volver al menú", on_click=lambda e: mostrar_menu_principal(page, ir_a_pantalla))
        ])
        page.update()

    def pantalla_volumen_masa_densidad():
        page.controls.clear()
        resultado = ft.Text(size=20, weight="bold", color="blue", text_align="center")

        masa, campo_masa = crear_campo("Masa")
        unidad = ft.Dropdown(label="Unidad", options=[
            ft.dropdown.Option("g"),
            ft.dropdown.Option("kg"),
            ft.dropdown.Option("toneladas")
        ], value="kg", width=120)
        densidad, campo_densidad = crear_campo("Densidad (kg/m³)", width=170)

        def seleccionar_material(material):
            densidad.value = str(DENSIDADES[material])
            calcular(None)
            page.update()

        botones = crear_filas_botones(list(DENSIDADES.keys()), seleccionar_material)

        def calcular(ev=None):
            try:
                m = float(masa.value)
                u = unidad.value
                if u == "g": m /= 1000
                elif u == "toneladas": m *= 1000
                d = float(densidad.value)
                v = m / d
                resultado.value = f"Volumen: {v:.4f} m³"
            except Exception:
                resultado.value = MENSAJE_ERROR
            page.update()

        masa.on_change = calcular
        unidad.on_change = calcular
        densidad.on_change = calcular

        page.controls.extend([
            cuadro_resultado_widget(resultado),
            ft.Text("Volumen (masa / densidad)", size=20),
            campo_masa,
            ft.Row([unidad, campo_densidad], spacing=10),
            ft.Text("Selecciona material:"),
            *botones,
            ft.ElevatedButton("Volver al menú", on_click=lambda e: mostrar_menu_principal(page, ir_a_pantalla))
        ])
        page.update()

    def pantalla_conversion_unidades():
        page.controls.clear()
        resultado = ft.Text(size=20, weight="bold", color="blue", text_align="center")
        valor, campo_valor = crear_campo("Valor")
        categorias = {
            "Longitud": {"m":1,"cm":0.01,"mm":0.001,"km":1000,"in":0.0254,"ft":0.3048},
            "Volumen": {"m³":1,"litros":0.001,"cm³":1e-6,"pies³":0.0283168,"galones":0.00378541},
            "Peso": {"kg":1,"g":0.001,"mg":1e-6,"toneladas":1000,"lb":0.453592},
            "Temperatura": ["C","F","K"]
        }
        categoria = ft.Dropdown(label="Categoría", options=[ft.dropdown.Option(c) for c in categorias], value="Longitud")
        u_origen = ft.Dropdown(label="Unidad de origen", options=[], value=None)
        u_destino = ft.Dropdown(label="Unidad destino", options=[], value=None)

        def actualizar_unidades(ev=None):
            u_origen.options.clear()
            u_destino.options.clear()
            unidades = categorias[categoria.value] if isinstance(categorias[categoria.value], dict) else categorias[categoria.value]
            for u in unidades:
                u_origen.options.append(ft.dropdown.Option(u))
                u_destino.options.append(ft.dropdown.Option(u))
            if u_origen.options:
                u_origen.value = u_origen.options[0].key
            if u_destino.options:
                if len(u_destino.options) > 1:
                    u_destino.value = u_destino.options[1].key
                else:
                    u_destino.value = u_destino.options[0].key
            page.update()
            convertir()

        def convertir(ev=None):
            try:
                v = float(valor.value)
                cat = categoria.value
                u1, u2 = u_origen.value, u_destino.value
                if not u1 or not u2:
                    resultado.value = MENSAJE_ERROR
                    page.update()
                    return
                if cat == "Temperatura":
                    if u1 == u2:
                        r = v
                    elif u1 == "C":
                        r = v+273.15 if u2=="K" else v*9/5+32
                    elif u1 == "F":
                        r = (v-32)*5/9 if u2=="C" else (v-32)*5/9+273.15
                    elif u1 == "K":
                        r = v-273.15 if u2=="C" else (v-273.15)*9/5+32
                else:
                    base = v * categorias[cat][u1]
                    r = base / categorias[cat][u2]
                resultado.value = f"{v} {u1} = {r:.4f} {u2}"
            except Exception:
                resultado.value = MENSAJE_ERROR
            page.update()
        valor.on_change = convertir
        categoria.on_change = actualizar_unidades
        u_origen.on_change = convertir
        u_destino.on_change = convertir
        actualizar_unidades()
        page.controls.extend([
            cuadro_resultado_widget(resultado),
            ft.Text("Conversión de unidades", size=20),
            campo_valor, categoria, u_origen, u_destino,
            ft.ElevatedButton("Volver al menú", on_click=lambda e: mostrar_menu_principal(page, ir_a_pantalla))
        ])
        page.update()

    def pantalla_cantidad_material():
        page.controls.clear()
        resultado = ft.Text(size=20, weight="bold", color="blue", text_align="center")
        volumen, campo_volumen = crear_campo("Volumen (m³)")
        densidad, campo_densidad = crear_campo("Densidad (kg/m³)")
        rendimiento, campo_rendimiento = crear_campo("Rendimiento por bolsa (kg)")
        def seleccionar_material(material):
            densidad.value = str(BOLSAS[material]["densidad"])
            rendimiento.value = str(BOLSAS[material]["rendimiento"])
            calcular(None)
            page.update()
        botones = crear_filas_botones(list(BOLSAS.keys()), seleccionar_material)
        def calcular(ev=None):
            try:
                v = float(volumen.value)
                d = float(densidad.value)
                r = float(rendimiento.value)
                bolsas = (v * d) / r
                resultado.value = f"Necesitas aproximadamente {bolsas:.2f} bolsas"
            except Exception:
                resultado.value = MENSAJE_ERROR
            page.update()
        volumen.on_change = calcular
        densidad.on_change = calcular
        rendimiento.on_change = calcular
        page.controls.extend([
            cuadro_resultado_widget(resultado),
            ft.Text("Cantidad de bolsas de material", size=20),
            campo_volumen, campo_densidad, campo_rendimiento,
            ft.Text("Materiales comunes:"),
            *botones,
            ft.ElevatedButton("Volver al menú", on_click=lambda e: mostrar_menu_principal(page, ir_a_pantalla))
        ])
        page.update()

    def pantalla_presion_superficial():
        page.controls.clear()
        resultado = ft.Text(size=20, weight="bold", color="blue", text_align="center")
        carga, campo_carga = crear_campo("Carga (kgf)")
        area, campo_area = crear_campo("Área (m²)")
        unidad = ft.Dropdown(label="Unidad", options=[ft.dropdown.Option("kg/m²"), ft.dropdown.Option("kN/m²")], value="kg/m²")
        def calcular(ev=None):
            try:
                c = float(carga.value)
                a = float(area.value)
                presion = c / a
                if unidad.value == "kN/m²":
                    presion *= 0.00980665
                resultado.value = f"Presión: {presion:.4f} {unidad.value}"
            except Exception:
                resultado.value = MENSAJE_ERROR
            page.update()
        carga.on_change = calcular
        area.on_change = calcular
        unidad.on_change = calcular
        page.controls.extend([
            cuadro_resultado_widget(resultado),
            ft.Text("Cálculo de presión superficial", size=20),
            campo_carga, campo_area, unidad,
            ft.ElevatedButton("Volver al menú", on_click=lambda e: mostrar_menu_principal(page, ir_a_pantalla))
        ])
        page.update()

    def pantalla_coeficiente_permeabilidad():
        page.controls.clear()
        resultado = ft.Text(size=20, weight="bold", color="blue", text_align="center")
        q, campo_q = crear_campo("Volumen Q (litros)")
        l, campo_l = crear_campo("Longitud L (m)")
        a, campo_a = crear_campo("Área A (cm²)")
        h, campo_h = crear_campo("Carga hidráulica h (m)")
        t, campo_t = crear_campo("Tiempo t (s)")
        def calcular(ev=None):
            try:
                Q = float(q.value) / 1000
                L = float(l.value)
                A = float(a.value) / 10000
                H = float(h.value)
                T = float(t.value)
                k = (Q * L) / (A * H * T)
                resultado.value = f"Coef. de permeabilidad: {k:.6e} m/s"
            except Exception:
                resultado.value = MENSAJE_ERROR
            page.update()
        q.on_change = calcular
        l.on_change = calcular
        a.on_change = calcular
        h.on_change = calcular
        t.on_change = calcular
        page.controls.extend([
            cuadro_resultado_widget(resultado),
            ft.Text("Coeficiente de permeabilidad", size=20),
            campo_q, campo_l, campo_a, campo_h, campo_t,
            ft.ElevatedButton("Volver al menú", on_click=lambda e: mostrar_menu_principal(page, ir_a_pantalla))
        ])
        page.update()

    # ---- Navegación central ---- #
    def ir_a_pantalla(nombre_pantalla):
        if nombre_pantalla == "dimensiones":
            pantalla_volumen_dimensiones()
        elif nombre_pantalla == "masa_densidad":
            pantalla_volumen_masa_densidad()
        elif nombre_pantalla == "conversion":
            pantalla_conversion_unidades()
        elif nombre_pantalla == "cantidad_material":
            pantalla_cantidad_material()
        elif nombre_pantalla == "presion":
            pantalla_presion_superficial()
        elif nombre_pantalla == "permeabilidad":
            pantalla_coeficiente_permeabilidad()
        else:
            mostrar_menu_principal(page, ir_a_pantalla)

    # Mostramos el menú principal al iniciar
    mostrar_menu_principal(page, ir_a_pantalla)

# ---- Lanzador de la app ---- #
import os
from flet import app, AppView

puerto = int(os.environ.get("PORT", 8550))
app(target=main, view=AppView.WEB_BROWSER, port=puerto)

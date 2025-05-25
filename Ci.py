import flet as ft

def campo_resaltado(label, width=None):
    return ft.Container(
        ft.TextField(label=label, bgcolor="#FFFBCC", border_radius=8, width=width, color="black"),
        bgcolor="#FFFBCC",
        border_radius=8,
        padding=4,
        margin=2
    )

def main(page: ft.Page):
    page.title = "Calculadora de Ingeniería"
    page.scroll = "auto"
    resultado = ft.Text(size=20, weight="bold", color="blue", text_align="center")
    contenedor_resultado = ft.Container(
        resultado,
        bgcolor="white",
        border_radius=10,
        padding=15,
        alignment=ft.alignment.center,
        margin=10,
        shadow=ft.BoxShadow(blur_radius=8, color="#e0e0e0")
    )
    materiales = {
        "Hormigón": 2400,
        "Cemento": 1500,
        "Arena": 1600,
        "Grava": 1700,
        "Acero": 7850,
        "Madera": 600,
    }

    def limpiar_controles():
        page.controls.clear()
        resultado.value = ""
        page.update()

    def mostrar_menu(e=None):
        limpiar_controles()
        page.controls.append(ft.Text("Calculadora de Ingeniería", size=24, weight="bold"))
        opciones = [
            ("📦", "Volumen por dimensiones", volumen_dimensiones),
            ("⚖️", "Volumen por masa y densidad", volumen_masa_densidad),
            ("🔄", "Conversión de unidades", conversion_unidades),
            ("🛒", "Cantidad de bolsas de material", cantidad_material),
            ("📏", "Presión superficial", presion_superficial),
            ("💧", "Coeficiente de permeabilidad", coeficiente_permeabilidad)
        ]
        SQUARE_BTN_SIZE = 110
        square_btn_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=0,
        )
        botones = [
            ft.ElevatedButton(
                content=ft.Column([
                    ft.Text(emoji, size=38),
                    ft.Text(texto, size=13, weight="bold", text_align="center"),
                ], alignment="center", horizontal_alignment="center", spacing=2),
                on_click=funcion,
                width=SQUARE_BTN_SIZE,
                height=SQUARE_BTN_SIZE,
                style=square_btn_style
            )
            for emoji, texto, funcion in opciones
        ]
        filas = [
            ft.Row(controls=botones[i:i+2], spacing=10, alignment="center")
            for i in range(0, len(botones), 2)
        ]
        page.controls.extend(filas)
        page.update()

    def volumen_dimensiones(e):
        limpiar_controles()
        l = campo_resaltado("Largo (m)")
        a = campo_resaltado("Ancho (m)")
        h = campo_resaltado("Altura (m)")

        def calcular(ev=None):
            try:
                v = float(l.content.value)
                an = float(a.content.value)
                al = float(h.content.value)
                resultado.value = f"Volumen: {v * an * al:.4f} m³"
            except Exception:
                resultado.value = ""
            page.update()

        l.content.on_change = calcular
        a.content.on_change = calcular
        h.content.on_change = calcular

        page.controls.extend([
            contenedor_resultado,
            ft.Text("Volumen (L x A x H)", size=20),
            l, a, h,
            ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)
        ])
        page.update()

    def volumen_masa_densidad(e):
        limpiar_controles()
        masa = campo_resaltado("Masa")
        unidad = ft.Dropdown(label="Unidad", options=[
            ft.dropdown.Option("g"),
            ft.dropdown.Option("kg"),
            ft.dropdown.Option("toneladas")
        ], value="kg", width=120)
        densidad = campo_resaltado("Densidad (kg/m³)", width=170)

        def usar_material(d):
            densidad.content.value = str(materiales[d])
            calcular(None)
            page.update()

        botones = [ft.ElevatedButton(mat, on_click=lambda e, m=mat: usar_material(m)) for mat in materiales]
        filas = [
            ft.Row(controls=botones[i:i+2], spacing=10)
            for i in range(0, len(botones), 2)
        ]

        def calcular(ev=None):
            try:
                m = float(masa.content.value)
                u = unidad.value
                if u == "g": m /= 1000
                elif u == "toneladas": m *= 1000
                d = float(densidad.content.value)
                v = m / d
                resultado.value = f"Volumen: {v:.4f} m³"
            except Exception:
                resultado.value = ""
            page.update()

        masa.content.on_change = calcular
        unidad.on_change = calcular
        densidad.content.on_change = calcular

        page.controls.extend([
            contenedor_resultado,
            ft.Text("Volumen (masa / densidad)", size=20),
            masa,
            ft.Row([unidad, densidad], spacing=10),
            ft.Text("Selecciona material:"),
            *filas,
            ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)
        ])
        page.update()

    def conversion_unidades(e):
        limpiar_controles()
        valor = campo_resaltado("Valor")
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
                v = float(valor.content.value)
                cat = categoria.value
                u1, u2 = u_origen.value, u_destino.value
                if not u1 or not u2:
                    resultado.value = ""
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
                resultado.value = ""
            page.update()

        
        valor.content.on_change = convertir
        categoria.on_change = actualizar_unidades
        u_origen.on_change = convertir
        u_destino.on_change = convertir

        
        actualizar_unidades()

        page.controls.extend([
            contenedor_resultado,
            ft.Text("Conversión de unidades", size=20),
            valor, categoria, u_origen, u_destino,
            ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)
        ])
        page.update()

    def cantidad_material(e):
        limpiar_controles()
        volumen = campo_resaltado("Volumen (m³)")
        densidad = campo_resaltado("Densidad (kg/m³)")
        rendimiento = campo_resaltado("Rendimiento por bolsa (kg)")
        materiales_local = {
            "Cemento": {"densidad":1500,"rendimiento":42.5},
            "Cal": {"densidad":1350,"rendimiento":25},
            "Arena": {"densidad":1600,"rendimiento":50},
            "Grava": {"densidad":1700,"rendimiento":50},
            "Hormigón": {"densidad":2400,"rendimiento":50}
        }
        def usar_material(m):
            densidad.content.value = str(materiales_local[m]["densidad"])
            rendimiento.content.value = str(materiales_local[m]["rendimiento"])
            calcular(None)
            page.update()
        botones = [ft.ElevatedButton(mat, on_click=lambda e, m=mat: usar_material(m)) for mat in materiales_local]
        filas = [
            ft.Row(controls=botones[i:i+2], spacing=10)
            for i in range(0, len(botones), 2)
        ]
        def calcular(ev=None):
            try:
                v = float(volumen.content.value)
                d = float(densidad.content.value)
                r = float(rendimiento.content.value)
                bolsas = (v * d) / r
                resultado.value = f"Necesitas aproximadamente {bolsas:.2f} bolsas"
            except Exception:
                resultado.value = ""
            page.update()
        volumen.content.on_change = calcular
        densidad.content.on_change = calcular
        rendimiento.content.on_change = calcular

        page.controls.extend([
            contenedor_resultado,
            ft.Text("Cantidad de bolsas de material", size=20),
            volumen, densidad, rendimiento,
            ft.Text("Materiales comunes:"),
            *filas,
            ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)
        ])
        page.update()

    def presion_superficial(e):
        limpiar_controles()
        carga = campo_resaltado("Carga (kgf)")
        area = campo_resaltado("Área (m²)")
        unidad = ft.Dropdown(label="Unidad", options=[ft.dropdown.Option("kg/m²"), ft.dropdown.Option("kN/m²")], value="kg/m²")

        def calcular(ev=None):
            try:
                c = float(carga.content.value)
                a = float(area.content.value)
                presion = c / a
                if unidad.value == "kN/m²":
                    presion *= 0.00980665
                resultado.value = f"Presión: {presion:.4f} {unidad.value}"
            except Exception:
                resultado.value = ""
            page.update()

        carga.content.on_change = calcular
        area.content.on_change = calcular
        unidad.on_change = calcular

        page.controls.extend([
            contenedor_resultado,
            ft.Text("Cálculo de presión superficial", size=20),
            carga, area, unidad,
            ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)
        ])
        page.update()

    def coeficiente_permeabilidad(e):
        limpiar_controles()
        q = campo_resaltado("Volumen Q (litros)")
        l = campo_resaltado("Longitud L (m)")
        a = campo_resaltado("Área A (cm²)")
        h = campo_resaltado("Carga hidráulica h (m)")
        t = campo_resaltado("Tiempo t (s)")
        def calcular(ev=None):
            try:
                Q = float(q.content.value) / 1000
                L = float(l.content.value)
                A = float(a.content.value) / 10000
                H = float(h.content.value)
                T = float(t.content.value)
                k = (Q * L) / (A * H * T)
                resultado.value = f"Coef. de permeabilidad: {k:.6e} m/s"
            except Exception:
                resultado.value = ""
            page.update()
        q.content.on_change = calcular
        l.content.on_change = calcular
        a.content.on_change = calcular
        h.content.on_change = calcular
        t.content.on_change = calcular

        page.controls.extend([
            contenedor_resultado,
            ft.Text("Coeficiente de permeabilidad", size=20),
            q, l, a, h, t,
            ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)
        ])
        page.update()

    mostrar_menu()

import os
from flet import app, AppView

port = int(os.environ.get("PORT", 8550))
app(target=main, view=AppView.WEB_BROWSER, port=port)

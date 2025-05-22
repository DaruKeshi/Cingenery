import flet as ft

def main(page: ft.Page):
    page.title = "Calculadora de Ingeniería"
    page.scroll = "auto" # type: ignore
    resultado = ft.Text()
    materiales = {
        "Hormigón": 2400,
        "Cemento": 1500,
        "Arena": 1600,
        "Grava": 1700,
        "Acero": 7850,
        "Madera": 600,
    }

    def limpiar_controles():
        page.controls.clear() # type: ignore
        resultado.value = ""
        page.update()

    def mostrar_menu(e=None):
        limpiar_controles()
        page.controls.append(ft.Text("Calculadora de Ingeniería", size=24, weight="bold")) # type: ignore
        opciones = [
            ("Volumen por dimensiones", volumen_dimensiones),
            ("Volumen por masa y densidad", volumen_masa_densidad),
            ("Conversión de unidades", conversion_unidades),
            ("Cantidad de bolsas de material", cantidad_material),
            ("Presión superficial", presion_superficial),
            ("Coeficiente de permeabilidad", coeficiente_permeabilidad)
        ]
        botones = [
    ft.ElevatedButton(texto, on_click=funcion, expand=True)
    for texto, funcion in opciones
]

filas = [
    ft.Row(controls=botones[i:i+2], spacing=10)
    for i in range(0, len(botones), 2)
]

page.controls.extend(filas) # type: ignore
        page.update()

    def volumen_dimensiones(e):
        limpiar_controles()
        l = ft.TextField(label="Largo (m)")
        a = ft.TextField(label="Ancho (m)")
        h = ft.TextField(label="Altura (m)")
        def calcular(e):
            try:
                v = float(l.value) * float(a.value) * float(h.value) # type: ignore
                resultado.value = f"Volumen: {v:.4f} m³"
            except:
                resultado.value = "Error en los valores"
            page.update()
        page.controls.extend([ft.Text("Volumen (L x A x H)", size=20), l, a, h, # type: ignore # type: ignore
                              ft.ElevatedButton("Calcular", on_click=calcular),
                              resultado,
                              ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)])
        page.update()

    def volumen_masa_densidad(e):
        limpiar_controles()
        masa = ft.TextField(label="Masa")
        unidad = ft.Dropdown(label="Unidad", options=[
            ft.dropdown.Option("g"),
            ft.dropdown.Option("kg"),
            ft.dropdown.Option("toneladas")
        ], value="kg")
        densidad_custom = ft.TextField(label="Densidad personalizada (kg/m³)")
        def calcular_densidad(d):
            try:
                m = float(masa.value) # type: ignore
                u = unidad.value
                if u == "g": m /= 1000
                elif u == "toneladas": m *= 1000
                v = m / materiales[d]
                resultado.value = f"{d}: {v:.4f} m³"
            except:
                resultado.value = "Error en el cálculo"
            page.update()
        botones = [ft.ElevatedButton(mat, on_click=lambda e, m=mat: calcular_densidad(m)) for mat in materiales]
        def calcular_personalizado(e):
            try:
                m = float(masa.value) # type: ignore
                u = unidad.value
                if u == "g": m /= 1000
                elif u == "toneladas": m *= 1000
                densidad = float(densidad_custom.value) # type: ignore # type: ignore
                v = m / densidad
                resultado.value = f"Volumen: {v:.4f} m³"
            except:
                resultado.value = "Error en personalizado"
            page.update()
        page.controls.extend([ft.Text("Volumen (masa / densidad)", size=20), # type: ignore # type: ignore
                              masa, unidad, ft.Text("Selecciona material:"), *botones,
                              densidad_custom,
                              ft.ElevatedButton("Calcular con densidad personalizada", on_click=calcular_personalizado),
                              resultado,
                              ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)])
        page.update()

    def conversion_unidades(e):
        limpiar_controles()
        valor = ft.TextField(label="Valor")
        categorias = {
            "Longitud": {"m":1,"cm":0.01,"mm":0.001,"km":1000,"in":0.0254,"ft":0.3048},
            "Volumen": {"m³":1,"litros":0.001,"cm³":1e-6,"pies³":0.0283168,"galones":0.00378541},
            "Peso": {"kg":1,"g":0.001,"mg":1e-6,"toneladas":1000,"lb":0.453592},
            "Temperatura": ["C","F","K"]
        }
        categoria = ft.Dropdown(label="Categoría", options=[ft.dropdown.Option(c) for c in categorias], value="Longitud")
        u_origen = ft.Dropdown(label="Unidad de origen", options=[])
        u_destino = ft.Dropdown(label="Unidad destino", options=[])
        def actualizar_unidades(e):
            u_origen.options.clear() # type: ignore
            u_destino.options.clear() # type: ignore # type: ignore
            for u in categorias[categoria.value] if isinstance(categorias[categoria.value], dict) else categorias[categoria.value]: # type: ignore # type: ignore
                u_origen.options.append(ft.dropdown.Option(u)) # type: ignore # type: ignore # type: ignore
                u_destino.options.append(ft.dropdown.Option(u)) # type: ignore
            u_origen.value = u_origen.options[0].key # type: ignore # type: ignore
            u_destino.value = u_destino.options[1].key # type: ignore
            page.update()
        categoria.on_change = actualizar_unidades
        actualizar_unidades(None)
        def convertir(e):
            try:
                v = float(valor.value) # type: ignore
                cat = categoria.value
                u1, u2 = u_origen.value, u_destino.value
                if cat == "Temperatura":
                    if u1 == u2: r = v
                    elif u1 == "C": r = v+273.15 if u2=="K" else v*9/5+32
                    elif u1 == "F": r = (v-32)*5/9 if u2=="C" else (v-32)*5/9+273.15
                    elif u1 == "K": r = v-273.15 if u2=="C" else (v-273.15)*9/5+32
                else:
                    base = v * categorias[cat][u1] # type: ignore
                    r = base / categorias[cat][u2] # type: ignore # type: ignore
                resultado.value = f"{v} {u1} = {r:.4f} {u2}" # type: ignore
            except:
                resultado.value = "Error en la conversión"
            page.update()
        page.controls.extend([ft.Text("Conversión de unidades", size=20), # type: ignore # type: ignore
                              valor, categoria, u_origen, u_destino,
                              ft.ElevatedButton("Convertir", on_click=convertir),
                              resultado,
                              ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)])
        page.update()

    def cantidad_material(e):
        limpiar_controles()
        volumen = ft.TextField(label="Volumen (m³)")
        densidad = ft.TextField(label="Densidad (kg/m³)")
        rendimiento = ft.TextField(label="Rendimiento por bolsa (kg)")
        materiales_local = {
            "Cemento": {"densidad":1500,"rendimiento":42.5},
            "Cal": {"densidad":1350,"rendimiento":25},
            "Arena": {"densidad":1600,"rendimiento":50},
            "Grava": {"densidad":1700,"rendimiento":50},
            "Hormigón": {"densidad":2400,"rendimiento":50}
        }
        def usar_material(m):
            densidad.value = str(materiales_local[m]["densidad"])
            rendimiento.value = str(materiales_local[m]["rendimiento"])
            page.update()
        botones = [ft.ElevatedButton(mat, on_click=lambda e, m=mat: usar_material(m)) for mat in materiales_local]
        def calcular(e):
            try:
                v = float(volumen.value) # type: ignore # type: ignore
                d = float(densidad.value) # type: ignore
                r = float(rendimiento.value) # type: ignore # type: ignore
                bolsas = (v * d) / r
                resultado.value = f"Necesitas aproximadamente {bolsas:.2f} bolsas"
            except:
                resultado.value = "Error en los valores"
            page.update()
        page.controls.extend([ft.Text("Cantidad de bolsas de material", size=20), # type: ignore
                              volumen, densidad, rendimiento,
                              ft.Text("Materiales comunes:"), *botones,
                              ft.ElevatedButton("Calcular", on_click=calcular),
                              resultado,
                              ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)])
        page.update()

    def presion_superficial(e):
        limpiar_controles()
        carga = ft.TextField(label="Carga (kgf)")
        area = ft.TextField(label="Área (m²)")
        unidad = ft.Dropdown(label="Unidad", options=[ft.dropdown.Option("kg/m²"), ft.dropdown.Option("kN/m²")], value="kg/m²")
        def calcular(e):
            try:
                c = float(carga.value) # type: ignore # type: ignore
                a = float(area.value) # type: ignore
                presion = c / a
                if unidad.value == "kN/m²":
                    presion *= 0.00980665
                resultado.value = f"Presión: {presion:.4f} {unidad.value}"
            except:
                resultado.value = "Error en los valores"
            page.update()
        page.controls.extend([ft.Text("Cálculo de presión superficial", size=20), # type: ignore
                              carga, area, unidad,
                              ft.ElevatedButton("Calcular", on_click=calcular),
                              resultado,
                              ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)])
        page.update()

    def coeficiente_permeabilidad(e):
        limpiar_controles()
        q = ft.TextField(label="Volumen Q (litros)")
        l = ft.TextField(label="Longitud L (m)")
        a = ft.TextField(label="Área A (cm²)")
        h = ft.TextField(label="Carga hidráulica h (m)")
        t = ft.TextField(label="Tiempo t (s)")
        def calcular(e):
            try:
                Q = float(q.value) / 1000 # type: ignore
                L = float(l.value) # type: ignore # type: ignore
                A = float(a.value) / 10000 # type: ignore
                H = float(h.value) # type: ignore # type: ignore
                T = float(t.value) # type: ignore
                k = (Q * L) / (A * H * T)
                resultado.value = f"Coef. de permeabilidad: {k:.6e} m/s"
            except:
                resultado.value = "Error en los valores"
            page.update()
        page.controls.extend([ft.Text("Coeficiente de permeabilidad", size=20), # type: ignore
                              q, l, a, h, t,
                              ft.ElevatedButton("Calcular", on_click=calcular),
                              resultado,
                              ft.ElevatedButton("Volver al menú", on_click=mostrar_menu)])
        page.update()

    mostrar_menu()

import os
from flet import app, AppView

port = int(os.environ.get("PORT", 8550))

app(target=main, view=AppView.WEB_BROWSER, port=port)

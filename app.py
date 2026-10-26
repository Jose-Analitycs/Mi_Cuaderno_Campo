import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime

# Configuración de página para Tablet / Móvil
st.set_page_config(
    page_title="Cuaderno de Campo - Finca & Huerto",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_FILE = "datos_agricolas.json"

# --- FUNCIONES DE BASE DE DATOS (JSON) ---
def cargar_datos():
    if not os.path.exists(DB_FILE):
        datos_iniciales = {
            "tratamientos": [
                {"fecha": "2026-02-15", "cultivo": "Melocotonero", "tipo": "Tratamiento de Invierno", "producto": "Aceite Mineral + Cobre", "dosis": "15 ml/L + 3 g/L", "notas": "Aplicado en yema hinchada"},
                {"fecha": "2026-02-20", "cultivo": "Azufaifo", "tipo": "Tratamiento de Invierno", "producto": "Aceite Mineral", "dosis": "15 ml/L", "notas": "Preventivo cochinilla"}
            ],
            "siembras": [
                {"fecha": "2026-10-05", "cultivo": "Ajos", "ubicacion": "Huerto Elevado - Bancal 1", "cantidad": 60, "unidad": "dientes", "notas": "Variedad morada"},
                {"fecha": "2026-10-12", "cultivo": "Habas", "ubicacion": "Huerto Elevado - Bancal 2", "cantidad": 40, "unidad": "semillas", "notas": "Siembra directa con goteo"}
            ],
            "cosechas": [
                {"fecha": "2026-07-20", "cultivo": "Melocotonero", "cantidad": 14.5, "unidad": "kg", "notas": "Excelente sabor y buen calibre"},
                {"fecha": "2026-09-15", "cultivo": "Calabaza Cacahuete", "cantidad": 28.0, "unidad": "kg", "notas": "Cosechadas 8 piezas grandes"}
            ]
        }
        guardar_datos(datos_iniciales)
        return datos_iniciales
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(datos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# Cargar datos en memoria
datos = cargar_datos()

# Encabezado principal
st.title("🌿 Cuaderno de Campo & Huerto")
st.caption("Gestión integral de tratamientos, siembras y cosecha")

# --- MENÚ POR PESTAÑAS (Ideal para Pantalla Táctil) ---
tab1, tab2, tab3 = st.tabs(["📝 Registrar Nuevo", "📊 Estadísticas y Consultas", "📂 Resumen General"])

# ==========================================
# PESTAÑA 1: REGISTRAR NUEVO DATO
# ==========================================
with tab1:
    st.header("Añadir nuevo registro")
    tipo_registro = st.radio("¿Qué deseas registrar?", ["🚜 Tratamiento / Abonado", "🌱 Siembra / Plantación", "🧺 Cosecha"], horizontal=True)

    if tipo_registro == "🚜 Tratamiento / Abonado":
        with st.form("form_tratamiento", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("Fecha", datetime.now()).strftime("%Y-%m-%d")
                cultivo = st.text_input("Árbol / Cultivo", placeholder="Ej: Melocotonero, Azufaifo, Bancal 1")
                tipo_trabajo = st.selectbox("Tipo de trabajo", ["Tratamiento de Invierno", "Fungicida", "Insecticida", "Abonado / Humus", "Riego / Fertirriego", "Poda"])
            with col2:
                producto = st.text_input("Producto utilizado", placeholder="Ej: Aceite mineral + Cobre")
                dosis = st.text_input("Dosis / Cantidad", placeholder="Ej: 15 ml/L o 2 kg por árbol")
                notas = st.text_area("Observaciones", placeholder="Ej: Sin viento, yema hinchada...")

            if st.form_submit_button("💾 Guardar Tratamiento"):
                if cultivo and producto:
                    datos["tratamientos"].append({"fecha": fecha, "cultivo": cultivo, "tipo": tipo_trabajo, "producto": producto, "dosis": dosis, "notas": notas})
                    guardar_datos(datos)
                    st.success(f"✅ Tratamiento guardado para {cultivo}")
                    st.rerun()
                else:
                    st.warning("Por favor, rellena al menos el árbol/cultivo y el producto.")

    elif tipo_registro == "🌱 Siembra / Plantación":
        with st.form("form_siembra", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("Fecha de siembra", datetime.now()).strftime("%Y-%m-%d")
                cultivo = st.text_input("Cultivo / Variedad", placeholder="Ej: Habas, Ajos, Calabaza Cacahuete")
                ubicacion = st.text_input("Ubicación", placeholder="Ej: Huerto Elevado - Bancal 1")
            with col2:
                cantidad = st.number_input("Cantidad", min_value=1, value=10)
                unidad = st.selectbox("Unidad", ["plantas", "semillas", "dientes de ajo", "matas"])
                notas = st.text_area("Observaciones", placeholder="Ej: Marco de plantación 20cm, riego instalado...")

            if st.form_submit_button("💾 Guardar Siembra"):
                if cultivo:
                    datos["siembras"].append({"fecha": fecha, "cultivo": cultivo, "ubicacion": ubicacion, "cantidad": cantidad, "unidad": unidad, "notas": notas})
                    guardar_datos(datos)
                    st.success(f"✅ Siembra registrada para {cultivo}")
                    st.rerun()
                else:
                    st.warning("Por favor, indica el nombre del cultivo.")

    elif tipo_registro == "🧺 Cosecha":
        with st.form("form_cosecha", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("Fecha de recogida", datetime.now()).strftime("%Y-%m-%d")
                cultivo = st.text_input("Árbol / Cultivo recolectado", placeholder="Ej: Melocotonero, Azufaifo, Habas")
            with col2:
                cantidad = st.number_input("Cantidad cosechada", min_value=0.1, step=0.5, value=1.0)
                unidad = st.selectbox("Unidad de medida", ["kg", "unidades", "cajas"])
                notas = st.text_area("Notas de cosecha", placeholder="Ej: Fruta muy dulce, primer pase...")

            if st.form_submit_button("💾 Guardar Cosecha"):
                if cultivo:
                    datos["cosechas"].append({"fecha": fecha, "cultivo": cultivo, "cantidad": cantidad, "unidad": unidad, "notas": notas})
                    guardar_datos(datos)
                    st.success(f"✅ Cosecha de {cantidad} {unidad} guardada para {cultivo}")
                    st.rerun()
                else:
                    st.warning("Por favor, indica el cultivo o árbol.")

# ==========================================
# PESTAÑA 2: ESTADÍSTICAS Y CONSULTAS
# ==========================================
with tab2:
    st.header("📊 Estadísticas e Historial por Cultivo")
    st.write("Consulta todo lo que le has hecho a un árbol o bancal y analiza su producción.")

    # Extraer todos los cultivos registrados
    todos_cultivos = sorted(list(set(
        [d["cultivo"] for d in datos["tratamientos"]] +
        [d["cultivo"] for d in datos["siembras"]] +
        [d["cultivo"] for d in datos["cosechas"]]
    )))

    if todos_cultivos:
        cultivo_sel = st.selectbox("🔍 Selecciona un Árbol o Cultivo para analizar:", todos_cultivos)

        if cultivo_sel:
            st.subheader(f"Ficha de Control: **{cultivo_sel}**")

            # Módulos métricos de resumen rápido
            col_m1, col_m2, col_m3 = st.columns(3)
            
            # Filtrar registros del cultivo seleccionado
            trats_c = [t for t in datos["tratamientos"] if t["cultivo"] == cultivo_sel]
            siem_c = [s for s in datos["siembras"] if s["cultivo"] == cultivo_sel]
            cos_c = [c for c in datos["cosechas"] if c["cultivo"] == cultivo_sel]

            total_kg = sum([c["cantidad"] for c in cos_c if c["unidad"] == "kg"])
            ult_trat = trats_c[-1]["fecha"] if trats_c else "Ninguno"

            with col_m1:
                st.metric("Total Kilos Cosechados", f"{total_kg:.1f} kg")
            with col_m2:
                st.metric("Total Tratamientos Dados", len(trats_c))
            with col_m3:
                st.metric("Último Tratamiento", ult_trat)

            st.divider()

            # --- GRÁFICO DE PRODUCCIÓN DEL CULTIVO ---
            if cos_c:
                st.markdown("### 📈 Evolución de Cosechas")
                df_cos_c = pd.DataFrame(cos_c)
                fig_c = px.bar(df_cos_c, x="fecha", y="cantidad", color="unidad", title=f"Histórico de recolección de {cultivo_sel}", labels={"fecha": "Fecha", "cantidad": "Cantidad"})
                st.plotly_chart(fig_c, use_container_width=True)

            # --- TABLAS DE HISTORIAL DETALLADO ---
            st.markdown("### 🚜 Historial de Tratamientos y Trabajos")
            if trats_c:
                st.dataframe(pd.DataFrame(trats_c)[["fecha", "tipo", "producto", "dosis", "notas"]], use_container_width=True)
            else:
                st.info("No hay tratamientos registrados para este cultivo.")

            st.markdown("### 🌱 Historial de Siembras / Plantaciones")
            if siem_c:
                st.dataframe(pd.DataFrame(siem_c)[["fecha", "ubicacion", "cantidad", "unidad", "notas"]], use_container_width=True)
            else:
                st.info("No hay siembras registradas para este cultivo.")

            st.markdown("### 🧺 Registro de Cosechas")
            if cos_c:
                st.dataframe(pd.DataFrame(cos_c)[["fecha", "cantidad", "unidad", "notas"]], use_container_width=True)
            else:
                st.info("No hay cosechas registradas para este cultivo.")
    else:
        st.info("Aún no has registrado ningún dato. Empieza en la pestaña '📝 Registrar Nuevo'.")

# ==========================================
# PESTAÑA 3: RESUMEN GENERAL
# ==========================================
with tab3:
    st.header("📂 Resumen Global de la Finca")
    
    if datos["cosechas"]:
        st.subheader("Comparativa de Producción Total por Cultivo")
        df_todas_cos = pd.DataFrame(datos["cosechas"])
        df_kg = df_todas_cos[df_todas_cos["unidad"] == "kg"]
        
        if not df_kg.empty:
            resumen_kg = df_kg.groupby("cultivo")["cantidad"].sum().reset_index()
            fig_global = px.pie(resumen_kg, values="cantidad", names="cultivo", title="Reparto Total de Cosecha (en Kilos)", hole=0.4)
            st.plotly_chart(fig_global, use_container_width=True)
    
    st.subheader("Todos los datos registrados")
    with st.expander("Ver tabla global de tratamientos"):
        if datos["tratamientos"]:
            st.dataframe(pd.DataFrame(datos["tratamientos"]))
    with st.expander("Ver tabla global de siembras"):
        if datos["siembras"]:
            st.dataframe(pd.DataFrame(datos["siembras"]))
    with st.expander("Ver tabla global de cosechas"):
        if datos["cosechas"]:
            st.dataframe(pd.DataFrame(datos["cosechas"]))
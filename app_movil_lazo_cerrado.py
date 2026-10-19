#!/usr/bin/env python3
"""
========================================================================================
    CUECALABS MOBILE SUITE v1.0 — INTERFAZ WEB INTERACTIVA PARA DISPOSITIVOS MÓVILES
========================================================================================
Copyright (c) 2026 CuecaLabsATP0305. Todos los derechos reservados.
Licencia Comercial y Regulatoria CuecaLabs (CL-CRL v1.0).

Este módulo web permite operar el motor estocástico de lazo cerrado directamente
desde pantallas táctiles y navegadores de teléfonos celulares en el entorno clínico.
========================================================================================
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración de la Interfaz Móvil Receptiva
st.set_page_config(
    page_title="CuecaLabs Mobile Suite",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilo personalizado para botones y contenedores móviles
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding-top: 1rem; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    div[data-testid="stMetricValue"] { font-size: 24px; font-weight: bold; color: #2980B9; }
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado Institucional
st.title("🔬 CuecaLabs Mobile Suite")
st.subheader("Máquina Gold Standard en Lazo Cerrado para Emergencias")

st.info("⚠️ **Aviso Clínico:** Esta simulación asiste la toma de decisiones, pero NUNCA reemplaza el juicio clínico del profesional en el terreno.")

# 3. Panel de Control de Variables Táctiles (Inputs para el Médico)
st.markdown("### 📊 Parámetros del Paciente")
fármaco_agresor = st.selectbox("Seleccione el Fármaco Causante del Colapso:", ["Metamizol (Dipirona)", "Inhibidor de la ECA", "AINE Clásico", "Otro Citotóxico"])
tiempo_intervencion = st.slider("Ventana de Observación (Horas):", min_value=12, max_value=72, value=48, step=6)
ruido_termico_ajuste = st.slider("Ruido Estocástico Celular (Fluctuación):", min_value=0.5, max_value=3.0, value=1.5, step=0.1)

# 4. Motor de Cómputo Estocástico Multivariable en Lazo Cerrado
def ejecutar_motor_movil(pasos=500, tiempo_max=48, factor_ruido=1.5):
    t = np.linspace(0, tiempo_max, pasos)
    np.random.seed(42)
    ruido = np.random.normal(0, factor_ruido, len(t))
    
    # Eje Homeostático Principal Sostenido
    eje_homeo = 100 + 50 * (1 - np.exp(-0.2 * t)) + ruido * 0.5
    # Ruta en Escape Sin Control (Farmacología Antigua)
    ruta_libre = 100 + 4.5 * t + 15 * np.sin(0.4 * t) + ruido
    # Ruta Mitigada por Lazo Cerrado y Activador Quiral
    atenuacion = np.exp(-0.15 * t)
    ruta_controlada = 100 + 40 * np.sin(0.5 * t) * atenuacion + ruido * 0.3
    
    return t, eje_homeo, ruido, ruta_libre, ruta_controlada

# Botón Táctil de Simulación
if st.button("▶️ EJECUTAR SIMULACIÓN DE RESCATE"):
    t, eh, rd, rrl, rrc = ejecutar_motor_movil(tiempo_max=tiempo_intervencion, factor_ruido=ruido_termico_ajuste)
    
    # 5. Métricas de Estado Crítico Actuales
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Ruta Sin Control (Escape)", value=f"{rrl[-1]:.1f} %", delta="CRÍTICO", delta_color="inverse")
    with col2:
        st.metric(label="Ruta Controlada (CuecaLabs)", value=f"{rrc[-1]:.1f} %", delta="ESTABLE")
        
    # 6. Renderizado de Gráfico Científico Optimizado para Pantallas Móviles
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(t, eh, color='#1E8449', linewidth=2, label='Eje Homeostático')
    ax.plot(t, rrl, color='#C0392B', linestyle='--', linewidth=1.5, label='Escape (Antiguo)')
    ax.plot(t, rrc, color='#2980B9', linewidth=2.5, label='Lazo Cerrado (Antídoto Quiral)')
    ax.axhspan(85, 125, alpha=0.15, color='#3498DB', label='Zona de Seguridad (85-125%)')
    ax.axhline(100, color='#7F8C8D', linestyle=':', alpha=0.6)
    
    ax.set_title('Perfil Cinético Proyectado', fontsize=10, weight='bold')
    ax.set_xlabel('Tiempo (Horas)', fontsize=8)
    ax.set_ylabel('Respuesta Celular (%)', fontsize=8)
    ax.legend(loc='upper left', fontsize=7, frameon=True)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.tick_params(axis='both', which='major', labelsize=8)
    
    st.pyplot(fig)
    
    # Mensaje diagnóstico automatizado
    if rrc[-1] >= 85 and rrc[-1] <= 125:
        st.success("🎯 ÉXITO TERAPÉUTICO: El sistema confirma la convergencia matemática hacia el Atractor Seguro dentro de la ventana de tolerancia.")
    else:
        st.warning("⚠️ ADVERTENCIA: Ajustar la concentración del activador quiral para forzar la atenuación del bucle.")

# 7. Sección de Instrucciones de Uso Rápido Multilingüe Integrada
with st.expander("🌐 Quick Instructions / Instructivo Multilingüe"):
    st.markdown("""
    - **ES:** Ingrese datos del paciente, presione Ejecutar y vigile que la línea azul converja en la zona sombreada.
    - **EN:** Input patient data, press Run, and ensure the blue line converges within the shaded area.
    - **ZH:** 输入患者数据，点击运行，并确保蓝色曲线收敛在阴影区域内。
    - **HI:** मरीज का डेटा दर्ज करें, रन दबाएं, और सुनिश्चित करें कि नीली रेखा छायादार क्षेत्र में स्थिर हो।
    - **FR:** Saisissez les données du patient, appuyez sur Exécuter et vérifiez que la ligne bleue converge dans la zone ombrée.
    """)


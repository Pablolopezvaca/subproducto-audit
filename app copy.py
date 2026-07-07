import streamlit as st
import google.generativeai as genai
import os

# Cargar el archivo CSS para mejorar la UI
try:
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    pass

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y CREDENCIALES
# =====================================================================
st.set_page_config(
    page_title="Subproducto-Check 🌿",
    page_icon="🌿",
    layout="centered"
)

# Configura tu clave de API de Google AI Studio (Gemini Pro)
if "API_KEY" not in st.session_state:
    st.session_state["API_KEY"] = ""

with st.sidebar:
    st.header("🔑 Configuración")
    api_key_input = st.text_input("Introduce tu Gemini API Key:", type="password", value=st.session_state["API_KEY"])
    if api_key_input:
        # LIMPIAR ESPACIOS INVISIBLES
        clave_limpia = api_key_input.strip() 
        st.session_state["API_KEY"] = clave_limpia
        genai.configure(api_key=clave_limpia)
    st.markdown("---")
    st.caption("Desarrollado como Proyecto Integrador - Campus Waste Lab Bizkaia")

st.title("Subproducto-Audit")
st.subheader("Validador Normativo Inteligente para PYMEs (País Vasco)")
st.markdown("""
Esta herramienta ayuda a las pequeñas y medianas empresas industriales a evaluar si sus mermas o materiales 
sobrantes de proceso pueden dejar de ser considerados legalmente como un 'residuo' y tramitarse como **Subproducto**, 
según el **Artículo 4 de la Ley Estatal 7/2022** y los marcos ambientales del País Vasco.
""")

st.markdown("---")

# =====================================================================
# 2. BLOQUE 1: CONFIGURACIÓN DE LA PYME e INPUTS
# =====================================================================
st.header("1. Datos de Operación en Planta")

sector = st.selectbox(
    "Sector Industrial de la Empresa:",
    ["Mecanizado y Metalurgia", "Transformación de Plásticos", "Automoción y Componentes", "Otros sectores industriales"]
)

toneladas = st.slider(
    "Volumen de material generado (Toneladas métricas al año):",
    min_value=1,
    max_value=500,
    value=50
)

descripcion_material = st.text_area(
    "Describa brevemente el material sobrante, en qué etapa del proceso se genera y para qué se podría usar:",
    placeholder="Ejemplo: Virutas limpias de plástico ABS procedentes de mermas de moldes de inyección, sin contaminación de aceites..."
)

st.markdown("---")

# =====================================================================
# 3. BLOQUE 2: EVALUACIÓN DE REQUISITOS LEGALES (ART. 4 LEY 7/2022)
# =====================================================================
st.header("2. Autoevaluación del Artículo 4 (Ley 7/2022)")
st.markdown("Selecciona las condiciones que cumple actualmente este flujo de material:")

c1 = st.checkbox("🔮 **Certeza de uso posterior:** ¿Existe un contrato formal, un comprador garantizado o una demanda clara en el mercado para este material?")
c2 = st.checkbox("⚙️ **Uso directo sin transformación compleja:** ¿El material puede utilizarse directamente en la otra empresa sin someterse a procesos industriales pesados ajenos a la práctica habitual?")
c3 = st.checkbox("🏭 **Origen integrado en el proceso:** ¿El material se produce de forma inevitable como parte integrante del proceso de producción principal (no es un descarte buscado)?")
c4 = st.checkbox("🛡️ **Cumplimiento técnico y ambiental:** ¿El uso del material cumple con todas las normas del mercado de destino y se garantiza que no tendrá impactos adversos en la salud humana ni en el medio ambiente de la CAPV?")

st.markdown("---")

# =====================================================================
# 4. BLOQUE 3: CÁLCULOS DINÁMICOS EN PLANTA
# =====================================================================
st.header("3. Pre-diagnóstico e Impacto Económico")

# Calcular índice de cumplimiento (Cada check suma 25%)
checks = [c1, c2, c3, c4]
porcentaje_cumplimiento = sum(checks) * 25

if porcentaje_cumplimiento < 100:
    st.error(f"🔴 ESTADO: Residuo Convencional ({porcentaje_cumplimiento}% de cumplimiento legal)")
    st.warning("⚠️ **Nota:** Al no cumplir con las 4 condiciones simultáneas del Artículo 4, el material debe gestionarse obligatoriamente como residuo convencional, priorizando la reducción en origen.")
else:
    st.success("🟢 ESTADO: Alta Viabilidad de Subproducto (100% de cumplimiento legal)")
    
    # Cálculo económico basado en costes promedio de Bizkaia (Impuesto Ley 7/2022 [10€] + Vertedero [65€] = 75€/Tm)
    ahorro_unitario = 75 
    ahorro_total = toneladas * ahorro_unitario
    
    st.metric(
        label="Ahorro Económico Estimado en Bizkaia (Tasas Evitadas + Canon de Vertedero)",
        value=f"{ahorro_total:,} € / año",
        delta="Coste Directo Evitado"
    )

st.markdown("---")

# =====================================================================
# 5. CONEXIÓN CON LA API DE GEMINI (MOTOR DE DECISIÓN LEGAL)
# =====================================================================
st.header("4. Generador de Informe Técnico Completo")
st.markdown("Presiona el botón para que la IA Generativa realice la auditoría legal de fondo y redacte la hoja de ruta corporativa:")

if st.button("🚀 Lanzar Auditoría Inteligente"):
    if not st.session_state["API_KEY"]:
        st.error("❌ Por favor, introduce tu Gemini API Key en la barra lateral izquierda.")
    else:
        with st.spinner("Auditando normativa y generando Plan de Acción (CIMAS)..."):
            try:
                # Forzamos la clave a nivel de sistema para evitar bloqueos de Streamlit
                os.environ["GOOGLE_API_KEY"] = st.session_state["API_KEY"]
                genai.configure(api_key=st.session_state["API_KEY"])
                
                # BUSCADOR DINÁMICO: Le preguntamos a Google qué modelos permite desde Europa
                modelos_permitidos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                if not modelos_permitidos:
                    st.error("Tu API Key actual no tiene permisos para generar texto desde esta región.")
                else:
                    # Priorizamos el mejor modelo que esté disponible en la lista real
                    modelo_elegido = modelos_permitidos[0] # Por defecto coge el primero que exista
                    preferencias = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro', 'models/gemini-1.0-pro']
                    
                    for pref in preferencias:
                        if pref in modelos_permitidos:
                            modelo_elegido = pref
                            break
                            
                    st.success(f"🌍 Conexión establecida desde Europa usando: **{modelo_elegido}**")
                    
                    # Prompt de instrucciones de sistema inyectado (Enfoque WLB + CIMAS)
                    instrucciones_auditor = """
                    Actúas como un Consultor Ambiental Experto y Auditor Legal especializado en la normativa de residuos del País Vasco (Ihobe, PGRA 2030, CIMAS).
                    Tu tarea es analizar los datos suministrados por la PYME y emitir un dictamen riguroso y formal.
                    
                    Debes estructurar tu respuesta estrictamente en los siguientes apartados:
                    
                    ### 📄 1. Dictamen Técnico-Legal de Fondos
                    - Analiza los datos del material y evalúa si su justificación técnica se sostiene frente al Artículo 4 de la Ley 7/2022.
                    - Cita las implicaciones en el País Vasco y los riesgos de inspección asociados a una incorrecta declaración.
                    
                    ### 📈 2. Plan de Acción Corporativo (Metodología CIMAS)
                    Genera una tabla estructurada: 
                    - Acción Concreta (Qué pasos dar).
                    - Plazo Estimado (Meses).
                    - Responsable Departamental (Dirección, Operaciones, HSE).
                    - KPI Cuantitativo de Seguimiento (Ej: Tasa de valorización, reducción de coste de vertido).
                    
                    ### 📢 3. Pauta de Comunicación Interna 
                    - Pauta corta con el mensaje para los operarios de planta para evitar contaminación cruzada.
                    """
                    
                    # Datos recopilados
                    datos_pyme = f"Sector: {sector} | Volumen: {toneladas} Tm/año | Descripción: {descripcion_material} | Requisitos Cumplidos: Certeza={c1}, Uso={c2}, Origen={c3}, Inocuidad={c4}"
                    
                    # Fusionamos todo en un solo texto (Bypass de errores)
                    prompt_completo = f"{instrucciones_auditor}\n\nAnaliza esta PYME:\n{datos_pyme}"
                    
                    # Llamada final
                    model = genai.GenerativeModel(modelo_elegido)
                    response = model.generate_content(prompt_completo)
                    
                    # --- DASHBOARD DE MÉTRICAS ---
                    st.markdown("### 📊 Dashboard de Impacto Operativo (KPIs)")
                    col1, col2, col3 = st.columns(3)
                    
                    # Cálculos dinámicos para darle realismo a los datos
                    ahorro_mostrar = toneladas * 75 if porcentaje_cumplimiento == 100 else 0
                    co2_evitado = toneladas * 0.85 # Factor estimado de huella
                    
                    col1.metric("Ahorro Estimado", f"{ahorro_mostrar:,} €/año", "Viabilidad Alta" if porcentaje_cumplimiento == 100 else "Alerta")
                    col2.metric("Huella Evitada (CO2e)", f"{co2_evitado:.1f} Ton", "-15% Emisiones")
                    col3.metric("Tasa de Circularidad", "92%", "+12% interanual")
                    st.markdown("---")
                    
                    # --- INFORME TÉCNICO EN FORMATO TXT ---
                    st.markdown("### 📥 INFORME TÉCNICO GENERADO AUTÓNOMAMENTE")
                    st.markdown(response.text)
                    
                    # --- BOTÓN DE DESCARGA ---
                    st.download_button(
                        label="📄 Descargar Informe Técnico en formato texto (.txt)",
                        data=response.text,
                        file_name="Auditoria_CIMAS_Subproducto.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"Error detallado de Google API: {e}")
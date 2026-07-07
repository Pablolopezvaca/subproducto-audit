import streamlit as st
from google import genai
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

if "API_KEY" not in st.session_state:
    st.session_state["API_KEY"] = ""

with st.sidebar:
    st.header("🔑 Configuración")
    api_key_input = st.text_input("Introduce tu Gemini API Key:", type="password", value=st.session_state["API_KEY"])
    if api_key_input:
        clave_limpia = api_key_input.strip() 
        st.session_state["API_KEY"] = clave_limpia
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

checks = [c1, c2, c3, c4]
porcentaje_cumplimiento = sum(checks) * 25

if porcentaje_cumplimiento < 100:
    st.error(f"🔴 ESTADO: Residuo Convencional ({porcentaje_cumplimiento}% de cumplimiento legal)")
    st.warning("⚠️ **Nota:** Al no cumplir con las 4 condiciones simultáneas del Artículo 4, el material debe gestionarse obligatoriamente como residuo convencional, priorizando la reducción en origen.")
else:
    st.success("🟢 ESTADO: Alta Viabilidad de Subproducto (100% de cumplimiento legal)")
    ahorro_unitario = 75 
    ahorro_total = toneladas * ahorro_unitario
    
    st.metric(
        label="Ahorro Económico Estimado en Bizkaia (Tasas Evitadas + Canon de Vertedero)",
        value=f"{ahorro_total:,} € / año",
        delta="Coste Directo Evitado"
    )

st.markdown("---")

# =====================================================================
# 5. CONEXIÓN CON LA API DE GEMINI (CON BUSCADOR DINÁMICO PARA EUROPA)
# =====================================================================
st.header("4. Generador de Informe Técnico Completo")

if st.button("🚀 Lanzar Auditoría Inteligente"):
    if not st.session_state["API_KEY"]:
        st.error("❌ Por favor, introduce tu Gemini API Key en la barra lateral izquierda.")
    else:
        with st.spinner("Auditando normativa y generando Plan de Acción (DEKO)..."):
            try:
                # Inicialización del nuevo cliente
                client = genai.Client(api_key=st.session_state["API_KEY"])
                
                # BUSCADOR DINÁMICO PARA COMPATIBILIDAD EN EUROPA:
                # Listamos los modelos y extraemos sus nombres limpios (ej. 'gemini-1.5-flash')
                # BUSCADOR DINÁMICO REFACTORIZADO PARA EL NUEVO SDK:
                modelos_permitidos = []
                for m in client.models.list():
                    # Comprobamos si el modelo soporta la acción de generar contenido
                    if 'generate_content' in m.supported_actions or 'generateContent' in m.supported_actions:
                        nombre_modelo = m.name.split('/')[-1]
                        modelos_permitidos.append(nombre_modelo)
                
                if not modelos_permitidos:
                    st.error("Tu API Key actual no devuelve modelos disponibles para generar texto desde esta región.")
                else:
                    # Definimos el orden de preferencia del modelo. No se usa gemini 2.0 porque la cuota es menor
                    preferencias = ['gemini-1.5-flash']
                    modelo_elegido = modelos_permitidos[0] # Por defecto toma el primero disponible
                    
                    for pref in preferencias:
                        if pref in modelos_permitidos:
                            modelo_elegido = pref
                            break
                            
                    st.success(f"🌍 Conexión regional establecida con éxito usando: **{modelo_elegido}**")
                    
                    instrucciones_auditor = """
                    Actúas como un Consultor Ambiental Experto y Auditor Legal especializado en la normativa de residuos del País Vasco (Ihobe, PGRA 2030, CIMAS).
                    Tu tarea es analizar los datos suministrados por la PYME y emitir un dictamen riguroso y formal.
                    
                    Debes estructurar tu respuesta estrictamente en los siguientes apartados:
                    
                    ### 📄 1. Dictamen Técnico-Legal de Fondos
                    - Analiza los datos del material y evalúa si su justificación técnica se sostiene frente al Artículo 4 de la Ley 7/2022.
                    - Cita las implicaciones en el País Vasco y los riesgos de inspección asociados a una incorrecta declaración.
                    
                    ### 📈 2. Plan de Acción Corporativo (Metodología DEKO (Datu-Ekonomia Zirkularra Operazioetan / Datos y Economía Circular en Operaciones))
                    Genera una tabla estructurada: 
                    - Acción Concreta (Qué pasos dar).
                    - Plazo Estimado (Meses).
                    - Responsable Departamental (Dirección, Operaciones, HSE).
                    - KPI Cuantitativo de Seguimiento (Ej: Tasa de valorización, reducción de coste de vertido).
                    
                    ### 📢 3. Pauta de Comunicación Interna 
                    - Pauta corta con el mensaje para los operarios de planta para evitar contaminación cruzada.
                    """
                    
                    datos_pyme = f"Sector: {sector} | Volumen: {toneladas} Tm/año | Descripción: {descripcion_material} | Requisitos Cumplidos: Certeza={c1}, Uso={c2}, Origen={c3}, Inocuidad={c4}"
                    prompt_completo = f"{instrucciones_auditor}\n\nAnaliza esta PYME:\n{datos_pyme}"
                    
                    # Llamada final utilizando el modelo detectado de forma dinámica
                    response = client.models.generate_content(
                        model=modelo_elegido,
                        contents=prompt_completo,
                    )
                    
                    # --- DASHBOARD DE MÉTRICAS ---
                    st.markdown("### 📊 Dashboard de Impacto Operativo (KPIs)")
                    col1, col2, col3 = st.columns(3)
                    
                    ahorro_mostrar = toneladas * 75 if porcentaje_cumplimiento == 100 else 0
                    co2_evitado = toneladas * 0.85
                    
                    col1.metric("Ahorro Estimado", f"{ahorro_mostrar:,} €/año", "Viabilidad Alta" if porcentaje_cumplimiento == 100 else "Alerta")
                    col2.metric("Huella Evitada (CO2e)", f"{co2_evitado:.1f} Ton", "-15% Emisiones")
                    col3.metric("Tasa de Circularidad", "92%", "+12% interanual")
                    st.markdown("---")
                    
                    st.markdown("### 📥 INFORME TÉCNICO GENERADO AUTÓNOMAMENTE")
                    st.markdown(response.text)
                    
                    st.download_button(
                        label="📄 Descargar Informe Técnico en formato texto (.txt)",
                        data=response.text,
                        file_name="Auditoria_DEKO_Subproducto.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"Error detallado de Google API (genai): {e}")
# 🌿 Subproducto-Check: Validador Inteligente para PYMEs Industriales

## 📌 Visión General
**Subproducto-Check** es una aplicación analítica y operativa diseñada para optimizar los workflows de sostenibilidad en plantas industriales del País Vasco. Su objetivo es evaluar de forma estructurada si las mermas o materiales sobrantes de los procesos de fabricación pueden dejar de considerarse legalmente como "residuos" y transicionar al estatus de **Subproducto**, conforme al Artículo 4 de la Ley 7/2022.

Este proyecto nace de la integración de conocimientos adquiridos en el programa **Waste Lab Bizkaia** y su aplicación práctica dentro de la iniciativa de incubación y emprendimiento **Aktibarural**, combinando la rigurosidad técnica de las operaciones en planta con el análisis de datos y la inteligencia artificial.

## ⚙️ ¿Para qué sirve?
En entornos industriales altamente regulados, la correcta categorización de los flujos de materiales es vital. Esta herramienta permite a los equipos de operaciones, calidad y medio ambiente:
1. **Validar requisitos:** Comprobar de forma interactiva las cuatro condiciones legales simultáneas necesarias para declarar un subproducto.
2. **Proyectar viabilidad:** Calcular instantáneamente los ahorros económicos (tasas evitadas y canon de vertedero en Bizkaia) basados en los volúmenes de generación.
3. **Automatizar el reporting:** Generar un pre-diagnóstico técnico y un plan de acción (*Plan de Trazabilidad Industrial*) utilizando IA generativa, facilitando la toma de decisiones basada en datos.

## 🚀 Características Principales
* **Interfaz de Captura de Datos Operativos:** Registro ágil del sector, toneladas generadas y caracterización del flujo de material en planta.
* **Cálculo de Impacto en Tiempo Real:** Dashboard interactivo que muestra KPIs críticos operativos: ahorros estimados y emisiones de CO2e evitadas.
* **Auditoría IA Integrada:** Conexión segura con el último SDK de Google Gemini (`google-genai`) para redactar dictámenes técnicos estructurados y pautas de comunicación interna para operarios.
* **Exportación de Evidencias:** Descarga del informe técnico en formato texto (`.txt`) para asegurar la trazabilidad de la información.

## 🛠️ Cómo Funciona (Ejemplo de Uso)
Imagina una planta del sector de **Mecanizado y Metalurgia** que genera 120 toneladas anuales de virutas limpias de aluminio (aleación 6063).
1. **Entrada de Datos:** El técnico introduce el volumen (120 Tm) y describe el origen del material y la existencia de una carta de intenciones de compra.
2. **Autoevaluación:** Se marcan las casillas correspondientes a la viabilidad de uso directo, certeza de mercado, origen integrado e inocuidad (Artículo 4).
3. **Resultados Cuantitativos:** Si el cumplimiento es del 100%, la app calcula automáticamente el impacto (ej. 9.000 €/año en costes directos evitados en Bizkaia).
4. **Generación de Hoja de Ruta:** Al pulsar "Lanzar Auditoría Inteligente", el motor dinámico procesa los datos mediante IA y devuelve un plan de acción operativo con responsables, plazos y KPIs de seguimiento departamental.

## 💻 Instalación y Despliegue Local

### Requisitos Previos
* Python 3.10 o superior.
* Una clave API de Google AI Studio.

### Pasos de Instalación
1. Clona el repositorio y navega al directorio del proyecto:
   ```bash
   git clone [https://github.com/Pablolopezvaca/subproducto-audit.git](https://github.com/Pablolopezvaca/subproducto-audit.git)
   cd subproducto-audit

2. Crea un entorno virtual y actívalo:
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate   

3. Instala las dependencias necesarias:
    pip install -r requirements.txt

4. Ejecúta la app en streamlit:
    streamlit run app.py

## 👤 Sobre el autor
Este desarrollo refleja un enfoque orientado a la sostenibilidad basada en datos y operaciones. Como especialista técnico en operaciones y datos dentro de entornos de alta complejidad, el objetivo principal de este proyecto es demostrar cómo la aplicación de Python y herramientas de automatización pueden optimizar workflows, consolidar indicadores ambientales (como huella de carbono y circularidad) y aportar trazabilidad absoluta a la información en planta para el cumplimiento normativo ESG y marcos como CSRD/ESRS o VSME.
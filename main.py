import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """
    A continuación encontrará un borrador de texto que puede estar mal redactado.
    Su objetivo es:
    - Redactar correctamente el borrador de texto
    - Convertir el proyecto de texto a un tono específico
    - Convertir el borrador de texto a un dialecto determinado

    He aquí algunos ejemplos diferentes Tonos:
    - Formal: ¡Saludos! OpenAI ha anunciado que Sam Altman se reincorpora a la empresa como Consejero Delegado. Tras un periodo de cinco días de conversaciones, discusiones y deliberaciones, se ha tomado la decisión de traer de vuelta a Altman, que había sido previamente despedido. Estamos encantados de dar la bienvenida de nuevo a Sam a OpenAI.
    - Informal: Hola a todos, ¡ha sido una semana loca! Tenemos una noticia emocionante que compartir: Sam Altman ha vuelto a OpenAI, asumiendo el cargo de director ejecutivo. Después de un montón de intensas conversaciones, debates y convencimientos, Altman hace su regreso triunfal a la startup de IA que cofundó.   

    Por favor, comience la redacción con una cálida introducción. Añada la introducción \
        si es necesario.
    
    A continuación figura el borrador del texto, el tono y el dialecto:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    SU {dialect} RESPUESTA:
"""

#Definición de variables PromptTemplate
prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)


#LLM y función de carga de llaves
def load_LLM(openai_api_key):
    """La lógica para cargar la cadena que desea utilizar debe ir aquí."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm


#Título y cabecera de la página
st.set_page_config(page_title="Reescriba su texto")
st.header("Reescriba su texto")


#Intro: instrucciones
col1, col2 = st.columns(2)

with col1:
    st.markdown("Reescribe tu texto en diferentes estilos.")

with col2:
    st.write("Contacte con [Matias Toro Labra](https://www.linkedin.com/in/luis-matias-toro-labra-b4074121b/) para construir sus proyectos de IA")


#Introducir la clave API de OpenAI
st.markdown("## Introduzca su clave API de OpenAI")

def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()


# Entrada
st.markdown("## Introduzca el texto que desea reescribir")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Su texto...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Por favor, introduzca un texto más corto. La longitud máxima es de 700 palabras.")
    st.stop()

# Opciones de ajuste de la plantilla
col1 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        '¿Qué tono quiere que tenga su redacción??',
        ('Formal', 'Informal'))
    
# Salida
st.markdown("### Su texto reescrito:")

if draft_input:
    if not openai_api_key:
        st.warning('Introduzca su OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_draft = prompt.format(
        tone=option_tone, 
        draft=draft_input
    )

    improved_redaction = llm(prompt_with_draft)

    st.write(improved_redaction)
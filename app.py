from flask import Flask,render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from utils import carga
from persona import personas, analizar_sentimiento

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
modelo = "gemini-2.5-flash"   
genai.configure(api_key=api_key)

app = Flask(__name__)
app.secret_key = 'bootcampdatalat'

contexto = carga("datos/musicmagic.txt")

def bot(prompt):
    #número máximo de intentos 
    max_intentos = 1
    repeticion = 0
    while True:
        try:
            personalidad = personas[analizar_sentimiento(prompt)]
            prompt_sistema = f"""
                                # PERSONA

                                Eres un chatbot de atención al cliente de una e-commerce. No debes
                                responder preguntas que no sean referentes a los datos del ecommerce 
                                informado.

                                Únicamente debes de utilizar los datos que estén dentro del 'contexto'.

                                # CONTEXTO
                                {contexto}

                                # PERSONALIDAD
                                {personalidad}
                             """
            
            
            configuracion_modelo = {
                "temperature":0.2,
                "max_output_tokens": 8192 
            }#8192 es el máximo para Gemini 2.5 es el número máximo de tokens que se pueden generar en una sola respuesta.
            #temperature controla la aleatoriedad de las respuestas generadas por el modelo. Un valor más bajo (cercano a 0) hace que las respuestas sean más determinísticas y coherentes, mientras que un valor más alto (cercano a 1) introduce más variabilidad y creatividad en las respuestas.

            llm = genai.GenerativeModel(
                model_name = modelo,
                system_instruction = prompt_sistema,
                generation_config = configuracion_modelo   
            )

            respuesta = llm.generate_content(prompt)
            return respuesta.text
        
        except Exception as e:
            repeticion += 1
            if repeticion >= max_intentos:
                return "Error con Gemini: %s" % e
            sleep(50)


@app.route("/chat", methods=["POST"]) #Estamos creando la ruta hacia el endpoint /chat que va a invocar el metodo POST 
def chat():
    prompt = request.json["msg"]
    respuesta = bot(prompt)
    return respuesta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
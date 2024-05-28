from flask import Flask, render_template, request
from .src.escenarios import search
from dotenv import load_dotenv
from decouple import config
import os


conversation = []

def init_app():
    # Carga las variables de entorno
    load_dotenv()

    app = Flask(__name__)
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    api_key = app.config.get('OPENAI_API_KEY')

    @app.route('/')
    def home():
        return render_template('inicio.html')

    @app.route('/asistente_elicitacion')
    def asistente_elicitacion():
        return render_template('asistente.html')

    @app.route('/analisis_escenarios', methods=['GET', 'POST'])
    def analisis_escenarios():
        if request.method == 'GET':
            return render_template('escenarios.html')
        
        if request.form['input']:
            question = 'Yo: '+ request.form['input']
            answer = 'IA: '+ search(question, api_key)
            
            conversation.append(question)
            conversation.append(answer)
            
            return render_template('escenarios.html', chat = conversation)
        else:
            return render_template('escenarios.html')
    
    return app
import os
from app.api_info import OpenAIClient
from app.src.elicitacion import consult, create_thread
from flask import Flask, jsonify, render_template, request, session
from .src.escenarios import search



conversation = []

def init_app(Debug=False):
    
    secret_key_hex = os.urandom(24).hex()

    app = Flask(__name__)
    app.secret_key = secret_key_hex


    @app.route('/')
    def home():
        return render_template('inicio.html')

        
    @app.route('/chat', methods=['POST'])
    def chat():
        openAI = OpenAIClient()
        client = openAI.get_client()

        if 'THREAD_ID' not in session:
            session['THREAD_ID'] = create_thread(client).id

        user_message = request.json.get('message')
        response_json = consult(user_message, session['THREAD_ID'], openAI)
  
        return jsonify(response_json)


    @app.route('/asistente_elicitacion')
    def asistente_elicitacion():
        session.pop('THREAD_ID', None)

        return render_template('asistente.html')

    @app.route('/analisis_escenarios', methods=['GET', 'POST'])
    def analisis_escenarios():
        client = OpenAIClient().get_client
        
        if request.method == 'GET':
            return render_template('escenarios.html')
        
        if request.form['input']:
            question = 'Yo: '+ request.form['input']
            answer = 'IA: '+ search(question, client)
            
            conversation.append(question)
            conversation.append(answer)
            
            return render_template('escenarios.html', chat = conversation)
        else:
            return render_template('escenarios.html')
    
    return app
import json
import os
from flask import Flask, Response, current_app as app, render_template, request, session

from requerimentsapp.api_info import OpenAIClient
from requerimentsapp.src.openAIChat import consult, create_thread_elit, create_thread_req
from requerimentsapp.src.escenarios import search
import markdown
import markdown.extensions.fenced_code


conversation = []
openAI = OpenAIClient()
TEMP_FOLDER = 'temp'

def create_app():
    
    secret_key_hex = os.urandom(24).hex()
    app = Flask(__name__)
    app.secret_key = secret_key_hex
    
    # Realizado para pruebas
        # with app.app_context():
        #         from . import routes

    @app.route('/')
    def home():
        return render_template('inicio.html')


    @app.route('/upload_file', methods=['POST'])
    def upload_file():
        ASSIT_REQ_ID = openAI.get_requeriment_id()
        client = openAI.get_client()

        file = request.files['pdf']
        user_message = request.form['message']
        

        if 'THREAD_REQ_ID' not in session and file:
            if not os.path.exists(TEMP_FOLDER):
                os.makedirs(TEMP_FOLDER)

            temp_file_path = os.path.join(TEMP_FOLDER, file.filename)
            file.save(temp_file_path)

            session['THREAD_REQ_ID'] = create_thread_req(temp_file_path, user_message, client).id

            
        response = consult(user_message, session['THREAD_REQ_ID'], ASSIT_REQ_ID, client)


    
        os.remove(temp_file_path)

        response_json = json.dumps(response)
        return Response(response_json, status=200, mimetype='application/json')

    @app.route('/asistente_requerimientos')
    def asistente_requerimientos():
        session.pop('THREAD_REQ_ID', None)

        return render_template('requerimientos.html')


    @app.route('/chat', methods=['POST'])
    def chat():
        ASSIT_ELIT_ID = openAI.get_elicitation_id()
        client = openAI.get_client()
        
        user_message = request.json.get('message')

        if 'THREAD_ELI_ID' not in session:
            session['THREAD_ELI_ID'] = create_thread_elit(client).id

        response = consult(user_message, session['THREAD_ELI_ID'], ASSIT_ELIT_ID, client)

        response_json = json.dumps(response)
        return Response(response_json, status=200, mimetype='application/json')


    @app.route('/asistente_elicitacion')
    def asistente_elicitacion():
        session.pop('THREAD_ELI_ID', None)

        return render_template('elicitacion.html')

    @app.route('/analisis_escenarios', methods=['GET', 'POST'])
    def analisis_escenarios():
        client = openAI.get_client()
        
        if request.method == 'GET':
            return render_template('escenarios.html')
        
        if request.form['input']:
            question = request.form['input']
            answer = search(question, client)
            answer_decode = markdown.markdown(answer, extensions=['fenced_code'])
            
            conversation.append(question)
            conversation.append(answer_decode)
            
            return render_template('escenarios.html', chat = conversation)
        else:
            return render_template('escenarios.html')
    
    return app
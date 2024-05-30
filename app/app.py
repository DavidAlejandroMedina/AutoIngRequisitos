from flask import Flask,Response, jsonify, render_template, request, session
from .src.escenarios import search
from dotenv import load_dotenv
from decouple import config
from app.api_info import OpenAIClient
from app.src.elicitacion import consult, create_thread
from werkzeug.utils import secure_filename
from .src.pdf import allow_extensions, pdf_plus_question
import os


conversation = []

def init_app(Debug=False):
    
    secret_key_hex = os.urandom(24).hex()

    app = Flask(__name__)
    app.secret_key = secret_key_hex
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    api_key = app.config.get('OPENAI_API_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

    @app.route('/')
    def home():
        return render_template('inicio.html')

        
    @app.route('/chat', methods=['POST'])
    def chat() -> Response:
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

        return render_template('elicitacion.html')

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
        
    @app.route('/cargar_archivo', methods=['GET','POST'])
    def cargar_archivo():
        if request.method=='GET':
            return render_template('Pdf.html')
        
        if request.method == 'POST' and not('file' in request.files):
            
            file = request.files['file']
            #print(file)
            
            # Chekeo que se seleccione un archivo
            if file.name == '':
                print('Archivo no seleccionado')
                return redirect(request.url)
            
            print(f'Nombre archivo: {file.filename}\nRetorno funcion: {allow_extensions(file.filename)}')

            # Guarda el archivo
            fileName = ''
            if file and allow_extensions(file.filename):
                fileName = secure_filename(file.filename)
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']),exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))

            if fileName != '':
                question = 'Yo: '+ request.form['input']
                answer = 'IA: '+ pdf_plus_question(path=os.path.join(app.config['UPLOAD_FOLDER']),pdf=fileName,question=request.form['input'],api_key=api_key)
            
            return redirect(request.url)
        elif request.form['input']:
            # Integrar consulta solo por promt
            pass 
        else:
            return redirect(request.url)
    
    return app
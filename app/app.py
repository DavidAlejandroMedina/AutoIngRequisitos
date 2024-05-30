from flask import Flask, render_template, request, redirect
from .src.escenarios import search
from dotenv import load_dotenv
from decouple import config
from werkzeug.utils import secure_filename
from .src.pdf import allow_extensions, pdf_plus_question
import os


conversation = []

def init_app():
    # Carga las variables de entorno
    load_dotenv()

    app = Flask(__name__)
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    api_key = app.config.get('OPENAI_API_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

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
        
    @app.route('/cargar_archivo', methods=['GET','POST'])
    def cargar_archivo():
        if request.method=='GET':
            return render_template('Pdf.html')
        
        if request.method == 'POST':
            # Chekeo que exista el archivo
            if not('file' in request.files):
                print('No se subio el archivo')
                return redirect(request.url)
            
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
        else:
            return redirect(request.url)
    
    return app
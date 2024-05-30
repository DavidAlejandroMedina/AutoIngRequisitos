from decouple import config
from openai import OpenAI
import PyPDF2

valid_extension = ['pdf']

def allow_extensions(fileName):
    return '.' in fileName and fileName.rsplit('.',1)[1].lower() in valid_extension

def read_pdf(pdf_file: str) -> str:

    """
        Se le da un archivo pdf, lee el arcivo y retorna un String con el contenido del archivo

        Parameters:
            pdf_file (str): Ruta con el archivo pdf
        
        returns:
            text (str): Contenido del pdf
    """
    try:
        pdf_file_object = open(pdf_file,'rb') # Se abre el archivo como binario
    except:
        return None

    pdf_reader = PyPDF2.PdfReader(pdf_file_object) # Lib PyPDF2 lee el archivo pdf
    #num_pages = len(pdf_reader.pages) # Extrae el numero de paginas

    text = ''

    for page in pdf_reader.pages:
        text+= page.extract_text() + '\n\n' # extrae el texto

    pdf_file_object.close()

    return text

def pdf_plus_question(path: str, pdf: str, question: str, api_key):
    # Se crea el cliente de OpenAI
    cliente = OpenAI(api_key=api_key)

    # Se define el rol del sistema
    messages=[
            {"role": "system", "content": "You are an software engineer that is specialized in requirements documentation. A coworker needs your help answering some questions related to a text, you will answer the questions using your sofware requirements knowlage and expirence"}
    ]

    # Se extrae la informacion del PDF
    text=read_pdf(f'{path}/{pdf}')
    if text is None:
        return 'Error archivo'

    # user_msg = "Nombre del documento:" + pdf + "\ncontenido:\n" text + "Del documento anterior " + question

    # prompt = {"role": "user", "content": user_msg}
    # messages.append(prompt)
    
    # answer = cliente.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=messages,
    #     max_tokens=150,
    #     temperature=1,
    #     n=1,
    #     stop=None,
    #     timeout=None
    # )

    # # Devuelve la respuesta generada por la API
    # return answer.choices[0].message.content
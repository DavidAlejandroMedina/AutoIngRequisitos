import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

class OpenAIClient:
    _client = None
    _api_key =  os.getenv('OPENAI_API_KEY')
    _elicitation_id = os.getenv('ELICITATION_ASSIST_ID')
    _requeriment_id = os.getenv('REQUERIMENT_ASSIST_ID')


    def __init__(self):
        if not self._api_key:
            raise ValueError("Clave de API no encontrada.")
        
        self._client = OpenAI(api_key=self._api_key)

    def get_client(self):
        return self._client
    
    def get_elicitation_id(self):
        return self._elicitation_id
    
    def get_requeriment_id(self):
        return self._requeriment_id
    



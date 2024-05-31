from typing import Any, Generator
from flask import json
from flask.testing import FlaskClient
import os
import pytest
import tempfile
from unittest.mock import MagicMock
from requerimentsapp import create_app
from requerimentsapp.src.openAIChat import consult

@pytest.fixture
def client() -> Generator[FlaskClient, Any, None]:
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_consult_successful_response(mocker):
    mock_openai = MagicMock()
    mocker.patch('requerimentsapp.api_info.OpenAIClient', return_value=mock_openai)

    mock_client = MagicMock()
    mock_openai.get_client.return_value = mock_client

    mock_thread = MagicMock()
    mock_thread.id = 'mock_thread_id'

    mock_assist = MagicMock()
    mock_assist.id = 'mock_assist_id'

    mock_message = MagicMock()
    mock_message.role = 'assistant'
    mock_message.content[0].text.value = 'This is the assistant response'

    
    mock_messages = MagicMock()
    mock_messages.data = [mock_message]

    mock_run = MagicMock()
    mock_run.status = 'completed'
    
    mock_client.beta.threads.create.return_value = mock_thread
    mock_client.beta.threads.messages.create.return_value = mock_message
    mock_client.beta.threads.runs.create_and_poll.return_value = mock_run
    mock_client.beta.threads.messages.list.return_value = mock_messages

    response = consult("Hello", 'mock_thread_id', "mock_assit_id", mock_openai.get_client.return_value)

    assert response == {'message': 'This is the assistant response'}

def test_consult_unsuccessful_response(mocker):
    mock_openai = MagicMock()
    mocker.patch('requerimentsapp.api_info.OpenAIClient', return_value=mock_openai)

    mock_client = MagicMock()
    mock_openai.get_client.return_value = mock_client

    mock_thread = MagicMock()
    mock_thread.id = 'mock_thread_id'

    mock_assist = MagicMock()
    mock_assist.id = 'mock_assist_id'

    mock_run = MagicMock()
    mock_run.status = 'failed'

    mock_client.beta.threads.create.return_value = mock_thread
    mock_client.beta.threads.runs.create_and_poll.return_value = mock_run

    response = consult("Hello", 'mock_thread_id', 'mock_assist_id', mock_openai.get_client.return_value)

    assert response == {'message': f'No he logrado responder a la pregunta\n (Error:{mock_run.status})'}


def test_upload_file(client: FlaskClient):
    TEMP_FOLDER = 'temp'

    with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_pdf:
        temp_pdf.write(b'mock pdf content')
        temp_pdf.seek(0)

        data = {
            'message': 'Solo escribe el la extension del archivo',
            'pdf': (temp_pdf, 'test.pdf')
        }

        response = client.post('/upload_file', data=data, content_type='multipart/form-data')

        assert response.status_code == 200
        
        response_data = json.loads(response.data)
        assert response_data['message'] == 'pdf'

        temp_file_path = os.path.join(TEMP_FOLDER, 'test.pdf')
        assert os.path.exists(temp_file_path)

 

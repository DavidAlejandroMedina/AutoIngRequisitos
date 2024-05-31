from decouple import config
from openai import OpenAI


def search(question, client):
    
    messages=[
            {"role": "system", "content": "You are an expert in technologies, such as web portal optimization and other web application features. You analyze the possible scenarios to implement a good project and name resources that could help in the construction of a web portal."}
    ]
    
    prompt = {"role": "user", "content": question}
    messages.append(prompt)
    
    answer = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        temperature=1,
        n=1,
        stop=None,
        timeout=None
    )
    
    # Devuelve la respuesta generada por la API
    return answer.choices[0].message.content
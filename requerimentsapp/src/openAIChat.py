def create_thread_elit(client):
    return client.beta.threads.create()

def create_thread_req(file, user_message, client):
    message_file = client.files.create(
    file=open(file, "rb"), 
    purpose="assistants")


    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": user_message,
                "attachments": [
                    { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
                ],
            }
        ]
    )

    return thread


def consult(user_message, thread_id, assistant_id, client):
    
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please address the user as Dev"
    )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        for message in messages.data:
            if message.role == 'assistant':
                assistant_answer = message.content[0].text.value
                break
    else:
        assistant_answer = f'No he logrado responder a la pregunta\n (Error:{run.status})'

    return {'message': assistant_answer}
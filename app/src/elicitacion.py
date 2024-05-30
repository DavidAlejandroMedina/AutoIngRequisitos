def create_thread(client):
    return client.beta.threads.create()

def consult(user_message, thread_id, openAI):
    client = openAI.get_client()
    assistant_id = openAI.get_elicitation_id()

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
        assistant_answer = 'No he logrado responder a la pregunta\n (Error:{run.status})'

    return {'message': assistant_answer}
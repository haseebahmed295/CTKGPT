
import g4f
import os
import json
import time

def process_gpt_request(prompt_text):
    # g4f.debug.logging = True # Enable debug logging
    # g4f.debug.version_check = False # Disable automatic version checking

   # Load the chat history from the file
    try:
    # Try to load the chat history from the file
        if os.path.exists('chat_history.json') and os.path.getsize('chat_history.json') > 0:
            with open('chat_history.json', 'r') as f:
                chat_history = json.load(f)
        else:
            chat_history = []
    except json.JSONDecodeError:
    # If there's an error decoding the JSON, start with an empty list
        chat_history = []

   # Prepare the messages array for the GPT API
    messages = []
    for item in chat_history:
        messages.append({"role": "user", "content": item['prompt']})
        messages.append({"role": "assistant", "content": item['response']})
    messages.append({"role": "user", "content": prompt_text})

    # Using automatic a provider for the given model
    ## Streamed completion
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )
    full_response = []
    for message in response:
        yield message
        full_response.append(message)
    
    full = ''.join(full_response)
        # time.sleep(0.1) # Simulate delay between chunks
    chat_history.append({
        'prompt': prompt_text,
        'response': full
    })

    # Save the updated chat history to the file
    with open('chat_history.json', 'w') as f:
        json.dump(chat_history, f)

def detect_python_code(text):
    is_code = False
    if '```' in text:
        is_code = not is_code
    return is_code
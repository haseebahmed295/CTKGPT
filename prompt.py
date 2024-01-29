
import re
import g4f
import os
import json

from bubbles import BotBubble

def process_gpt_request(prompt_text , model):
    # g4f.debug.logging = True # Enable debug logging
    # g4f.debug.version_check = False # Disable automatic version checking

   # Load the chat history from the file
    try:
    # Try to load the chat history from the file
        if os.path.exists('prefs/chat_history.json') and os.path.getsize('prefs/chat_history.json') > 0:
            with open('prefs/chat_history.json', 'r') as f:
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
        model=model,
        messages=messages,
        stream=True,
    )
    print(response)
    # if model.supports_stream:
    full_response = []
    for message in response:
        yield message
        full_response.append(message)
    # else:
    #     return [{"prompt": prompt_text, "response": response}]
    

    chat_history.append({
        'prompt': prompt_text,
        'response': "".join(full_response), # full_response
    })

    # Save the updated chat history to the file
    with open('prefs/chat_history.json', 'w') as f:
        json.dump(chat_history, f)

def clear_chat_history():
    try:
        # Read existing data from the file
        with open('prefs/chat_history.json', 'r') as f:
            data = json.load(f)

        # Check if the file is empty
        if not data:
            print("No chat history")
            return

        # Remove all items from the data list
        data.clear()

        # Write the updated data back to the file
        with open('prefs/chat_history.json', 'w') as f:
            json.dump(data, f)

    except FileNotFoundError:
        # If the file doesn't exist, write an empty list to it
        with open('prefs/chat_history.json', 'w') as f:
            json.dump([], f)
        print("No chat history")
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON")

def insert_text(app, item:iter):
    right = BotBubble(app, app.chat_frame, "right")
    right_index = right.add_text_box()
    right.text_boxes[right_index].insert("end", f'{item["prompt"]}')
    right.adjust_text_box(right.text_boxes[right_index])

    left = BotBubble(app, app.chat_frame, "left")
    text_blocks = find_code_and_text_segments(item['response'])
    for block in text_blocks:
        if len(block[0]) == 0:
            continue

        if not block[1]:
            c = left.add_text_box()
            left.text_boxes[c].insert("end", f'{block[0]}')
            left.adjust_text_box(left.text_boxes[c])
        else:
            c = left.add_code_box(block[2])
            left.text_boxes[c].insert("end", f'{block[0]}')
            left.adjust_text_box(left.text_boxes[c])
            left.colorizers[c].update()

def find_code_and_text_segments(text):
    """
    Returns a list of tuples, each containing a segment of the text, a boolean
    indicating whether it is a code block, and the language name if it is a code block.

    Parameters:
    text (str): The string containing potential code blocks.

    Returns:
    list: A list of tuples with each containing a segment of text, a boolean,
          and the language name (str or None).
    """
    # Regular expression pattern to find code blocks with any language
    pattern = r"```(\w+)?\s(.*?)```"
    # Find all matches and their positions
    matches = list(re.finditer(pattern, text, flags=re.DOTALL))
    last_idx = 0
    segments = []

    for match in matches:
        # Get text before the code block
        start, end = match.span()
        non_code = text[last_idx:start]
        if non_code:
            segments.append((non_code, False, None))
        
        # Get the code block
        lang = match.group(1) or "plaintext"  # Default to plaintext if no language is specified
        code = match.group(2)
        segments.append((code, True, lang))
        
        last_idx = end
    
    # Get any remaining text after the last code block
    if last_idx < len(text):
        segments.append((text[last_idx:], False, None))
    
    return segments
import json
import os
import requests
import time

def process_gpt_request(prompt_text, api_key="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"):
  if api_key:
      # Load the chat history from the file
      if os.path.exists('chat_history.json') and os.path.getsize('chat_history.json') > 0:
          with open('chat_history.json', 'r') as f:
             chat_history = json.load(f)
      else:
          chat_history = []

      # Prepare the messages array for the GPT API
      messages = []
      for item in chat_history:
          messages.append({"role": "user", "content": item['prompt']})
          messages.append({"role": "assistant", "content": item['response']})
      messages.append({"role": "user", "content": prompt_text})

      payload = {
          "model": "gpt-3.5-turbo",
          "messages": messages
      }

      headers = {
          "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
      }

      response = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)


      if response.status_code == 200:
          advice = response.json()['choices'][0]['message']['content']

          # Append the new prompt and response to the chat history
          chat_history.append({
              'prompt': prompt_text,
              'response': advice
          })

          # Save the updated chat history to the file
          with open('chat_history.json', 'w') as f:
              json.dump(chat_history, f)

          # Simulate streaming by yielding chunks of the response
          chunk_size = 50 # Define the size of each chunk
          for i in range(0, len(advice), chunk_size):
              yield advice[i:i+chunk_size]
              time.sleep(0.1) # Simulate delay between chunks

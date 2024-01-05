
import re

def find_text_in_pattern(input_string):
    # Define the pattern to match text within triple backticks
    pattern = r'```(.*?)```'
    
    # Find all matches using the re.finditer() method
    matches = re.finditer(pattern, input_string)
    
    # Iterate over the matches and print the text and indices
    for match in matches:
        text = match.group(1)  # Extract the text within the backticks
        start_index = match.start(1)  # Get the starting index of the captured group
        end_index = match.end(1)  # Get the ending index of the captured group
        print(f'Text: {text}, Start Index: {start_index}, End Index: {end_index}')

# Example usage
input_string = "Here is some code: \n```python\nHello, World!``` and here is more code: ```x = 5```"
find_text_in_pattern(input_string)
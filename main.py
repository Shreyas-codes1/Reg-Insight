from acts import acts
from rules import rules
from forms import forms
from regulations import regulations

from flask import Flask, jsonify
import concurrent.futures
import os

app = Flask(__name__)

def run_function(func):
    """Runs a function."""
    func()  # Assume each function writes its output to a file

def combine_files():
    """Combines the contents of the text files into a single file."""
    file_names = ['acts.txt', 'rules.txt', 'forms.txt', 'regulations.txt']
    combined_file_name = 'combined_text.txt'

    with open(combined_file_name, 'w') as combined_file:
        for file_name in file_names:
            if os.path.exists(file_name):
                with open(file_name, 'r') as file:
                    content = file.read()
                    combined_file.write(f'Content from {file_name}:\n{content}\n\n')
            else:
                combined_file.write(f'Output file {file_name} not found.\n\n')

@app.route('/combine', methods=['GET'])
def run_combine_files():
    """Executes the functions in parallel and combines the results into a single file."""
    functions = [acts, rules, forms, regulations]
    function_names = ['acts', 'rules', 'forms', 'regulations']

    # Execute functions in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_function, func) for func in functions]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Check if there were any exceptions
            except Exception as exc:
                print(f'An error occurred: {exc}')

    # Combine the outputs into a single file
    combine_files()

    return jsonify({"message": "Functions executed and results combined successfully."})

if __name__ == '__main__':
    app.run(debug=True)

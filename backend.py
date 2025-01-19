from flask import Flask, jsonify
from flask_cors import CORS
from nbconvert import PythonExporter
import nbformat

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and origins by default

@app.route('/run_notebook', methods=['GET'])
def run_notebook():
    # Load the notebook
    with open('hello_react.ipynb', 'r') as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Use nbconvert to export the notebook as a Python script
    exporter = PythonExporter()
    python_script, _ = exporter.from_notebook_node(notebook_content)

    # Execute the Python script or any part of the notebook here
    exec(python_script)

    # Return the result (you may adjust depending on your notebook's output)
    return jsonify({"message": "Notebook executed successfully"})

if __name__ == '__main__':
    app.run(debug=True)

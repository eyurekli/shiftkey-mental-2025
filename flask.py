from flask import Flask, jsonify
import nbformat
from jupyter_client import KernelManager

app = Flask(__name__)

@app.route('/run_notebook', methods=['GET'])
def run_notebook():
    # Load the Jupyter notebook
    with open('your_notebook.ipynb') as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Initialize Jupyter kernel manager to execute the notebook
    km = KernelManager()
    km.start_kernel()
    kc = km.connect_shell()

    # Execute the notebook cell by cell (this is a simplified version)
    for cell in notebook_content.cells:
        if cell.cell_type == 'code':
            code = cell.source
            msg_id = kc.execute(code)
            reply = kc.get_shell_msg(msg_id)
            # Collect the output (You can extract it here)
            output = reply.get('content', {}).get('text', '')
            print(output)  # You can send this output to the frontend

    km.shutdown_kernel()

    return jsonify({"message": "Notebook executed successfully", "output": output})

if __name__ == "__main__":
    app.run(debug=True)

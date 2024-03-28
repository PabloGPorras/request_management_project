from flask import Flask, render_template, request, redirect, url_for, jsonify
from models.model import Model
from models.modelBuilder import ModelBuilder
from database.engine import getEngine, getSession
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model_editor', methods=['GET', 'POST'])
def model_editor():
    if request.method == 'POST':
        # Process form data
        table_name = request.form.get('table_name')
        table_columns = json.loads(request.form.get('table_columns'))

        model_builder = ModelBuilder()
        with getSession() as session:
            model = Model(model_name=table_name, model_json=json.dumps(table_columns))
            session.add(model)
            session.commit()
            table = model_builder.createModel(model)

        return redirect(url_for('index'))
    else:
        return render_template('model_editor.html')

if __name__ == '__main__':
    app.run(debug=True)

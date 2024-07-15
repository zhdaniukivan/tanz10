from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{DATABASE_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FormData(db.Model):
    __tablename__ = 'form_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(JSONB)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """
    Handle the main form page. Display the form and handle form submission.

    Returns:
        str: Rendered HTML template.
    """
    if request.method == 'POST':
        form_data = {key: value for key, value in request.form.items() if key.startswith('input')}
        print(f"Received form data: {form_data}")  # Отладочное сообщение
        new_entry = FormData(data=form_data)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('data'))
    return render_template('index.html')

@app.route('/data')
def data() -> str:
    """
    Display the submitted form data.

    Returns:
        str: Rendered HTML template with submitted data.
    """
    entries = FormData.query.all()
    return render_template('data.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)

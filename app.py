from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from models import db, ImageData
import os

app = Flask(_name_, instance_relative_config=True)

# Asegurar que el directorio instance exista
os.makedirs(app.instance_path, exist_ok=True)

# Configuración de base de datos según entorno
if os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'local.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    image_data = ImageData(
        filename=data['filename'],
        red_count=data['redCount'],
        green_count=data['greenCount'],
        blue_count=data['blueCount'],
        timestamp=data['timestamp'],
        username=data['username']
    )
    db.session.add(image_data)
    db.session.commit()
    return jsonify({'message': 'Datos guardados correctamente'}), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    data = ImageData.query.order_by(ImageData.timestamp.desc()).all()
    return jsonify([{
        'filename': d.filename,
        'redCount': d.red_count,
        'greenCount': d.green_count,
        'blueCount': d.blue_count,
        'timestamp': d.timestamp,
        'username': d.username
    } for d in data])

@app.route('/')
def index():
    return render_template('index.html')

if _name_ == '_main_':
    app.run(debug=True)
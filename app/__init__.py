from flask import Flask
from config import get_config
from flask_cors import CORS

def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(get_config())
    
    # Autoriser CORS pour le front-end Vercel
    CORS(app, origins=["https://smart-agro-three.vercel.app"], supports_credentials=True)
    
    from flasgger import Swagger
    Swagger(app, template={
        "info": {
            "title": "Agriculture Cameroun API",
            "description": "API du Système Expert Agricole pour le Cameroun",
            "version": "1.0.0"
        }
    })

    # Initialisation des routes
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return "Système Multi-Agents Agriculture Cameroun - API Operational"

    return app

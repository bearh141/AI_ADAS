from flask import Flask

from app.routes.drowsy_router import drowsy_bp
from app.routes.sign_router import sign_bp
from app.routes.object_router import object_bp 
from app.routes.lane_router import lane_bp
from app.services.model_loader import load_models, loaded_models
from app.utils.warm_up_model import warmup_all

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(drowsy_bp, url_prefix="/drowsy")
    app.register_blueprint(sign_bp, url_prefix="/sign")
    app.register_blueprint(object_bp, url_prefix="/object") 
    app.register_blueprint(lane_bp, url_prefix="/lane")

    # Load models AI
    if not loaded_models:
        load_models()
        warmup_all()

    return app
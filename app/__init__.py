from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config')
    
    db.init_app(app)
    
    from app.views.main import main
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()
    
    return app

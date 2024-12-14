from flask import Flask
from models import db, User
from routes import routes  
from config import Config
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  

    db.init_app(app)  


    jwt = JWTManager(app)  

    app.register_blueprint(routes)  

    with app.app_context():
        db.create_all()  
        create_default_user()

    return app

def create_default_user():
    user = User.query.filter_by(username='admin').first()
    if not user:
        hashed_password = generate_password_hash('password')
        new_user = User(username='admin', password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print("Default user 'admin' created")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

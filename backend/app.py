from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-this-in-production'
    
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    
    from auth import auth_bp
    from bookmarks import bookmarks_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(bookmarks_bp, url_prefix='/api/bookmarks')
    
    with app.app_context():
        from models import User, Bookmark
        db.create_all()
        
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Bookmark Manager API"})
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

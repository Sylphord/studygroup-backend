import os
from flask import Flask
from extensions import db, bcrypt, jwt
import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
with app.app_context():
    db.engine.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        department VARCHAR(100),
        level VARCHAR(20)
    )""")
    db.engine.execute("""CREATE TABLE IF NOT EXISTS groups_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(150) NOT NULL,
        course VARCHAR(100),
        description TEXT,
        max_members INT DEFAULT 10,
        schedule VARCHAR(100),
        location VARCHAR(200),
        creator_id INT
    )""")
    db.engine.execute("""CREATE TABLE IF NOT EXISTS memberships (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        group_id INT
    )""")
    
from routes.auth import auth_bp
from routes.groups import groups_bp
from routes.memberships import memberships_bp

app.register_blueprint(auth_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(memberships_bp)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
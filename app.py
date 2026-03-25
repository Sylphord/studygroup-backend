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

from routes.auth import auth_bp
from routes.groups import groups_bp
from routes.memberships import memberships_bp

app.register_blueprint(auth_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(memberships_bp)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
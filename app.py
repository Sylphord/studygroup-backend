import os
from flask import Flask
from extensions import mysql, bcrypt, jwt
import config

app = Flask(__name__)

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY

mysql.init_app(app)
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
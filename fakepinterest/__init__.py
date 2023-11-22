from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
#a linha abaixo era pra usar bd local
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
#app.config["SQLALCHEMY_DATABASE_URI"] = postgresql://projeto_pinterest_user:7p0m1Sdq4Zjz1Oy8Tqc7A6BhhWEyH27l@dpg-clf280fjc5ks73dgu110-a.oregon-postgres.render.com/projeto_pinterest
# Para criar o bd la no Render
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") #essa linha é do bd postgresql do Render
app.config["SECRET_KEY"] = "36935f480034d7a10c5cb587ea7803f7"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fakepinterest import routes
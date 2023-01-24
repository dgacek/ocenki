from flask import Flask, jsonify, render_template, request
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.pool import StaticPool
from flask_cors import CORS


app = Flask(__name__, static_folder="public")
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
CORS(app, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "basic"

csrf = CSRFProtect(app)

db = declarative_base()

class Rating(db):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))
    
    user = relationship("User", back_populates="ratings")
    album = relationship("Album", back_populates="ratings")

    def __repr__(self) -> str:
        return '{"id": %i, "rating": "%i", "user_id": "%i", "album_id": "%i"}' % (self.id, self.rating, self.user_id, self.album_id)


class User(db):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    ratings = relationship("Rating", order_by=Rating.id, back_populates="user")

    def __repr__(self) -> str:
        return '{"id": %i, "username": "%s", "password": "%s"}' % (self.id, self.username, self.password)


class Album(db):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    spotify_uri = Column(String)
    ratings = relationship("Rating", order_by=Rating.id, back_populates="album")

    def __repr__(self) -> str:
        return '{"id": %i, "spotify_uri": "%s"}' % (self.id, self.spotify_uri)
    

engine = create_engine("sqlite:///:memory:", echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)
# engine = create_engine("sqlite:///database.db", echo=True)
db.metadata.create_all(engine)
dbsession = sessionmaker(bind=engine)

# create test user
test_user = User(username="test", password="test")
session = dbsession()
session.add(test_user)
session.commit()


class SessionUser(UserMixin):
    ...


def get_user(user_id: int):
    session = dbsession()
    for user in session.query(User).filter_by(id=user_id):
        return user
    return None


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        user_model = SessionUser()
        user_model.id = user.id
        return user_model
    return None


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def home(path):
    return render_template("index.html")


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    session = dbsession()

    for user in session.query(User).filter_by(username=username, password=password):
        user_model = SessionUser()
        user_model.id = user.id
        login_user(user_model, remember=True)
        return jsonify({"login": True})

    return jsonify({"login": False})


@app.route("/api/data", methods=["GET"])
@login_required
def user_data():
    user = get_user(current_user.id)
    return jsonify({"username": user.username})


@app.route("/api/getsession")
def check_session():
    if current_user.is_authenticated:
        return jsonify({"login": True})

    return jsonify({"login": False})


@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"logout": True})


if __name__ == "__main__":
    app.run(debug=True, load_dotenv=True)

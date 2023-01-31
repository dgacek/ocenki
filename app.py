import base64, datetime, requests
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
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.pool import StaticPool
from flask_cors import CORS
from passlib.hash import sha512_crypt

crypt_salt = "menpwgra"
spotify_client_id = "88acafcfdefa48ff962c05ad0df9bcb5"
spotify_client_secret = "60475eb74e474702bbb80564b88b480f"

class SpotifyToken:
    def __init__(self, token, expiry_date):
        self.token = token
        self.expiry_date = expiry_date


spotify_token = SpotifyToken("", datetime.datetime.now())

def get_spotify_token(current_token):
    if current_token.token == "" or datetime.datetime.now() > current_token.expiry_date:
        auth_input = spotify_client_id + ":" + spotify_client_secret
        auth_string = base64.b64encode(auth_input.encode("ascii")).decode("ascii")
        data = requests.post("https://accounts.spotify.com/api/token", 
        data={
            "grant_type": "client_credentials"
        }, 
        headers={
            "Authorization": "Basic " + auth_string,
            "Content-Type": "application/x-www-form-urlencoded"
        })
        response = data.json()
        expires_in = response["expires_in"]
        return SpotifyToken(response["access_token"], datetime.datetime.now() + datetime.timedelta(seconds=expires_in))
    return current_token


spotify_token = get_spotify_token(spotify_token)

crypt = sha512_crypt(salt=crypt_salt, rounds=656000)

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
    album_spotify_id = Column(String)
    
    user = relationship("User", back_populates="ratings")
    Index("ratings:album_spotify_id", album_spotify_id)

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
    

engine = create_engine("sqlite:///:memory:", echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)
# engine = create_engine("sqlite:///database.db", echo=True)
db.metadata.create_all(engine)
dbsession = sessionmaker(bind=engine)

# create test user
test_user = User(username="test", password=crypt.hash("test"))
test_rating = Rating(album_spotify_id="2wy9EzWP9NuyVt4TSCz3qs", rating=69, user=test_user)
session = dbsession()
session.add(test_user)
session.add(test_rating)
session.commit()


def get_average_rating(spotify_album_id):
    rating_sum = 0
    rating_count = 0
    session = dbsession()
    for instance in session.query(Rating).filter(Rating.album_spotify_id == spotify_album_id):
        rating_sum += instance.rating
        rating_count += 1
    
    if rating_count > 0:
        return int(rating_sum/rating_count)

    return -1


def get_ratings_count(spotify_album_id):
    return session.query(Rating).filter(Rating.album_spotify_id == spotify_album_id).count()


def get_current_user_rating(spotify_album_id, current_user_id):
    session = dbsession()
    for instance in session.query(Rating).filter(Rating.album_spotify_id == spotify_album_id, Rating.user_id == current_user_id):
        return instance.rating

    return -1


def append_ratings(search_output, current_user_id):
    result = search_output
    for x in range(len(search_output["albums"]["items"])):
        result["albums"]["items"][x]["average_rating"] = get_average_rating(search_output["albums"]["items"][x]["id"])
        result["albums"]["items"][x]["ratings_count"] = get_ratings_count(search_output["albums"]["items"][x]["id"])
        result["albums"]["items"][x]["current_user_rating"] = get_current_user_rating(search_output["albums"]["items"][x]["id"], current_user_id)

    return result


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

    for user in session.query(User).filter_by(username=username):
        if crypt.verify(password, user.password):
            user_model = SessionUser()
            user_model.id = user.id
            login_user(user_model, remember=True)
            return jsonify({"login": True})

    return jsonify({"login": False})


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    session = dbsession()

    for user in session.query(User).filter_by(username=username):
        return jsonify({"register": False})

    user = User(username=username, password=crypt.hash(password))
    session.add(user)
    session.commit()
    return jsonify({"register": True})


@app.route("/api/data", methods=["GET"])
@login_required
def user_data():
    user = get_user(current_user.id)
    return jsonify({"username": user.username})


@app.route("/api/search", methods=["GET"])
@login_required
def search():
    query = request.args["q"]
    response = requests.get("https://api.spotify.com/v1/search?q="+query+"&type=album", headers={"Authorization": "Bearer "+get_spotify_token(spotify_token).token})
    return append_ratings(response.json(), current_user.id)


@app.route("/api/rate", methods=["POST"])
@login_required
def create_rating():
    data = request.json
    album_id = data.get("album_id")
    rating = data.get("rating")
    session = dbsession()
    session.add(Rating(album_spotify_id=album_id, user_id=current_user.id, rating=rating))
    session.commit()
    return jsonify({"average_rating": get_average_rating(album_id), "ratings_count": get_ratings_count(album_id), "current_user_rating": rating})


@app.route("/api/rate", methods=["PATCH"])
@login_required
def update_rating():
    data = request.json
    album_id = data.get("album_id")
    rating = data.get("rating")
    session = dbsession()
    record = session.query(Rating).filter_by(user_id=current_user.id, album_spotify_id=album_id).first()
    record.rating = rating
    session.commit()
    return jsonify({"average_rating": get_average_rating(album_id), "ratings_count": get_ratings_count(album_id), "current_user_rating": rating})


@app.route("/api/getsession")
def check_session():
    if current_user.is_authenticated:
        user = get_user(current_user.id)
        return jsonify({"login": True, "username": user.username})

    return jsonify({"login": False})


@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"logout": True})


if __name__ == "__main__":
    app.run(debug=True, load_dotenv=True, host="0.0.0.0")

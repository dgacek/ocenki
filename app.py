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
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
from flask_socketio import SocketIO


app = Flask(__name__, static_folder="public")
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

csrf = CSRFProtect(app)
socketio = SocketIO(app)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self) -> str:
        return '{"id": %i, "username": "%s", "password": "%s"}' % (self.id, self.username, self.password)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    fromUserId = Column(Integer)
    toUserId = Column(Integer)
    text = Column(String)
    date = Column(DateTime)

    def __repr__(self) -> str:
        return '{"id": %i, "fromUserId": %i, "toUserId": %i, "text": "%s", "date": "%s"}' % (self.id, self.fromUserId, self.toUserId, self.text, str(self.date))


engine = create_engine("sqlite:///:memory:", echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# create test user
test_user = User(username="test", password="test")
session = Session()
session.add(test_user)
session.commit()
session.close()


class SessionUser(UserMixin):
    ...


def get_user(user_id: int):
    session = Session()
    for user in session.query(User).filter_by(id=user_id):
        session.close()
        return user
    session.close()
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
    session = Session()

    for user in session.query(User).filter_by(username=username, password=password):
        user_model = SessionUser()
        user_model.id = user.id
        login_user(user_model)
        session.close()
        return jsonify({"login": True})

    session.close()
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
    socketio.run(app, debug=True, load_dotenv=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

def init_db():
    print("Creating DB with tables...")
    db.create_all()


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(512))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    options = db.Column(db.String(120))
    correct_option = db.Column(db.Integer)
    quiz = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    points = db.Column(db.Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

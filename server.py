from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from mailtrap import intercept_msg

import os 

app = Flask(__name__)

ENV = ""

if ENV == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kop.db"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('POSTGRESQL_DB')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, email, phone, dealer, rating, comments):
        self.customer = customer
        self.email = email
        self.phone = phone
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        customer = request.form["customer"]
        email = request.form["email"]
        phone = request.form["phone"]
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]

        if customer == "" or email == "" or phone == "":
            return render_template(
                "index.html", message="Please enter required fields"
            )
        if (
            db.session.query(Feedback)
            .filter(Feedback.customer == customer)
            .count()
            == 0
        ):
            data = Feedback(customer, email, phone, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            intercept_msg(customer, email, phone, dealer, rating, comments)
            return render_template("success.html")
        return render_template(
            "index.html", message="You have already submitted feedback"
        )


if __name__ == "__main__":
    app.run()

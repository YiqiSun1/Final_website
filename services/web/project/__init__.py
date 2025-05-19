import os
from sqlalchemy import func, text
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.from_object("project.config.Config")
app.secret_key = "super-secret-key"
db = SQLAlchemy(app)

@app.route('/')
def root():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    tweets = (
    Tweet.query
    .order_by(Tweet.created_at.desc())
    .options(db.joinedload(Tweet.user))  # eager-load user
    .paginate(page=page, per_page=20, error_out=False)
)

    return render_template(
        "home.html",
        tweets=tweets.items,
        page=page,
        has_next=tweets.has_next,
        has_prev=tweets.has_prev,
    )
from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("user_id"):
        return redirect(url_for("root"))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password")
            return render_template("login.html")

        session["user_id"] = user.id
        return redirect(url_for("root"))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("root"))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if session.get("user_id"):
        return redirect(url_for("root"))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash("Passwords do not match")
            return render_template("create_account.html")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists")
            return render_template("create_account.html")

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password1)
        )
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return redirect(url_for("root"))

    return render_template("create_account.html")

from datetime import datetime

@app.route('/create_message', methods=['GET', 'POST'])
def create_message():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    if request.method == 'POST':
        content = request.form.get('content')

        if not content or len(content.strip()) == 0:
            flash("Message cannot be empty")
            return render_template("create_message.html")

        tweet = Tweet(
            content=content.strip(),
            user_id=session["user_id"],
            created_at=datetime.utcnow()
        )
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for("root"))

    return render_template("create_message.html")

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 20

    results = []
    suggestions = []
    has_next = has_prev = False

    if query:
        # Prepare ts_query and rank
        ts_query = func.websearch_to_tsquery('english', query)

        base_query = (
            db.session.query(Tweet)
            .filter(text("content_tsv @@ websearch_to_tsquery('english', :q)"))
            .params(q=query)
            .add_columns(
                func.ts_rank_cd(Tweet.content_tsv, ts_query).label('rank')
            )
            .join(User)
            .add_columns(User.username)
            .order_by(text('rank DESC'))
        )

        paginated = base_query.limit(per_page).offset((page - 1) * per_page).all()
        results = paginated

        # Get spell suggestions using pg_trgm
        suggestion_query = db.session.execute(text("""
            SELECT word
            FROM ts_stat('SELECT to_tsvector(''english'', content) FROM tweets')
            WHERE word % :query
            ORDER BY similarity(word, :query) DESC
            LIMIT 5;
        """), {'query': query}).fetchall()

        suggestions = [row[0] for row in suggestion_query]

        # Check if there’s a next page
        has_next = len(paginated) == per_page
        has_prev = page > 1

    return render_template("search.html",
                           query=query,
                           results=results,
                           page=page,
                           has_next=has_next,
                           has_prev=has_prev,
                           suggestions=suggestions)

@app.template_filter('highlight')
def highlight(text, query):
    for word in query.split():
        text = text.replace(word, f"<mark>{word}</mark>")
    return text
@app.template_filter('highlight')
def highlight(text, query):
    for word in query.lower().split():
        text = text.replace(word, f"<mark>{word}</mark>")
        text = text.replace(word.capitalize(), f"<mark>{word.capitalize()}</mark>")
    return text

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    tweets = db.relationship('Tweet', backref='user', lazy=True)


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)    
    
 
 
# @app.route("/static/<path:filename>")
# def staticfiles(filename):
#     return send_from_directory(app.config["STATIC_FOLDER"], filename)
# 
# 
# @app.route("/media/<path:filename>")
# def mediafiles(filename):
#     return send_from_directory(app.config["MEDIA_FOLDER"], filename)
# 
# 
# @app.route("/upload", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         file = request.files["file"]
#         filename = secure_filename(file.filename)
#         print(f'app.config["MEDIA_FOLDER"] = {app.config["MEDIA_FOLDER"]}', flush=True)
#         file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
#     return """
#     <!doctype html>
#     <title>upload new File</title>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file><input type=submit value=Upload>
#     </form>
#     """

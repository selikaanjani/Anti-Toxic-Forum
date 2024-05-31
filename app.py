from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

from network import Tokenizer, Network
from config import Config

from db import db
import uuid


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)

tokenizer = Tokenizer()
network = Network()

from backend.schema import User, Comment
from backend.forms import LoginForm, SignUpForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=True, duration=timedelta(days=30))
                return redirect(url_for('index'))
            else:
                form.email.errors = ['Wrong credentials']
                form.password.errors = ['Wrong credentials']

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                form.email.errors = ['Email has been used']
            else:
                hashed_password = generate_password_hash(form.password.data)
                now = datetime.now()
                user = User(
                    id=uuid.uuid4(),
                    name=form.name.data,
                    email=form.email.data,
                    password=hashed_password,
                    created_at=now,
                    updated_at=now
                )
                db.session.add(user)
                db.session.flush()
                db.session.commit()
                return redirect(url_for('index'))

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('sign-up.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/post', methods=['GET'])
def get_posts():
    comments = Comment.query.order_by(Comment.created_at.asc()).all()
    data = []
    for comment in comments:
        data.append({
            "user": comment.user.name,
            "created_at": comment.created_at.isoformat(),
            "self": bool(comment.user_id == current_user.id),
            "message": comment.content,
            "toxicity_percentages": [round(comment.toxic, 2), round(comment.severe_toxic, 2), round(comment.obscene, 2), round(comment.threat, 2), round(comment.insult, 2), round(comment.identity_hate, 2)],
            "censored": comment.is_censored
        })

    return make_response(jsonify({"data": data}), 200)


@app.route('/post', methods=['POST'])
def create_post():
    data = request.json
    message = data['message']
    tokenized_message = tokenizer.tokenize([message])
    toxicity_values = network.predict(tokenized_message)[0]
    toxic, severe_toxic, obscene, threat, insult, identity_hate = [
        round(value * 100, 2) for value in toxicity_values]
    threshold = 0.5
    is_censored = bool(
        sum([value > threshold for value in toxicity_values]) > 0)
    now = datetime.now()
    comment = Comment(
        id=uuid.uuid4(),
        user_id=current_user.id,
        content=message,
        toxic=toxic,
        severe_toxic=severe_toxic,
        obscene=obscene,
        threat=threat,
        insult=insult,
        identity_hate=identity_hate,
        is_censored=is_censored,
        created_at=now,
        updated_at=now
    )
    db.session.add(comment)
    db.session.flush()
    db.session.commit()
    return make_response(jsonify({"success": True}), 200)


if __name__ == "__main__":
    app.run(debug=True)

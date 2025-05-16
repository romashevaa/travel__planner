from models import Post
from forms import PostForm
from models import Trip
from forms import TripForm
from forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import redirect, url_for, flash, request
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager
from models import User, Trip, Post  # імпортуй Post також


# Ініціалізація додатку
app = Flask(__name__)
app.config.from_object(Config)

# Підключення розширень
db.init_app(app)
login_manager.init_app(app)

# Завантаження користувача по id (обов’язково для Flask-Login)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Головна сторінка


@app.route('/')
def home():
    return render_template('base.html', title='Головна')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash('Користувач з таким email вже існує.', 'danger')
            return redirect(url_for('register'))
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Реєстрація успішна!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title='Реєстрація')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вхід виконано.', 'success')
            return redirect(url_for('home'))
        flash('Невірний email або пароль.', 'danger')
    return render_template('login.html', form=form, title='Вхід')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вихід виконано.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', trips=trips, title='Мої подорожі')


@app.route('/trip/create', methods=['GET', 'POST'])
@login_required
def create_trip():
    form = TripForm()
    if form.validate_on_submit():
        trip = Trip(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            owner=current_user
        )
        db.session.add(trip)
        db.session.commit()
        flash('Подорож створено!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_trip.html', form=form, title='Нова подорож')


@app.route('/trip/<int:trip_id>')
@login_required
def view_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.owner != current_user:
        flash('Доступ заборонено.', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('view_trip.html', trip=trip, title=trip.title)


@app.route('/trip/<int:trip_id>/blog', methods=['GET', 'POST'])
@login_required
def trip_blog(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.owner != current_user:
        flash('Доступ заборонено.', 'danger')
        return redirect(url_for('dashboard'))

    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, trip=trip, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Пост додано!', 'success')
        return redirect(url_for('trip_blog', trip_id=trip.id))

    posts = Post.query.filter_by(trip_id=trip.id).order_by(
        Post.timestamp.desc()).all()
    return render_template('trip_blog.html', trip=trip, posts=posts, form=form, title='Блог подорожі')


# Запуск сервера
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

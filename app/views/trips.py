from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Trip
from ..forms import TripForm
from ..extensions import db

trips_bp = Blueprint('trips', __name__)


@trips_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('trips.dashboard'))
    return redirect(url_for('trips.explore'))


@trips_bp.route('/dashboard')
@login_required
def dashboard():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', trips=trips)


@trips_bp.route('/trip/create', methods=['GET', 'POST'])
@login_required
def create_trip():
    form = TripForm()
    if form.validate_on_submit():
        trip = Trip(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_public=form.is_public.data,
            owner=current_user
        )
        db.session.add(trip)
        db.session.commit()
        return redirect(url_for('trips.dashboard'))
    return render_template('create_trip.html', form=form)


@trips_bp.route('/trip/<int:trip_id>')
def view_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    # Гість — заборона
    if not current_user.is_authenticated:
        flash('Авторизуйтесь, щоб переглянути повну подорож.', 'warning')
        return redirect(url_for('auth.login'))

    # Не власник — заборона
    if trip.owner != current_user:
        flash('Доступ заборонено.', 'danger')
        return redirect(url_for('trips.dashboard'))

    return render_template('view_trip.html', trip=trip)


@trips_bp.route('/explore')
def explore():
    trips = Trip.query.filter_by(is_public=True).order_by(
        Trip.start_date.desc()).all()
    return render_template('explore.html', trips=trips)

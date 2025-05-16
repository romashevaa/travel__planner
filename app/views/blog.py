from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Trip, Post
from ..forms import PostForm
from ..extensions import db

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/trip/<int:trip_id>/blog', methods=['GET', 'POST'])
@login_required
def trip_blog(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.owner != current_user:
        flash('Доступ заборонено.', 'danger')
        return redirect(url_for('trips.dashboard'))

    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, trip=trip, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.trip_blog', trip_id=trip.id))

    posts = Post.query.filter_by(trip_id=trip.id).order_by(
        Post.timestamp.desc()).all()
    return render_template('trip_blog.html', trip=trip, posts=posts, form=form)

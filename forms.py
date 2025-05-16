from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import TextAreaField, DateField


class RegisterForm(FlaskForm):
    name = StringField('Ім’я', validators=[
                       DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[
                             DataRequired(), Length(min=6)])
    confirm = PasswordField('Повтор пароля', validators=[
                            DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')


class TripForm(FlaskForm):
    title = StringField('Назва подорожі', validators=[DataRequired()])
    description = TextAreaField('Опис')
    start_date = DateField('Дата початку')
    end_date = DateField('Дата завершення')
    submit = SubmitField('Створити подорож')


class PostForm(FlaskForm):
    content = TextAreaField('Ваш пост', validators=[DataRequired()])
    submit = SubmitField('Опублікувати')

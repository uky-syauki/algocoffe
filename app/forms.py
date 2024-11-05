from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Harap mengisi email')])
    password = PasswordField('Password', validators=[DataRequired('Harap mengisi password')])
    submit = SubmitField('Login')
    
    
class RegisterForm(FlaskForm):
    username = StringField("Nama Lengkap", validators=[DataRequired('Harap mengisi email')])
    telp = StringField("Nomor Telpon", validators=[DataRequired('Harap mengisi Nomor Telpon')])
    alamat = StringField("Alamat", validators=[DataRequired('Harap mengisi Alamat')])
    email = StringField("Email", validators=[DataRequired('Harap mengisi Email')])
    password = PasswordField("Password", validators=[DataRequired('Harap mengisi password')])
    submit = SubmitField("Sign Up")
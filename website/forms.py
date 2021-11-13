from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, IntegerField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from .models import User
from werkzeug.security import check_password_hash
from flask_wtf.file import FileField, FileAllowed, FileRequired

class CorrectLogin:
    def __call__(self, form, field):
        user = User.query.filter_by(login=form.login.data).first()
        if not user:
            raise ValidationError("Niepoprawny login")
        if not check_password_hash(user.password, form.password.data):
            raise ValidationError("Niepoprawne haslo")


class LoginForm(FlaskForm):
    login = StringField("Login", [DataRequired(), Length(min=4, max=30)])
    password = PasswordField("Password", [DataRequired(), Length(min=8, max=30)])


class Password:
    def passwordHasUpperLetter(self):
        for let in self.password:
            if let.isupper():
                return True
        return False

    def passwordHasDigit(self):
        result = False
        for let in self.password:
            if let.isdigit():
                result = True
                break
        return result

    def __call__(self, form, field):
        self.password = field.data
        if not self.passwordHasDigit():
            raise ValidationError("Hasło powinno mieć przynajmniej jedną cyfrę")
        if not self.passwordHasUpperLetter():
            raise ValidationError("Hasło powinno mieć przynamniej jedną dużą literkę")

class EmailNotExists:
    def __call__(self, form, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Użytkownik o podanym adresie email już istnieje!")


class SignUpForm(FlaskForm):
    login = StringField("Login", [DataRequired(), Length(min=4, max=30)])
    email = StringField("Email", [DataRequired(), Length(min=4, max=30), Email()])
    password1 = PasswordField("Password", [DataRequired(), Length(min=8, max=30),
                                        EqualTo('password2', message='Passwords must match'),
                                        Password()])
    password2 = PasswordField("Password confirm", [DataRequired(), Length(min=8, max=30)])


class CommentForm(FlaskForm):
    comment = StringField(label= ('comment'),
                            validators=[DataRequired(), Length(max=150)])


class FilterFilms(FlaskForm):
    films_number = SelectField("films_number", [DataRequired()], coerce=int, choices=[(1, "jeden"), (4, "cztery"), (8, "osiem"), (16, "szesnaście")])


class UploadAvatarForm(FlaskForm):
    image = FileField('Upload (<=3M)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png.')
    ])
    submit = SubmitField()


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('Crop')

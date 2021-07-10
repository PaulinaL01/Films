from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email


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


class SignUpForm(FlaskForm):
    login = StringField("Login", [DataRequired(), Length(min=4, max=30)])
    email = StringField("Email", [DataRequired(), Length(min=4, max=30), Email()])
    password1 = PasswordField("Password", [DataRequired(), Length(min=8, max=30),
                                        EqualTo('password2', message='Passwords must match'),
                                        Password()])
    password2 = PasswordField("Password confirm", [DataRequired(), Length(min=8, max=30)])

class Complaint(FlaskForm):
    login = StringField(label=('Login'),
                           validators=[DataRequired(),
                                       Length(max=30)])
    complaint = StringField(label= ('complaint'),
                            validators=[DataRequired(),
                                       Length(max=150)])
    mark = IntegerField(label= ('complaint'),
                            validators=[DataRequired()])
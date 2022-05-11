import flask_wtf
from wtforms import StringField, PasswordField, validators


class LoginForm(flask_wtf.FlaskForm):
    user_number = StringField(
        'user_number',
        [validators.DataRequired()]
    )
    password = PasswordField(
        'password',
        [validators.DataRequired()]
    )

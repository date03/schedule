import flask_wtf
from wtforms import StringField, HiddenField, BooleanField, validators


class CreateUserForm(flask_wtf.FlaskForm):
    user_number = StringField(
        'user_number',
        [validators.DataRequired("必須事項です。"),
         validators.Length(7, 7, "確認してください。")],
        render_kw={'size': '7'}
    )
    password = StringField("password", render_kw={
                           'readonly': True, 'size': '7'})
    user_lname = StringField(
        'user_lname',
        [validators.DataRequired("必須事項です。"),
         validators.Length(-1, 15, "最大15文字までです。")],
        render_kw={'size': '7'}
    )
    user_fname = StringField(
        'user_fname',
        [validators.DataRequired("必須事項です。"),
         validators.Length(-1, 15, "最大15文字までです。")],
        render_kw={'size': '7'}
    )
    cook = BooleanField('cook')
    front = BooleanField('front')
    dns_admin = BooleanField('dns_admin')

    checkbox = BooleanField('checkbox',
                            [validators.DataRequired("必須事項です。")])

import flask_wtf
from wtforms import StringField, validators
from wtforms.widgets.core import TextArea


class CreateNewsForm(flask_wtf.FlaskForm):
    news_title = StringField(
        "news_title",
        [validators.DataRequired("必須事項です。"),
         validators.Length(-1, 30, "最大30文字までです。")],
        render_kw={'size': '30'}
    )
    news_body = StringField(
        "news_body",
        [validators.DataRequired("必須事項です。"),
         validators.Length(-1, 1000, "最大1000文字までです。")],
        widget=TextArea()
    )

import flask_wtf
from wtforms import SelectField, SubmitField, HiddenField


class WeekDayForm(flask_wtf.FlaskForm):
    week = SelectField('week', choices=[
                       (0, '月'), (1, '火'), (2, '水'), (3, '木'), (4, '金'), (5, '土'), (6, '日')])
    sub = SubmitField("検索")


class DeleteMonthScheduleForm(flask_wtf.FlaskForm):
    delid = HiddenField("delid")
    sub = SubmitField("削除")

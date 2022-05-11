import flask_wtf
from wtforms import SelectField, HiddenField
from wtforms.fields.simple import SubmitField


class DayScheduleForm(flask_wtf.FlaskForm):
    hour = [('--', '--'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
            ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24')]
    minutes = [('--', '--'), ('00', '00'), ('30', '30')]

    day = SelectField('day', choices=[])
    s_h = SelectField('s_h', choices=hour)
    s_m = SelectField('s_m', choices=minutes)
    e_h = SelectField('e_h', choices=hour)
    e_m = SelectField('e_m', choices=minutes)


class DeleteDayScheduleForm(flask_wtf.FlaskForm):
    delid = HiddenField("delid")
    sub = SubmitField("削除")

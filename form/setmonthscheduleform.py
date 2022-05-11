import flask_wtf
from wtforms import SelectField


class SetMonthScheduleForm(flask_wtf.FlaskForm):
    hour = [('--', '--'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
            ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24')]
    minutes = [('--', '--'), ('00', '00'), ('30', '30')]

    user_number = SelectField('user_number', choices=[])
    week = SelectField('week', choices=[(
        0, '月'), (1, '火'), (2, '水'), (3, '木'), (4, '金'), (5, '土'), (6, '日')])
    s_h = SelectField('s_h', choices=hour)
    s_m = SelectField('s_m', choices=minutes)
    e_h = SelectField('e_h', choices=hour)
    e_m = SelectField('e_m', choices=minutes)

import flask_wtf
from wtforms import SelectField
import datetime


class GetMonthScheduleForm(flask_wtf.FlaskForm):
    month = SelectField(
        'month', choices=[])
    week = SelectField('week', choices=[(
        0, '月'), (1, '火'), (2, '水'), (3, '木'), (4, '金'), (5, '土'), (6, '日')])
    position = SelectField('position', choices=[(
        'all', 'すべて'), ('cook', 'キッチン'), ('front', 'フロント')])
    time = SelectField('time', choices=[('all', '--'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
                                        ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24')])

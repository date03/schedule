import flask_wtf
from wtforms import SelectField


class MonthScheduleForm(flask_wtf.FlaskForm):
    hour = [('--', '--'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
            ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24')]
    minutes = [('--', '--'), ('00', '00'), ('30', '30')]
    week = SelectField('week', choices=[(
        0, '月'), (1, '火'), (2, '水'), (3, '木'), (4, '金'), (5, '土'), (6, '日')])
    w_s_h = SelectField('w_s_h', choices=hour)
    w_s_m = SelectField('w_s_m', choices=minutes)
    w_e_h = SelectField('w_e_h', choices=hour)
    w_e_m = SelectField('w_e_m', choices=minutes)

    m_s_h = SelectField('m_s_h', choices=hour)
    m_s_m = SelectField('m_s_m', choices=minutes)
    m_e_h = SelectField('m_e_h', choices=hour)
    m_e_m = SelectField('m_e_m', choices=minutes)

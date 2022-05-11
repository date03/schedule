import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./drive/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'kaihatusitanohahimazindesu'
db = SQLAlchemy(app)


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10), unique=True)  # 従業員番号(ID)
    user_lname = db.Column(db.String(15))  # 苗字
    user_fname = db.Column(db.String(15))  # 名前
    dns_admin = db.Column(db.Boolean, default=False)  # dnsの管理画面が見れるか
    admin = db.Column(db.Boolean, default=False)  # 管理者画面が見れるか
    create = db.Column(db.String(10))  # ユーザの作成者

    def __init__(self, user_number, user_lname, user_fname, create, dns_admin=False):
        self.user_number = user_number
        self.user_lname = user_lname
        self.user_fname = user_fname
        self.create = create
        self.dns_admin = dns_admin


class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10), unique=True)  # 従業員番号(ID)
    password_hash = db.Column(db.String(100), nullable=False)  # ハッシュ化したパスワード
    last_login = db.Column(db.DateTime)  # 最終ログイン時刻

    def __init__(self, user_number, password):
        self.user_number = user_number
        self._set_password(password)

    # パスワードをハッシュ化
    def _set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 入力されたパスワードが登録されているパスワードハッシュと一致するかを確認
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def login(self):
        self.last_login = datetime.datetime.now()


class UserPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10))  # 従業員番号(ID)
    store_number = db.Column(db.Integer)  # 店番
    cook = db.Column(db.Boolean, default=False)  # キッチンができるか
    front = db.Column(db.Boolean, default=False)  # フロントができるか

    def __init__(self, user_number, store_number, cook, front):
        self.user_number = user_number
        self.store_number = store_number
        self.cook = cook
        self.front = front


class UserSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10))  # 従業員番号(ID)
    month = db.Column(db.Integer)  # 何月分のスケジュールか
    w_m = db.Column(db.String(1))  # 希望(w)or最大(m)
    week = db.Column(db.String(2))  # 曜日(mo,tu,we,th,fr,sa,su)
    s_hour = db.Column(db.String(2))  # 開始時
    s_minute = db.Column(db.String(2))  # 分
    e_hour = db.Column(db.String(2))  # 終了時
    e_minute = db.Column(db.String(2))  # 分
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 更新日時

    def __init__(self, user_number, month, w_m, week, s_hour, s_minute, e_hour, e_minute):
        self.user_number = user_number
        self.month = month
        self.w_m = w_m
        self.week = week
        self.s_hour = s_hour
        self.s_minute = s_minute
        self.e_hour = e_hour
        self.e_minute = e_minute

    def commit_t(self, s_hour, s_minute, e_hour, e_minute):
        self.s_hour = s_hour
        self.s_minute = s_minute
        self.e_hour = e_hour
        self.e_minute = e_minute
        self.update = datetime.datetime.now()


class StdSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10))  # 従業員番号(ID)
    month = db.Column(db.Integer)  # 何月分のスケジュールか
    week = db.Column(db.String(2))  # 曜日(mo,tu,we,th,fr,sa,su)
    s_hour = db.Column(db.String(2))  # 開始時
    s_minute = db.Column(db.String(2))  # 分
    e_hour = db.Column(db.String(2))  # 終了時
    e_minute = db.Column(db.String(2))  # 分
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 更新日時

    def __init__(self, user_number, month, week, s_hour, s_minute, e_hour, e_minute):
        self.user_number = user_number
        self.month = month
        self.week = week
        self.s_hour = s_hour
        self.s_minute = s_minute
        self.e_hour = e_hour
        self.e_minute = e_minute
        self.update = datetime.datetime.now()


class DaySchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10))  # 従業員番号(ID)
    day = db.Column(db.Date)  # 日にち
    s_hour = db.Column(db.String(2))  # 開始時
    s_minute = db.Column(db.String(2))  # 分
    e_hour = db.Column(db.String(2))  # 終了時
    e_minute = db.Column(db.String(2))  # 分
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 利用者の登録日時
    conf = db.Column(db.Boolean, default=False)  # 管理者が確認済みか否か
    confdate = db.Column(db.DateTime)  # 管理者が確認した時刻

    def __init__(self, user_number, day, s_hour, s_minute, e_hour, e_minute):
        self.user_number = user_number
        self.day = day
        self.s_hour = s_hour
        self.s_minute = s_minute
        self.e_hour = e_hour
        self.e_minute = e_minute
        self.conf = False
        self.update = datetime.datetime.now()

    def configu(self):
        self.conf = True
        self.confdate = datetime.datetime.now()


class StoreSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10))  # 従業員番号(ID)
    day = db.Column(db.Date)  # 日にち
    s_hour = db.Column(db.String(2))  # 開始時
    s_minute = db.Column(db.String(2))  # 分
    e_hour = db.Column(db.String(2))  # 終了時
    e_minute = db.Column(db.String(2))  # 分
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 更新日時

    def __init__(self, user_number, day, s_hour, s_minute, e_hour, e_minute):
        self.user_number = user_number
        self.day = day
        self.s_hour = s_hour
        self.s_minute = s_minute
        self.e_hour = e_hour
        self.e_minute = e_minute
        self.update = datetime.datetime.now()


class ContractSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10), unique=True)  # 従業員番号(ID)
    week = db.Column(db.String(2))  # 曜日(mo,tu,we,th,fr,sa,su)
    s_hour = db.Column(db.String(2))  # 開始時
    s_minute = db.Column(db.String(2))  # 分
    e_hour = db.Column(db.String(2))  # 終了時
    e_minute = db.Column(db.String(2))  # 分
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 更新日時


class DnsNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    store_number = db.Column(db.Integer)  # 店番
    user_number = db.Column(db.String(10))  # 従業員番号(ID)
    news_title = db.Column(db.String(30), nullable=False)  # ニュースタイトル
    news_body = db.Column(db.String(1000), nullable=False)  # ニュース本文
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 更新日時

    def __init__(self, store_number, user_number, news_title, news_body):
        self.store_number = store_number
        self.user_number = user_number
        self.news_title = news_title
        self.news_body = news_body
        self.update = datetime.datetime.now()


class DeveloperNews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 通し番号
    user_number = db.Column(db.String(10))  # 従業員番号(ID)
    news_title = db.Column(db.String(30), nullable=False)  # ニュースタイトル
    news_body = db.Column(db.String(1000), nullable=False)  # ニュース本文
    news_category = db.Column(db.String(10))  # カテゴリ
    update = db.Column(db.DateTime, default=datetime.datetime.now)  # 更新日時


db.create_all()

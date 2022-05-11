"""共通ページやログイン部分の処理"""

from form import LoginForm
from database import DeveloperNews, User, UserLogin, db
from flask import Blueprint, render_template, request, redirect, abort
import flask_login

ddn_app = Blueprint("ddn", __name__)


@ddn_app.route("/", methods=['GET'])  # トップページ
def ddn():
    news = DeveloperNews.query.order_by(DeveloperNews.id.desc()).all()
    return render_template("ddn/ddn.html", all_news=news)


"""
@ddn_app.route("/index", methods=['GET'])  # 旧トップページから現在へのリダイレクト
def index():
    return redirect("/")
"""


@ddn_app.route("/news/<news_id>", methods=['GET'])  # ニュースの詳細
def ddn_news(news_id=None):
    news = DeveloperNews.query.filter_by(id=news_id).first()
    if news_id == None or news == None:
        abort(404)
    create_user = User.query.filter_by(
        user_number=news.user_number).first()
    return render_template('ddn/news.html', news=news, create_user=create_user.user_lname+create_user.user_fname)


@ddn_app.route("/redirect", methods=['GET'])  # リダイレクト時に表示するページ
def ddn_redirect():
    return render_template("ddn/redirect.html", status=request.args.get("status"), next=request.args.get("next"))


@ddn_app.route("/login", methods=["GET", "POST"])  # ログインページ
def ddn_login():
    if flask_login.current_user.is_authenticated:  # すでにログイン中なら/に飛ばす
        return redirect("/")

    form = LoginForm(request.form)
    if form.validate_on_submit():  # サインインボタンを押すと呼ばれる
        userlogin = UserLogin.query.filter_by(
            user_number=form.user_number.data).one_or_none()  # DBのログイン情報を探す

        # 見つからないかパスワードが一致しなければエラー
        if userlogin is None or not userlogin.check_password(form.password.data):
            return render_template("ddn/login.html", form=form, status="error", next=request.args.get("next"))

        userlogin.login()
        db.session.add(userlogin)  # 最終ログイン時刻の記録
        db.session.commit()
        user = User.query.filter_by(
            user_number=userlogin.user_number).one_or_none()
        flask_login.login_user(user)

        if request.args.get("next") is not None:
            return redirect("/redirect?status=redirect&next="+request.args.get("next"))
        else:
            return redirect("/redirect?status=login")

    return render_template("ddn/login.html", form=form)


@ddn_app.route("/logout", methods=['GET'])  # ログアウトページ
def ddn_logout():
    flask_login.logout_user()
    return redirect("/redirect?status=logout")

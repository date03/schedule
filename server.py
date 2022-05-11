import page
from database import *
from waitress import serve
from flask import redirect, request, render_template

debug = False

"""ログイン実装関連"""

login_manager = flask_login.LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/redirect?status=mustlogin&next='+request.path)


"""ページの読み込み"""

app.register_blueprint(page.ddn_app)
app.register_blueprint(page.minecraft_app)
app.register_blueprint(page.dns_app)
app.register_blueprint(page.etc_app)


"""エラー用ページ"""


@app.errorhandler(404)
def e404(error):
    return render_template("etc/e404.html"), 404


"""起動部分"""

if __name__ == "__main__":
    if debug:
        app.run(host='0.0.0.0', port=8081, debug=True)
    else:
        serve(app, host='0.0.0.0', port=5000)

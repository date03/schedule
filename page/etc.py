from flask import Blueprint, send_from_directory, render_template

etc_app = Blueprint("etc", __name__)


"""アイコンを渡す"""


@etc_app.route("/favicon.ico", methods=['GET'])
def favicon():
    return send_from_directory("static/images", "icon.ico", mimetype="image/vnd.microsoft.icon")


"""サイトマップの送信"""


@etc_app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return send_from_directory("static/xml", 'sitemap.xml', mimetype='application/xml')


"""SSL発行関連"""


# SSLの発行用
@ etc_app.route('/.well-known/acme-challenge/<filename>', methods=['GET'])
def well_known(filename):  # 登録に必要なものはテンプレートのetcへ入れておく
    return render_template("etc/.well-known/acme-challenge/" + filename)


"""ads.txt用"""


@etc_app.route('/ads.txt', methods=['GET'])
def ads():
    return send_from_directory("static/text", 'ads.txt', mimetype='text/plain')

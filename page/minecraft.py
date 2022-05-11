from flask import Blueprint, render_template

minecraft_app = Blueprint("minecraft", __name__)


@minecraft_app.route("/minecraft", methods=['GET'])
def minecraft():
    from module import minecraft_log
    return render_template("minecraft/minecraft.html", minecraft_log=minecraft_log.log())


@minecraft_app.route("/minecraft/mod", methods=['GET'])
def minecraft_mod():
    return render_template("minecraft/mod.html")

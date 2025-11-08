from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.models import User, Group, Printer
from app import db

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return render_template("home.html")

@home_bp.route("/home")
def home_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    user = User.query.get(session["user_id"])
    groups = user.groups  # pega todos os grupos do usuário
    return render_template("home_group.html", groups=groups)

# Cadastrar novo grupo
@home_bp.route("/groups/new", methods=["POST"])
def new_group():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    user = User.query.get(session["user_id"])
    name = request.form.get("name")

    if not name:
        flash("Nome do grupo é obrigatório", "error")
        return redirect(url_for("home.home_page"))

    # Cria grupo e adiciona o usuário automaticamente
    group = Group(name=name)
    group.users.append(user)
    db.session.add(group)
    db.session.commit()

    flash("Grupo cadastrado!", "success")
    return redirect(url_for("home.home_page"))

@home_bp.route("/groups/<int:group_id>/printers")
def group_printers(group_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    user = User.query.get(session["user_id"])
    group = Group.query.get(group_id)

    # Segurança: o usuário só pode acessar grupos aos quais pertence
    if group not in user.groups:
        return "Acesso negado", 403

    printers = group.printers
    return render_template("group_printers.html", group=group, printers=printers)

@home_bp.route("/groups/<int:group_id>/printers/new", methods=["GET", "POST"])
def new_printer(group_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    user = User.query.get(session["user_id"])
    group = Group.query.get(group_id)

    if group not in user.groups:
        return "Acesso negado", 403

    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return "Nome da impressora é obrigatório", 400

        printer = Printer(name=name, group_id=group.id)
        db.session.add(printer)
        db.session.commit()

        return redirect(url_for("home.group_printers", group_id=group.id))

    return render_template("new_printer.html", group=group)
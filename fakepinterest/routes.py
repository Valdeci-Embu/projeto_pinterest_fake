# criar as rotas do site
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Fotos
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, email=formcriarconta.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=formcriarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # o usuario ta vendo seu proprio
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            #salvar o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)

            #registrar esse arquivo no banco de dados
            foto = Fotos(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario=current_user, form=formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Fotos.query.order_by(Fotos.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)
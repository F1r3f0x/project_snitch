"""
    Rutas
"""
################################################
# Includes
# Stdlib
from functools import wraps
from datetime import datetime
import copy

from flask import jsonify, request, url_for, abort, flash, redirect
from flask import render_template, session, logging, make_response

from flask_login import LoginManager, login_user, logout_user, current_user
from flask_login import login_required

from sqlalchemy.exc import OperationalError, IntegrityError

from werkzeug.routing import BuildError

from project_snitch.forms import UserRegisterForm, UserLoginForm, UserSubscribeForm
from project_snitch.forms import UserUnsubscribeForm, UserChangeProfile

from project_snitch.models import Legislador
from project_snitch.models import EstadoNoticioso
from project_snitch.models import CargoLegislativo
from project_snitch.models import PartidoPolitico
from project_snitch.models import Region
from project_snitch.models import TipoLegislador
from project_snitch.models import Periodo
from project_snitch.models import Distrito
from project_snitch.models import Circunscripcion
from project_snitch.models import TipoUsuario
from project_snitch.models import Usuario
from project_snitch.models import Noticia, FuenteNoticias

from project_snitch import app, db, login, searcher#, whooshee
from project_snitch import my_utils
from project_snitch.my_tools import funciones as tools

HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_INTERNAL_SERVER_ERROR = 500

ID_TIPO_SENADOR = 1
ID_TIPO_DIPUTADO = 2

NOTICIAS_POR_PAGINA = 10


def requiere_admin(fun):
    @wraps(fun)
    def vista_admin(*args, **kwargs):
        if not current_user.is_admin():
            flash('Necesitas ser administrador para entrar a esta pagina',
                  'danger')
            return redirect(url_for('home'))
        return fun(*args, **kwargs)
    return vista_admin


@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))


###############################################################################
# Rutas

@app.route('/', methods=['GET'])
def home():
    changelog = tools.get_changelog(app.config['CHANGELOG_DIR'])
    return render_template('index.html', changelog=changelog)


@app.route('/legislador/<int:id_legislador>', methods=['GET', 'POST'])
def mostrar_legislador(id_legislador):
    try:
        legislador = Legislador.query.get(id_legislador)

        if legislador:
            if len(legislador.cargos) > 0:
                # Ultimo Cargo
                ultimo_cargo = legislador.cargos[-1]

                # Lista de Cargos
                cargos = []
                for cargo in legislador.cargos:
                    # Año fin es nullable y va a mostrar None cuando se llama a str().
                    if cargo.periodo.anno_fin:
                        anno_fin = str(cargo.periodo.anno_fin)
                    else:
                        anno_fin = ''

                    cargo_vista = {
                        'tipo': cargo.tipo.nombre,
                        'years': '-'.join([str(cargo.periodo.anno_inicio),
                                           anno_fin]),
                        'partido': cargo.partido.nombre
                    }

                    if cargo.region:
                        cargo_vista['region'] = cargo.region.numero
                    else:
                        cargo_vista['region'] = ''

                    if cargo.tipo_legislador_id == ID_TIPO_SENADOR:
                        cargo_vista['circunscripcion'] = str(
                            cargo.circunscripcion.numero)
                        cargo_vista['distritos'] = my_utils.string_distritos(
                            cargo.distritos)
                    else:
                        cargo_vista['circunscripcion'] = '-'
                        cargo_vista['distritos'] = cargo.distritos[0].numero

                    cargos.append(cargo_vista)

                if ultimo_cargo.tipo_legislador_id == ID_TIPO_SENADOR:
                    distritos = my_utils.string_distritos(ultimo_cargo.distritos)
                    is_senador = True
                else:
                    distritos = ultimo_cargo.distritos[0].numero
                    is_senador = False

                noticia = Noticia.query.filter_by(id=1).first()

                if current_user.is_authenticated:
                    if legislador not in current_user.favoritos:
                        # Subscribirse
                        form = UserSubscribeForm()
                        if form.validate_on_submit():
                            current_user.favoritos.append(legislador)
                            db.session.add(current_user)
                            db.session.commit()

                            flash(f'Sapeando {legislador.primer_nombre} {legislador.primer_apellido}!', 'success')

                            return redirect(url_for('mostrar_legislador',
                                                    id_legislador=id_legislador))

                        return render_template('legislador.html',
                                               barra_busqueda=True,
                                               titulo=str(legislador),
                                               senador=is_senador,
                                               legislador=legislador,
                                               distritos=distritos,
                                               cargo=ultimo_cargo,
                                               lista_cargos=cargos,
                                               form=form
                                               )

                return render_template('legislador.html',
                                       barra_busqueda=True,
                                       titulo=str(legislador),
                                       senador=is_senador,
                                       legislador=legislador,
                                       distritos=distritos,
                                       cargo=ultimo_cargo,
                                       lista_cargos=cargos,
                                       )
            else:
                app.logger.info(f'{datetime.now()}: Legislador {legislador} no tiene cargos!!.')
                return 'Este legislador esta mal registrado, contacte al administrador (plabin@outlook.cl)',\
                       HTTP_INTERNAL_SERVER_ERROR
        else:
            return abort(HTTP_INTERNAL_SERVER_ERROR)

    except OperationalError:
        return abort(HTTP_SERVICE_UNAVAILABLE)


@app.route('/lista_legisladores')
#@login_required
#@requiere_admin
def lista_legisladores():
    legisladores = Legislador.query.order_by(Legislador.primer_apellido).all()

    lista_senadores = []
    lista_diputados = []

    for l in legisladores:
        if l.is_senador():
            lista_senadores.append(l)
        else:
            lista_diputados.append(l)

    return render_template('lista_legisladores.html',
                           barra_busqueda=True,
                           titulo='Lista Legisladores',
                           senadores=lista_senadores,
                           diputados=lista_diputados)


@app.route('/buscar')
def buscar():
    texto = request.args.get('buscar', None, str).strip().lower()
    if texto:
        results = Legislador.query.msearch(texto)
        resultado_busqueda = []
        for r in results:
            cargos = r.cargos
            if len(cargos) > 0:
                resultado_busqueda.append({'legislador': r, 'ultimo_cargo': cargos[len(cargos)-1]})
        if resultado_busqueda:
            return render_template('buscar.html',
                                   barra_busqueda=True,
                                   titulo=f'Buscar "{texto}"',
                                   busqueda=texto,
                                   results=resultado_busqueda)

        return render_template('buscar.html',
                               barra_busqueda=True,
                               titulo='Buscar',
                               busqueda=texto)
    else:
        return redirect(url_for('home'))


@app.route('/registrar', methods=['GET', 'POST'])
def registrar_usuario():
    form = UserRegisterForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        password = form.password.data

        nuevo_usuario = Usuario(nombre=nombre,
                                email=email,
                                password=password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        app.logger.info(f'{datetime.now()}: User {nuevo_usuario} registered')

        flash('Estas registrado!', 'success')
        return redirect(url_for('home'))

    return render_template('registrar.html',
                           barra_busqueda=True,
                           titulo='Registrarse',
                           form=form,
                           debug=app.config['DEBUG'])


@app.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = UserLoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nombre=form.nombre.data).first()
        if usuario is None or not usuario.check_password(form.password.data):
            flash('Nombre de usuario o contraseña es incorrecto', 'danger')
            return redirect(url_for('login_usuario'))

        login_user(usuario, remember=form.remember_me.data)

        app.logger.info(f'{datetime.now()}: {usuario} logged in')

        flash(f'Bienvenido {usuario.nombre}!', 'success')

        next_page = request.args.get('next')

        if next_page:
            try:
                next_page = my_utils.get_last_dir_url(next_page)
                return redirect(url_for(next_page))
            except BuildError:
                app.logger.info(f'{datetime.now()}: Wierd redirect: {next_page} from {current_user} - {request.remote_addr}')
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))

    return render_template('login.html',
                           barra_busqueda=True,
                           titulo='Login',
                           form=form,
                           debug=app.config['DEBUG'])


@app.route('/logout')
@login_required
def logout_usuario():
    _user = copy.copy(current_user)
    logout_user()
    app.logger.info(f'{datetime.now()}: User {_user } logged out')
    return redirect(url_for('home'))


@app.route('/lista_noticias')
def mostrar_lista_noticias():
    pagina = request.args.get('pagina', 1, int)
    noticias = Noticia.query.order_by(Noticia.fecha.desc()).paginate(pagina, NOTICIAS_POR_PAGINA, True)

    siguiente_url = url_for('mostrar_lista_noticias',
                            pagina=noticias.next_num) if noticias.has_next else None
    anterior_url = url_for('mostrar_lista_noticias',
                           pagina=noticias.prev_num) if noticias.has_prev else None

    return render_template('lista_noticias.html',
                           barra_busqueda=True,
                           titulo='Lista de Noticias',
                           pagina=pagina,
                           noticias=noticias.items,
                           siguiente=siguiente_url,
                           anterior=anterior_url)


@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def mostrar_perfil():
    form = UserUnsubscribeForm()
    if form.validate_on_submit():
        id_legislador = request.form['legislador']
        legislador = Legislador.query.get(id_legislador)

        if not legislador or not id_legislador:
            return abort(HTTP_INTERNAL_SERVER_ERROR)

        current_user.favoritos.remove(legislador)
        db.session.commit()

        flash(f'Dejaste de Sapear a {legislador}', 'success')

        return redirect(url_for('mostrar_perfil'))

    return render_template('perfil.html',
                           barra_busqueda=True,
                           titulo='Mi Perfil',
                           usuario=current_user,
                           form=form)


@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = UserChangeProfile()

    if form.validate_on_submit():

        nuevo_nombre = form.nombre.data
        nueva_pass = form.password.data
        nuevo_mail = form.email.data

        if nuevo_nombre:
            current_user.nombre = nuevo_nombre
            db.session.add(current_user)
            db.session.commit()

        if nueva_pass:
            current_user.password = nueva_pass
            db.session.add(current_user)
            db.session.commit()

        if nuevo_mail:
            current_user.mail = nuevo_mail
            db.session.add(current_user)
            db.session.commit()

        app.logger.info(f'{datetime.now()}: User {current_user} edited his profile.')

        flash('Perfil editado correctamente!', 'success')

        return redirect(url_for('mostrar_perfil'))

    return render_template('editar_perfil.html',
                           barra_busqueda=True,
                           titulo='Editar Perfil',
                           usuario=current_user,
                           form=form,
                           debug=app.config['DEBUG'])


###############################################################################
"""
    API
    Utiliza flask.make_response() para agregar los headers necesarios para utilizar la API desde otro dominio
"""

@app.route('/api')
def mostrar_api():
    return render_template('api.html')


@app.route('/api/legisladores', methods=['GET'])
def get_legislador():

    _id = request.args.get('id', None, int)

    dict_respuesta = []
    if _id:
        legislador = Legislador.query.filter_by(id=_id).first()
        if legislador:
            dict_respuesta.append(legislador.json_dict())
    else:
        legisladores = Legislador.query.all()
        for l in legisladores:
            dict_respuesta.append(l.json_dict())

    if dict_respuesta:
        resp = make_response(jsonify(data={'legisladores': dict_respuesta}), 200)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = make_response(jsonify(data={'msg': 'El Legislador no existe'}), 404)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


###############################################################################
# Ajax
@app.route('/ajax/nombres_legisladores')
def ajax_nombres():
    termino = request.args.get('term', None, str).strip().lower()
    if termino:
        legisladores = Legislador.query.msearch(termino)
        respuesta_json = [{'label': str(_l), 'value': str(_l.id)} for _l in legisladores]
        if respuesta_json:
            return jsonify(data=respuesta_json), 200

    return jsonify(data='El termino no se encuentra'), 404


@app.route('/ajax/legislador/noticias')
def ajax_legislador_noticias():
    noticias = []
    try:
        id = request.args.get('id', 1, int)
        noticias = Legislador.query.get(id).noticias
    except AttributeError:
        pass

    if noticias:
        data = [_noticia.ajax_dict() for _noticia in noticias]
        return jsonify(data), 200

    return jsonify(data='El termino no se encuentra'), 404


###############################################################################

# SimpleSearch no necesita index
# @app.route('/reindex')
# @login_required
# @requiere_admin
# def index():
#     searcher.delete_index()
#     searcher.create_index()
#     flash('Reindex OK!', 'success')
#     return redirect(url_for('home'))

################################################################################

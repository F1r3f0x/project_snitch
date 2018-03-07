"""
    Vistas de Flask Admin
"""
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import current_user
from flask import flash, redirect, url_for
from wtforms import PasswordField
from project_snitch import admin, db, login
from project_snitch import models


class BaseAdminView(ModelView):
    """
    Clase Base Segura
    """
    form_base_class = SecureForm  # Proteccion contra CRFS
    can_delete = False

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin()
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        print(name)
        flash('Necesita ser administrador para acceder a esta seccion', 'warning')
        return redirect(url_for('login_usuario'))


class CargoLegislativoAdminView(BaseAdminView):
    column_exclude_list = ('id_interna', )
    column_searchable_list = ('legislador.texto_buscable', 'partido.nombre',
                              'region.nombre')
    column_sortable_list = (('legislador', 'legislador.texto_buscable'),
                            ('tipo', 'tipo.nombre'),
                            ('region', 'region.numero'))
    column_filters = ('partido.nombre', 'region.nombre')


class UsuarioAdminView(BaseAdminView):
    create_modal = True
    edit_modal = True
    column_searchable_list = ('nombre', 'email')
    column_exclude_list = ('password_hash', )

    # Fix para reesctritura de contraseña
    form_excluded_columns = ('password_hash', )
    form_extra_fields = {
        'password_help': PasswordField('Contraseña')
    }

    def on_model_change(self, form, model, is_created):
        if form.password_help.data != '':
            model.password = form.password_help.data
    ##


class LegisladorAdminView(BaseAdminView):
    column_searchable_list = ('primer_nombre', 'primer_apellido',
                              'segundo_nombre', 'segundo_apellido',
                              'texto_buscable', 'email')
    column_exclude_list = ('texto_buscable', 'foto_url')
    column_filters = ('estado_noticioso.nombre', )
    form_excluded_columns = ('seguidores', 'texto_buscable')
    page_size = 40


class StdCargosAdminView(BaseAdminView):
    create_modal = True
    edit_modal = True
    form_excluded_columns = ('cargos', )


class PartidoPoliticioAdminView(StdCargosAdminView):
    column_exclude_list = ('logo_url', )


class TipoUsuarioAdminView(StdCargosAdminView):
    form_excluded_columns = ('usuarios', )


class PeriodoAdminView(StdCargosAdminView):
    column_labels = {
        'anno_inicio': 'Año Inicio',
        'anno_fin': 'Año Fin'
    }


class EstadoNoticiosoAdminView(StdCargosAdminView):
    form_excluded_columns = ('legisladores', )


class NoticiaAdvminView(BaseAdminView):
    can_delete = True
    create_modal = True
    edit_modal = True
    column_exclude_list = ('contenido_texto', 'preview_url', 'titulo_buscable')
    column_searchable_list = ('titulo', 'fuente.nombre')
    column_sortable_list = ('titulo', ('fuente','fuente.id'), 'fecha')


admin.add_view(CargoLegislativoAdminView(models.CargoLegislativo, db.session))
admin.add_view(StdCargosAdminView(models.Circunscripcion, db.session))
admin.add_view(StdCargosAdminView(models.Distrito, db.session))
admin.add_view(EstadoNoticiosoAdminView(models.EstadoNoticioso, db.session))
admin.add_view(LegisladorAdminView(models.Legislador, db.session))
admin.add_view(PartidoPoliticioAdminView(models.PartidoPolitico, db.session))
admin.add_view(PeriodoAdminView(models.Periodo, db.session))
admin.add_view(StdCargosAdminView(models.Region, db.session))
admin.add_view(StdCargosAdminView(models.TipoLegislador, db.session))
admin.add_view(TipoUsuarioAdminView(models.TipoUsuario, db.session))
admin.add_view(UsuarioAdminView(models.Usuario, db.session))
admin.add_view(NoticiaAdvminView(models.Noticia, db.session))
admin.add_view(BaseAdminView(models.FuenteNoticias, db.session))

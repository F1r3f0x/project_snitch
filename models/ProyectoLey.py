from datetime import datetime
from app import db
import app.my_tools.funciones as tools

tabla_autores_proyecto = db.Table(
    'autores_proyecto',
    db.Column('cargo_legislativo_id', db.Integer,
              db.ForeignKey('cargo_legislativo.id'), primary_key=True),
    db.Column('proyecto_ley_id', db.Integer,
              db.ForeignKey('proyecto_ley.id'), primary_key=True)
)


class ProyectoLey(db.Model):
    """
    Modelo SQLAlchemy de Proyecto de Ley.

    Attributes:
        id (int): Id.
        nombre (str): Nombre.
        descripcion (str): Descripcion.
        camara_origen_id (int): Id de camara de origen del proyecto.
        fecha (date): Fecha de creacion del proyecto
        url (str): Url al proyecto
        nombre_buscable (str): Nombre buscable para whoosh
        activo (bool): Esta activo en el sistema?

        votaciones (list[Votacion]): Lista de votaciones del proyecto.
        autores (list[CargoLegislativo]): Lista de Autores del proyecto

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'proyecto_ley'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), nullable=False)
    descripcion = db.Column(db.String(2048), nullable=True)
    camara_origen_id = db.Column(db.Integer, db.ForeignKey('camara.id'),
                                 nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now())
    url = db.Column(db.String(1024), nullable=False)
    nombre_buscable = db.Column(db.String(256), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    votaciones = db.relationship('Votacion', backref='proyecto_ley')

    autores = db.relationship('CargoLegislativo', secondary=tabla_autores_proyecto,
                              lazy='subquery',
                              backref=db.backref('proyectos_ley', lazy=True))

    def __init__(self,
                 camara_origen_id,
                 nombre='',
                 descripcion='',
                 url='',
                 **kwargs):
        """

        Args:
            nombre (str): Nombre.
            descripcion (str): Descripcion.
            camara_origen_id (int): Id de camara de origen del proyecto.
            url (str): Url al proyecto
            activo (bool): Esta activo en el sistema?

        Keyword Args:
            fecha (date): Fecha de creacion del proyecto

            votaciones (list[Votacion]): Lista de votaciones del proyecto.
            autores (list[CargoLegislativo]): Lista de Autores del proyecto
        """
        super(ProyectoLey, self).__init__(**kwargs)
        self.nombre = nombre
        self.nombre_buscable = tools.get_texto_buscable(nombre)
        self.descripcion = descripcion
        self.camara_origen_id = camara_origen_id
        self.url = url

        fecha = kwargs.get('fecha')
        if fecha:
            self.fecha = fecha
        self.votaciones = kwargs.get('votaciones')
        self.autores = kwargs.get('autores')

    def __repr__(self):
        return f'<ProyectoLey {self.id}: {self.nombre}>'

    def __str__(self):
        return self.nombre

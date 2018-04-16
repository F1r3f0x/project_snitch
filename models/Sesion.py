from datetime import datetime
from app import db

lista_asistencia = db.Table(
    'lista_asistencia',
    db.Column('sesion_id', db.Integer, db.ForeignKey('sesion.id'),
              primary_key=True),
    db.Column('cargo_legislativo_id', db.Integer,
              db.ForeignKey('cargo_legislativo.id'), primary_key=True)
)


class Sesion(db.Model):
    """
    Modelo SQLAlchemy de Sesion del Congreso.

    Attributes:
        id (int): Id.
        numero (int): Numero de la sesion
        camara_id (int): Id de camara de la sesion
        fecha (datetime): Fecha
        nombre (str): Nombre.
        descripcion (str): Descripcion.
        numero_asistir (int): Numero de legisladores que deben asistir a la sesion.
        porc_asistencia (int): Porcentaje de asistencia a la sesion.
        numero_asistentes (int): Numero de asistentes a la sesion.
        url (str): Url a la sesion.
        activo (bool): Esta activo en el sistema?

        camara (Camara): Camara de la Sesion.
        cargos (list[CargoLegislativo]): Lista de asistentes a la sesion.
        votaciones (list[Votacion]): Lista de Votaciones de la sesion

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'sesion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer, nullable=False)
    camara_id = db.Column(db.Integer, db.ForeignKey('camara.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now())
    nombre = db.Column(db.String(256), nullable=True)
    descripcion = db.Column(db.String(256), nullable=True)
    numero_asisitr = db.Column(db.Integer, nullable=True)
    porc_asistencia = db.Column(db.Integer, nullable=True)
    numero_asistentes = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(1024), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    camara = db.relationship('Camara', backref='sesiones')
    cargos = db.relationship('CargoLegislativo', secondary=lista_asistencia,
                             lazy='subquery',
                             backref=db.backref('sesiones'))
    votaciones = db.relationship('Votacion', backref='sesion')

    def __init__(self,
                 camara_id=1,
                 numero=0,
                 nombre='Sesion Nombre',
                 descripcion='',
                 url='www.senado.cl/sesion/1',
                 **kwargs):
        """

        Args:
            id (int): Id.
            camara_id (int): Id de Camara de la sesion.
            numero (int): Numero de la sesion
            nombre (str): Nombre.
            descripcion (str): Descripcion.
            url (str): Url a la sesion.

        Keyword Args:
            fecha (datetime): Fecha
            nombre (str): Nombre.
            numero_asistir (int): Numero de legisladores que deben asistir a la sesion.
            porc_asistencia (int): Porcentaje de asistencia a la sesion.
            numero_asistentes (int): Numero de asistentes a la sesion.

            camara (Camara): Camara de la Sesion.
            cargos (list[CargoLegislativo]): Lista de asistentes a la sesion.
            votaciones (list[Votacion]): Lista de Votaciones de la sesion
        """
        super(Sesion, self).__init__(**kwargs)
        self.numero = numero
        self.nombre = nombre
        self.descripcion = descripcion
        self.url = url

        self.numero_asistir = kwargs.get('numero_asistir')
        self.porc_asistencia = kwargs.get('porc_asistencia')
        self.numero_asistentes = kwargs.get('numero_asistentes')
        self.fecha = kwargs.get('fecha')

        camara = kwargs.get('camara')
        if camara:
            self.camara = camara
        else:
            self.camara_id = camara_id
        self.cargos = kwargs.get('cargos')
        self.votaciones = kwargs.get('votaciones')

    def __repr__(self):
        return f'<Sesion {self.id}: Camara={self.camara_id} Numero={self.numero} Fecha={self.fecha} Url={self.url}'

    def __str__(self):
        return f'Sesion {self.numero} de Camara {self.camara.nombre} ({self.fecha})'

from project_snitch import db

lista_pareado = db.Table(
    'lista_pareado',
    db.Column('pareo_id', db.Integer, db.ForeignKey('pareo.id'),
              primary_key=True),
    db.Column('cargo_legislativo_id', db.Integer,
              db.ForeignKey('cargo_legislativo.id'), primary_key=True)
)


class Pareo(db.Model):
    """
    Modelo SQLAlchemy de Pareo.

    Attributes:
        id (int): Id.
        votacion_id (int): Id de la votacion a la que pertenece el pareo.
        activo (bool): Esta activo en el sistema?

        votacion (Votacion): Votacion a la que pertenece el pareo.
        cargos (list[Cargos]): Cargos en el pareo.

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'pareo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    votacion_id = db.Column(db.Integer, db.ForeignKey('votacion.id'),
                            nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    votacion = db.relationship('Votacion', backref='pareos')
    cargos = db.relationship('CargoLegislativo', secondary=lista_pareado,
                             lazy='subquery',
                             backref=db.backref('pareos', lazy=True))

    def __init__(self,
                 votacion_id,
                 **kwargs):
        """

        Args:
            votacion_id (int): Id de la votacion a la que pertenece el pareo.

        Keyword Args:
            cargos (list[Cargos]): Cargos en el pareo.
        """
        super(Pareo, self).__init__(**kwargs)
        self.votacion_id = votacion_id
        self.cargos = kwargs.get('cargos')

    def __repr__(self):
        return f'<Pareo {self.id}: Votacion={self.votacion_id} Legisladores={self.legisladores}'

    def __str__(self):
        return f'Pareo {self.id} de {self.votacion}'

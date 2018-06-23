from app import db

circunscripcion_distritos = db.Table(
    'circunscripcion_distrito',
    db.Column('circunscripcion_id', db.Integer, db.ForeignKey('circunscripcion.id'), primary_key=True),
    db.Column('distrito_id', db.Integer, db.ForeignKey('distrito.id'), primary_key=True)
)


class Circunscripcion(db.Model):
    """
    Modelo SQLAlchemy de Circunscripción.

    Attributes:
    id (int): Id de Circunscripción.
    numero (int): Numero de la Circunscripción.
    antiguo (bool): Es de la legislación antigua? (pre 2018).
    activo (bool): Esta activo en el sistema?

    __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'circunscripcion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    numero = db.Column(db.Integer, nullable=False)
    antiguo = db.Column(db.Boolean, nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    
    distritos = db.relationship('Distrito', secondary=circunscripcion_distritos, lazy='subquery', backref=db.backref('circunscripcion', lazy=True))

    def __init__(self,
                 id,
                 numero='999',
                 antiguo=False,
                 **kwargs):
        """
        Args:
            id (int): Id en tabla.
            numero (int): Numero de la circunscripción.
            antiguo (bool): Legislación antigua (pre 2018).

        Keyword Args:
            distritos (list[Distritos]): Distritos de la Circunscripción.
        """
        super(Circunscripcion, self).__init__(**kwargs)

        self.id = id
        self.numero = numero
        self.antiguo = antiguo

        distritos = kwargs.get('distritos')
        if distritos:
            self.distritos = kwargs.get('distritos')

    def __str__(self):
        if self.antiguo:
            agrega = 'Antigua'
        else:
            agrega = 'Nueva'

        return f'{self.numero}, {agrega}'

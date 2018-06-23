from app import db


class Distrito(db.Model):
    """
    Modelo SQLAlchemy de Distrito.

    Attributes:
        id (int): Id del Distrito.
        numero (int): Numero del distrito.
        antiguo (bool): Es de la legislación antigua? (pre 2018).
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'distrito'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    numero = db.Column(db.Integer, nullable=False)
    antiguo = db.Column(db.Boolean, nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 id,
                 numero='999',
                 antiguo=False,
                 **kwargs):
        """

        Args:
            id (int): Id del Distrito.
            numero (int): Numero del distrito.
            antiguo (bool): Es de la legislación antigua? (pre 2018).
        """
        super(Distrito, self).__init__(**kwargs)

        self.id = id
        self.numero = numero
        self.antiguo = antiguo

    def __str__(self):
        if self.antiguo:
            agrega = 'Antiguo'
        else:
            agrega = 'Nuevo'

        return f'{self.numero}, {agrega}'

    def __repr__(self):
        return f'<Distrito {self.id}: {self.numero}, Antiguo={self.antiguo}>'

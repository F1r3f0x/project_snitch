from project_snitch import db


class Region(db.Model):
    """
    Modelo SQLAlchemy de Región.

    Attributes:
        id (int): Id de Región.
        numero (str): Numero Romano de la Región.
        nombre (str): Nombre de la Región.
        actvio (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.String(5), nullable=False)
    nombre = db.Column(db.String(256), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 nombre='nombreRegion',
                 numero='XXX',
                 **kwargs):
        """
        Args:
            nombre (str): Nombre región.
            numero (str): Numero romano región.
        """
        super(Region, self).__init__(**kwargs)

        self.nombre = nombre
        self.numero = numero

    def __str__(self):
        return f'{self.numero}, {self.nombre}'

    def __repr__(self):
        return f'<Region {self.id}: {self.numero}, {self.nombre}>'

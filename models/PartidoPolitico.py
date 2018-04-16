from app import db


class PartidoPolitico(db.Model):
    """
    Modelo SQLAlchemy de Partido Político.

    Attributes:
        id (int): Id del Partido.
        nombre (str): Nombre del Partido.
        logo_url (str): Url al logo del Partido
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'partido_politico'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), nullable=False)
    logo_url = db.Column(db.String(256), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 nombre='nombreEstado',
                 logo_url='logo.png',
                 **kwargs):
        """
        Args:
            nombre (str): Nombre del Partido.
            logo_url (str): Url al logo del Partido
        """
        super(PartidoPolitico, self).__init__(**kwargs)

        self.nombre = nombre
        self.logo_url = logo_url

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f'<PartidoPolitico {self.id}: {self.nombre}>'

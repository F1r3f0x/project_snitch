from app import db


class Voto(db.Model):
    """
    Modelo SQLAlchemy de Voto.

    Attributes:
        id (int): Id.
        nombre (str): Nombre.
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'voto'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 nombre='Voto',
                 **kwargs):
        """
        Args:
            nombre (str): Nombre.
        """
        super(Voto, self).__init__(**kwargs)
        self.nombre = nombre

    def __repr__(self):
        return f'<Voto {self.id}: {self.nombre}>'

    def __str__(self):
        return self.nombre

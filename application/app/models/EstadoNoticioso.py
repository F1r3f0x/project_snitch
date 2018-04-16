from app import db


class EstadoNoticioso(db.Model):
    """
    Modelo SQLAlchemy de Estado Noticioso.

    Attributes:
        id (int): Id del estado.
        nombre(str): Nombre del estado.
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'estado_noticioso'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 nombre='nombreEstado',
                 **kwargs):
        """
        Args:
            nombre(str): Nombre del estado.
        """
        super(EstadoNoticioso, self).__init__(**kwargs)

        self.nombre = nombre

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f'<EstadoNoticioso {self.id}: {self.nombre}>'

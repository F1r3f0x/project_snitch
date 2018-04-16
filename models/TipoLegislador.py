from app import db


class TipoLegislador(db.Model):
    """
    Modelo SQLAlchemy de Tipo de Legislador.

    Attributes:
        id (int): Id del Tipo.
        nombre (str): Nombre del Tipo.
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'tipo_legislador'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 nombre='nombreTipo',
                 **kwargs):
        """
        Args:
            nombre (str): Nombre del Tipo.
        """
        super(TipoLegislador, self).__init__(**kwargs)

        self.nombre = nombre

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f'<TipoLegislador {self.id}: {self.nombre}>'

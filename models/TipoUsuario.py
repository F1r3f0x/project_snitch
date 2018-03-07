from project_snitch import db


class TipoUsuario(db.Model):
    """
    Modelo SQLAlchemy de Tipo de Usuario.

    Attributes:
        id (int): Id del Tipo.
        nombre (str): Nombre del Tipo.
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'tipo_usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 nombre='Usuario Tipo',
                 **kwargs):
        """
        Args:
            id (int): Id del Tipo.
            nombre (str): Nombre del Tipo.
            activo (bool): Esta activo en el sistema?
        """
        super(TipoUsuario, self).__init__(**kwargs)
        self.nombre = nombre

    def __repr__(self):
        return f'<TipoUsuario {self.id}: {self.nombre}>'

    def __str__(self):
        return self.nombre

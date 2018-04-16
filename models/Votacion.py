from app import db


class Votacion(db.Model):
    """
    Modelo SQLAlchemy de Votacion en sesion.

    Attributes:
        id (int): Id.
        sesion_id (int): Id de Sesion a la que pertenece la votacion.
        proyecto_ley_id (int): Id del proyecto que se vota.
        descripcion (str): Descripcion.
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'votacion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sesion_id = db.Column(db.Integer, db.ForeignKey('sesion.id'), nullable=False)
    proyecto_ley_id = db.Column(db.Integer, db.ForeignKey('proyecto_ley.id'),
                                nullable=True)
    descripcion = db.Column(db.String(2048), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 id_sesion,
                 descripcion,
                 id_proyecto=None,
                 **kwargs):
        """
        Args:
            sesion_id (int): Id de Sesion a la que pertenece la votacion.
            proyecto_ley_id (int): Id del proyecto que se vota.
            descripcion (str): Descripcion.
        """
        super(Votacion, self).__init__(**kwargs)
        self.sesion_id = id_sesion
        self.proyecto_ley_id = id_proyecto
        self.descripcion = descripcion

    def __repr__(self):
        return f'<Votacion {self.id}: Sesion={self.sesion_id} Proyecto={self.proyecto_ley_id}'

    def __str__(self):
        return f'Votacion {self.id} de Sesion {self.sesion}'

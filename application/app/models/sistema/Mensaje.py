from datetime import datetime
from app import db


class Mensaje(db.Model):
    """
    Modelo SQLAlchemy de Mensajes para la pagina web.

    Attributes:
        id (int): Id.
        titulo (str): Titulo.
        contenido (str): contenido.
        fecha (datetime): Fecha creacion.
        autor_id (int): Id de autor del mensaje.
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'mensaje'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(512), nullable=False)
    contenido = db.Column(db.String(2048), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now())
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'),
                         nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    autor = db.relationship('Usuario', backref='mensajes', lazy=True)

    def __init__(self,
                 autor_id,
                 titulo='Nuevo Mensaje',
                 contenido='Contenido del nuevo mensaje.',
                 **kwargs):
        """
        Args:
            nombre (str): Nombre.
        """
        super(Mensaje, self).__init__(**kwargs)
        self.autor_id = autor_id
        self.titulo = titulo
        self.contenido = contenido

    def __repr__(self):
        return f'<Mensaje {self.id}: {self.titulo} {self.autor}> {{ {self.contenido} }}'

    def __str__(self):
        return f'{self.titulo}: {self.contenido}'

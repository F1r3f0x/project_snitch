from app import db
from datetime import datetime


class Periodo(db.Model):
    """
    Modelo SQLAlchemy de Periodo Legislativo.

    Attributes:
        id (int): Id del Periodo.
        nombre (str): Nombre del Periodo.
        anno_inicio (str): Año de inicio del Periodo.
        anno_fin (str): Año de término del Periodo (opcional).
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'periodo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(512), nullable=False)
    # God save the one without Unicode support
    anno_inicio = db.Column('año_inicio', db.Integer, nullable=False)
    anno_fin = db.Column('año_fin', db.Integer, nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 nombre='nombreTipo',
                 anno_inicio=datetime.now().year,
                 anno_fin=2018,
                 **kwargs):
        """
        Args:
            id (int): Id del Periodo.
            nombre (str): Nombre del Periodo.
            anno_inicio (str): Año de inicio del Periodo.
            anno_fin (str): Año de termino del Periodo (opcional).
        """
        super(Periodo, self).__init__(**kwargs)

        self.id = id
        self.nombre = nombre
        self.anno_inicio = anno_inicio
        self.anno_fin = anno_fin

    def __str__(self):
        return f'{self.nombre} ({self.anno_inicio} - {self.anno_fin})'

    def __repr__(self):
        return f'<PeriodoLegislativo {self.id}: {self.nombre} ({self.anno_inicio} - {self.anno_fin})>'

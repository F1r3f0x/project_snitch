from app import db
from datetime import datetime

cargo_distritos = db.Table(
    'distrito_cargo_legislativo',
    db.Column('cargo_legislativo_id', db.Integer,
              db.ForeignKey('cargo_legislativo.id'), primary_key=True),
    db.Column('distrito_id', db.Integer, db.ForeignKey('distrito.id'),
              primary_key=True)
)


class CargoLegislativo(db.Model):
    """
    Modelo SQLAlchemy de un Cargo Legislativo.

    Attributes:
        id (int): Id del registro.
        legislador_id (int): Id del legislador al que le pertenece el cargo.
        remuneracion (int): Remuneración que obtiene el legislador durante este cargo.
        tipo_legislador_id (int): Id del Tipo de legislador (Senador o Diputado).
        partido_politico_id (int): Id del Partido Político del cargo.
        periodo_id (int): Id del periodo legislativo del cargo.
        region_id (int): Id de la región en la que se asume el cargo.
        circunscripcion_id (int): Id del a circunscripción en la que se asume el cargo (opcional)
        id_interna (int): Id del legislador en el sistema interno correspondiente (Senado o Camara de Diputados).
        actvio (bool): Esta activo en el sistema?.

        legislador (Legislador): Legislador al que le pertenece el cargo.
        tipo (TipoLegislador): Tipo de Legislador (Senador o Diputado).
        region (Region): Región en la que se asume el cargo.
        partido (PartidoPolitico): Partido Político del cargo.
        periodo (Periodo): Período Legislativo del cargo.
        circunscripcion (Circunscripcion): Circunscripción en la que se asume el cargo.
        distritos (Distrito[]): Distritos en los que se asume el cargo.

        __tablename__ (str): Nombre de la tabla en la base de datos
    """

    __tablename__ = 'cargo_legislativo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    legislador_id = db.Column(db.String(256), db.ForeignKey('legislador.id'),
                              nullable=False, default=1)
    remuneracion = db.Column(db.Integer, nullable=True)
    tipo_legislador_id = db.Column(db.Integer,
                                   db.ForeignKey('tipo_legislador.id'),
                                   nullable=False, default=1)
    partido_politico_id = db.Column(db.Integer,
                                    db.ForeignKey('partido_politico.id'),
                                    nullable=False, default=9999)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'),
                           nullable=False, default=9)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'),
                          nullable=True)
    circunscripcion_id = db.Column(db.Integer,
                                   db.ForeignKey('circunscripcion.id'),
                                   nullable=True)
    id_interna = db.Column(db.Integer, nullable=True)
    fecha_ingreso = db.Column(db.Integer, nullable=False,
                              default=datetime.now())
    activo = db.Column('activo', db.Boolean, nullable=False, default=True)

    legislador = db.relationship('Legislador', backref='cargos')
    tipo = db.relationship('TipoLegislador', backref='cargos')
    region = db.relationship('Region', backref='cargos')
    partido = db.relationship('PartidoPolitico', backref='cargos')
    periodo = db.relationship('Periodo', backref='cargos')
    circunscripcion = db.relationship('Circunscripcion', backref='cargos')
    distritos = db.relationship('Distrito', secondary=cargo_distritos,
                                lazy='subquery',
                                backref=db.backref('cargos', lazy=True))

    def __init__(self,
                 remuneracion=9999,
                 **kwargs):
        """
        Args:
            remuneracion (int): Remuneración del legislador en el cargo.

        Keyword Args:
            legislador (Legislador): Legislador al que le pertenece el cargo.
            tipo (TipoLegislador): Tipo de Legislador (Senador o Diputado).
            region (Region): Región en la que se asume el cargo.
            partido (PartidoPolitico): Partido Político del cargo.
            periodo (Periodo): Período Legislativo del cargo.
            circunscripcion (Circunscripcion): Circunscripción en la que se asume el cargo.
            distritos (list[Distrito]): Lista de Distritos
            id_interna (int): Id interna en sistema donde se extrajo.
        """
        super(CargoLegislativo, self).__init__(**kwargs)

        if kwargs.get('legislador'):
            self.legislador = kwargs.get('legislador')
        if kwargs.get('tipo'):
            self.tipo = kwargs.get('tipo')
        if kwargs.get('region'):
            self.region = kwargs.get('region')
        if kwargs.get('partido'):
            self.partido = kwargs.get('partido')
        if kwargs.get('periodo'):
            self.periodo = kwargs.get('periodo')
        if kwargs.get('circunscripcion'):
            self.circunscripcion = kwargs.get('circunscripcion')
        if kwargs.get('id_interna'):
            self.id_interna = kwargs.get('id_interna')

        self.remuneracion = remuneracion

        distritos = kwargs.get('distritos')
        if distritos:
            self.distritos = kwargs.get('distritos')

    def add_distrito(self, distrito):
        """
        Agrega un Distrito a la lista de distritos del Cargo.
        Args:
            distrito (Distrito): el Distrito a agregar.

        Returns:
            int: Tamaño de nueva lista de distritos.
        """
        self.distritos.append(distrito)
        return len(self.distritos)

    def print_to_console(self):
        print(f'Cargo Legislativo en {self.periodo}')
        print(f'\tTipo: {self.tipo}')
        print(f'\tid_interna: {self.id_interna}')
        print(f'\tFecha Ingreso: {self.fecha_ingreso}')
        print(f'\tRegion: {self.region}')
        print(f'\tPartido: {self.partido}')
        print(f'\tCircunscripcion: {self.circunscripcion}')
        print(f'\tDistritos: {self.distritos}')

    def __repr__(self):
        return f'<CargoLegislativo {self.legislador}: Periodo={self.periodo}, Partido={self.partido}, Region={self.region}>'

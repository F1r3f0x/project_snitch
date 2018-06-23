from datetime import datetime
from app import db, ID_SENADOR
import app.my_tools.funciones as tools
from app.models.utilitaria.EnviableJSON import EnviableJSON

noticias_legislador = db.Table(
    'noticia_legislador',
    db.Column('noticia_id', db.Integer,
              db.ForeignKey('noticia.id'), primary_key=True),
    db.Column('legislador_id', db.Integer, db.ForeignKey('legislador.id'),
              primary_key=True)
)


class Legislador(db.Model, EnviableJSON):
    """
    Modelo SQLAlchemy de Legislador.

    Attributes:
        id (int): Id del Legislador.
        primer_nombre (str): Primer Nombre.
        segundo_nombre (str): Segundo Nombre.
        primer_apellido (str): Primer Apellido.
        segundo_apellido (str): Segundo Apellido.
        texto_buscable (str): Texto buscable con el nombre del Legislador para Whoosh.
        sexo (bool): True para Hombre, False para Mujer o Null.
        email (str): Email.
        telefono (str): Teléfono.
        foto_url (str): Url de la foto del Legislador.
        buscar_noticias (bool): Buscar noticias del Legislador?
        estado_noticioso_id (int): Id del Estado Noticioso del Legislador.
        ultimo_tipo_legislador_id: Id del ultimo Tipo de Legislador del Legislador para filtrar.
        activo (bool): Esta activo en el sistema?

        estado_noticioso (EstadoNoticioso): Estado Noticioso del Legislador.

        noticias (Noticia): Lista de noticias en las que aparece el Legislador.

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'legislador'
    __searchable__ = ['texto_buscable', 'primer_nombre', 'primer_apellido']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primer_nombre = db.Column(db.String(256), nullable=False)
    segundo_nombre = db.Column(db.String(256), nullable=True)
    primer_apellido = db.Column(db.String(256), nullable=False)
    segundo_apellido = db.Column(db.String(256), nullable=True)
    texto_buscable = db.Column(db.String(1027), nullable=True)
    sexo = db.Column(db.Boolean, nullable=True)
    email = db.Column(db.String(1024), nullable=True)
    telefono = db.Column(db.String(64), nullable=True)
    foto_url = db.Column(db.String(256), nullable=True)
    buscar_noticias = db.Column(db.Boolean(), nullable=True)
    estado_noticioso_id = db.Column(db.Integer,
                                    db.ForeignKey('estado_noticioso.id'),
                                    nullable=True)
    # Agregar setter
    ultimo_tipo_legislador_id = db.Column(db.Integer,
                                          db.ForeignKey('tipo_legislador.id'),
                                          nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False,
                              default=datetime.now())
    activo = db.Column(db.Boolean, nullable=False, default=True)

    ultimo_tipo_legislador = db.relationship('TipoLegislador')
    estado_noticioso = db.relationship('EstadoNoticioso',
                                       backref='legisladores')
    noticias = db.relationship('Noticia', secondary=noticias_legislador,
                               lazy='subquery',
                               backref=db.backref('legisladores', lazy=True))

    def __init__(self,
                 primer_nombre='nombre',
                 segundo_nombre='',
                 primer_apellido='apellido',
                 segundo_apellido='',
                 sexo=None,
                 email='',
                 telefono='',
                 foto_url='',
                 buscar_noticias=False,
                 **kwargs):
        """
        Args:
            primer_nombre (str): Primer Nombre.
            segundo_nombre (str): Segundo Nombre.
            primer_apellido (str): Primer Apellido.
            segundo_apellido (str): Segundo Apellido.
            sexo (bool): True para Hombre, False para Mujer o Null.
            email (str): Email.
            telefono (str): Teléfono.
            foto_url (str): Url de la foto del Legislador.
            buscar_noticias (bool): Buscar noticias del Legislador?

        Keyword Args:
            estado_noticioso_id (int): Id del Estado Noticioso del Legislador.
            estado_noticioso (EstadoNoticioso): Estado Noticioso del Legislador.
            noticias (list[Noticias]): Lista de Noticias en las que el Legislador es mencionado.
        """
        super(Legislador, self).__init__(**kwargs)

        self.primer_nombre = primer_nombre
        self.segundo_nombre = segundo_nombre
        self.primer_apellido = primer_apellido
        self.segundo_nombre = segundo_apellido
        self.texto_buscable = tools.get_texto_buscable(f'{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}')
        self.sexo = sexo
        self.email = email
        self.telefono = telefono
        self.foto_url = foto_url
        self.buscar_noticias = buscar_noticias

        estado_noticioso_id = kwargs.get('estado_noticioso_id')
        if estado_noticioso_id:
            self.estado_noticioso_id = estado_noticioso_id

        estado_noticioso = kwargs.get('estado_noticioso')
        if estado_noticioso:
            self.estado_noticioso = estado_noticioso_id

        noticias = kwargs.get('noticias')
        if noticias:
            self.noticias = noticias

    def is_senador(self):
        return self.ultimo_tipo_legislador_id == ID_SENADOR

    def print_to_console(self):
        print(f'Legislador: {self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido}')
        print(f'\tEmail: {self.email}')
        print(f'\tTelefono: {self.telefono}')
        print(f'\tUltimo Tipo id: {self.ultimo_tipo_legislador_id}')
        print(f'\tCargos:')
        for _c in self.cargos:
            print(f'\t\t{_c.__repr__()}')

    def __repr__(self):
        return f'<Legislador {self.id}: {self.primer_apellido}, {self.primer_nombre}>'

    def __str__(self):
        return f'{self.primer_nombre} {self.primer_apellido} {self.segundo_apellido}'

    def json_dict(self):
        noticias = None
        if self.noticias:
            noticias = []
            for _n in self.noticias:
                noticias.append(_n.id)

        cargos = None
        if self.cargos:
            cargos = []
            for _c in self.cargos:
                cargos.append(_c.id)

        dict_legislador = {
            'id': self.id,
            'primer_nombre': self.primer_nombre,
            'segundo_nombre': self.segundo_nombre,
            'primer_apellido': self.primer_apellido,
            'segundo_apellido': self.segundo_apellido,
            'texto_buscable': self.texto_buscable,
            'sexo (es Hombre)': self.sexo,
            'email': self.email,
            'telefono': self.telefono,
            'foto_url': self.foto_url,
            'buscar_noticias': self.buscar_noticias,
            'estado_noticioso_id': self.estado_noticioso_id,
            'ultimo_tipo_self_id': self.ultimo_tipo_legislador_id,
            'noticias_ids': noticias,
            'cargos_ids': cargos,
            'activo': self.activo
        }

        return dict_legislador

    def ajax_dict(self):
        return 'hola'
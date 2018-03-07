from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin  # Agrega a la clase metodos necesarios para flask_login
from project_snitch import db, ID_ADMIN, ID_USER, ID_EDITOR

favorito = db.Table(
    'favorito',
    db.Column('usuario_id', db.Integer,
              db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('legislador_id', db.Integer, db.ForeignKey('legislador.id'), primary_key=True),
    db.Column('fecha', db.DateTime, nullable=False, default=datetime.now())
)


class Usuario(db.Model, UserMixin):
    """
    Modelo SQLAlchemy de Usuario.

    Attributes:
        id (int): Id del Usuario.
        nombre (str): Nombre.
        email (str): Email.
        fecha_registro (datetime): Fecha del registro en el sistema.
        fecha_confirmacion (datetime): Fecha de recepcion de la confirmacion
        password_hash (str): Contraseña cifrada del Usuario.
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.now())
    fecha_confirmacion = db.Column(db.DateTime, nullable=True)
    password_hash = db.Column(db.String(4096), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    tipo_usuario_id = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'))

    tipo = db.relationship('TipoUsuario', backref='usuarios', lazy=True)
    favoritos = db.relationship('Legislador',
                                secondary=favorito,
                                lazy='subquery',
                                backref=db.backref('seguidores', lazy=True))

    def __init__(self,
                 nombre='Usuario Nombre',
                 email='mail@mail.cl',
                 password='pass123',
                 tipo_usuario=2,
                 **kwargs):
        """
        Args:
            id (int): Id del Usuario.
            nombre (str): Nombre.
            email (str): Email.
            password_hash (str): Contraseña cifrada del Usuario.

        Keyword Args:
            favoritos (list[Legislador]): Lista de Favoritos del Usuario
        """
        super(Usuario, self).__init__(**kwargs)

        self.nombre = nombre
        self.email = email
        self.password = password
        self.tipo_usuario_id = tipo_usuario

        favoritos = kwargs.get('favoritos')
        if favoritos:
            self.favoritos = kwargs.get('favoritos')

    def is_admin(self):
        return self.tipo_usuario_id == ID_ADMIN

    def is_pleb(self):
        return self.tipo_usuario_id == ID_USER

    def is_editor(self):
        return self.tipo_usuario_id == ID_EDITOR

    def add_favorito(self, legislador):
        """
        Agrega un Legislador favorito a la lista de Favoritos del Usuario
        Args:
            legislador (Legislador): el Legislador a agregar.

        Returns:
            int: Tamaño de nueva lista de Favoritos.
        """
        self.favoritos.append(legislador)
        return len(self.favoritos)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, pass_to_check):
        """
        Compara una contraseña en texto plano con la contraseña
        cifrada del usuario.

        Args:
            pass_to_check (str): Contraseña a comparar

        Returns:
            bool: True si es correcta. False si es incorrecta.
        """
        return check_password_hash(self.password_hash, pass_to_check)

    def __repr__(self):
        return f'<Usuario {self.id}: {self.nombre} - {self.email}>'

from app import db


class VotoVotacion(db.Model):
    """
    Modelo SQLAlchemy de Voto de Votacion.

    Attributes:
        votacion_id (int): Id de votacion.
        cargo_legislativo_id (str): Id de legislador votante.
        voto_id (inr): Id tipo de voto.

        votacion (Votacion): Votacion del voto
        votante (CargoLegislativo): Votante
        voto (Voto): Tipo del voto

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'lista_votos'

    votacion_id = db.Column(db.Integer, db.ForeignKey('votacion.id'),
                            primary_key=True, nullable=False)
    cargo_legislativo_id = db.Column(db.Integer,
                                     db.ForeignKey('cargo_legislativo.id'),
                                     primary_key=True,
                                     nullable=False)
    voto_id = db.Column(db.Integer, db.ForeignKey('voto.id'), nullable=False)

    votacion = db.relationship('Votacion', backref='lista_votos')
    votante = db.relationship('CargoLegislativo', backref='votos')
    voto = db.relationship('Voto')

    def __init__(self,
                 votacion_id,
                 cargo_legislativo_id,
                 voto_id,
                 **kwargs):
        """
        Args:
            votacion_id (int): Id de votacion.
            cargo_legislativo_id (str): Id de legislador votante.
            voto_id (inr): Id tipo de voto.
        """
        super(VotoVotacion, self).__init__(**kwargs)
        self.votacion_id = votacion_id
        self.cargo_legislativo_id = cargo_legislativo_id
        self.voto_id = voto_id

    def __repr__(self):
        return f'<VotoVotacion {self.id}: {self.nombre}>'

    def __str__(self):
        return f'Voto de {self.votacion_id}'

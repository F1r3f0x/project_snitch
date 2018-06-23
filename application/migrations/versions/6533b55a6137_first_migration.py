"""first migration

Revision ID: 6533b55a6137
Revises: 
Create Date: 2018-06-22 20:52:40.984731

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6533b55a6137'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('camara',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('circunscripcion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=False),
    sa.Column('antiguo', sa.Boolean(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('distrito',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=False),
    sa.Column('antiguo', sa.Boolean(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('estado_noticioso',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fuente_noticias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('url', sa.String(length=256), nullable=False),
    sa.Column('spider_extraccion', sa.String(length=1024), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('partido_politico',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('logo_url', sa.String(length=256), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('periodo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=512), nullable=False),
    sa.Column('año_inicio', sa.Integer(), nullable=False),
    sa.Column('año_fin', sa.Integer(), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('numero', sa.String(length=5), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tipo_legislador',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tipo_usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('voto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('circunscripcion_distrito',
    sa.Column('circunscripcion_id', sa.Integer(), nullable=False),
    sa.Column('distrito_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['circunscripcion_id'], ['circunscripcion.id'], ),
    sa.ForeignKeyConstraint(['distrito_id'], ['distrito.id'], ),
    sa.PrimaryKeyConstraint('circunscripcion_id', 'distrito_id')
    )
    op.create_table('legislador',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('primer_nombre', sa.String(length=256), nullable=False),
    sa.Column('segundo_nombre', sa.String(length=256), nullable=True),
    sa.Column('primer_apellido', sa.String(length=256), nullable=False),
    sa.Column('segundo_apellido', sa.String(length=256), nullable=True),
    sa.Column('texto_buscable', sa.String(length=1027), nullable=True),
    sa.Column('sexo', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=1024), nullable=True),
    sa.Column('telefono', sa.String(length=64), nullable=True),
    sa.Column('foto_url', sa.String(length=256), nullable=True),
    sa.Column('buscar_noticias', sa.Boolean(), nullable=True),
    sa.Column('estado_noticioso_id', sa.Integer(), nullable=True),
    sa.Column('ultimo_tipo_legislador_id', sa.Integer(), nullable=True),
    sa.Column('fecha_ingreso', sa.DateTime(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['estado_noticioso_id'], ['estado_noticioso.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('noticia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=256), nullable=False),
    sa.Column('contenido_texto', mysql.MEDIUMTEXT(unicode=True), nullable=True),
    sa.Column('url', sa.String(length=1024), nullable=False),
    sa.Column('preview_url', sa.String(length=1024), nullable=True),
    sa.Column('titulo_buscable', sa.String(length=256), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('fuente_noticias_id', sa.Integer(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['fuente_noticias_id'], ['fuente_noticias.id'], ),
    sa.PrimaryKeyConstraint('id', 'fuente_noticias_id')
    )
    op.create_table('proyecto_ley',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('descripcion', sa.String(length=2048), nullable=True),
    sa.Column('camara_origen_id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('url', sa.String(length=1024), nullable=False),
    sa.Column('nombre_buscable', sa.String(length=256), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['camara_origen_id'], ['camara.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sesion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=False),
    sa.Column('camara_id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=True),
    sa.Column('descripcion', sa.String(length=256), nullable=True),
    sa.Column('numero_asisitr', sa.Integer(), nullable=True),
    sa.Column('porc_asistencia', sa.Integer(), nullable=True),
    sa.Column('numero_asistentes', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=1024), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['camara_id'], ['camara.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=256), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('fecha_registro', sa.DateTime(), nullable=False),
    sa.Column('fecha_confirmacion', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=4096), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.Column('tipo_usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tipo_usuario_id'], ['tipo_usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('cargo_legislativo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('legislador_id', sa.Integer(), nullable=False),
    sa.Column('remuneracion', sa.Integer(), nullable=True),
    sa.Column('tipo_legislador_id', sa.Integer(), nullable=False),
    sa.Column('partido_politico_id', sa.Integer(), nullable=False),
    sa.Column('periodo_id', sa.Integer(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('circunscripcion_id', sa.Integer(), nullable=True),
    sa.Column('id_interna', sa.Integer(), nullable=True),
    sa.Column('fecha_ingreso', sa.Integer(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['circunscripcion_id'], ['circunscripcion.id'], ),
    sa.ForeignKeyConstraint(['legislador_id'], ['legislador.id'], ),
    sa.ForeignKeyConstraint(['partido_politico_id'], ['partido_politico.id'], ),
    sa.ForeignKeyConstraint(['periodo_id'], ['periodo.id'], ),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.ForeignKeyConstraint(['tipo_legislador_id'], ['tipo_legislador.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorito',
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('legislador_id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['legislador_id'], ['legislador.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('usuario_id', 'legislador_id')
    )
    op.create_table('noticia_legislador',
    sa.Column('noticia_id', sa.Integer(), nullable=False),
    sa.Column('legislador_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['legislador_id'], ['legislador.id'], ),
    sa.ForeignKeyConstraint(['noticia_id'], ['noticia.id'], ),
    sa.PrimaryKeyConstraint('noticia_id', 'legislador_id')
    )
    op.create_table('votacion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sesion_id', sa.Integer(), nullable=False),
    sa.Column('proyecto_ley_id', sa.Integer(), nullable=True),
    sa.Column('descripcion', sa.String(length=2048), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['proyecto_ley_id'], ['proyecto_ley.id'], ),
    sa.ForeignKeyConstraint(['sesion_id'], ['sesion.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('autores_proyecto',
    sa.Column('cargo_legislativo_id', sa.Integer(), nullable=False),
    sa.Column('proyecto_ley_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cargo_legislativo_id'], ['cargo_legislativo.id'], ),
    sa.ForeignKeyConstraint(['proyecto_ley_id'], ['proyecto_ley.id'], ),
    sa.PrimaryKeyConstraint('cargo_legislativo_id', 'proyecto_ley_id')
    )
    op.create_table('distrito_cargo_legislativo',
    sa.Column('cargo_legislativo_id', sa.Integer(), nullable=False),
    sa.Column('distrito_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cargo_legislativo_id'], ['cargo_legislativo.id'], ),
    sa.ForeignKeyConstraint(['distrito_id'], ['distrito.id'], ),
    sa.PrimaryKeyConstraint('cargo_legislativo_id', 'distrito_id')
    )
    op.create_table('lista_asistencia',
    sa.Column('sesion_id', sa.Integer(), nullable=False),
    sa.Column('cargo_legislativo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cargo_legislativo_id'], ['cargo_legislativo.id'], ),
    sa.ForeignKeyConstraint(['sesion_id'], ['sesion.id'], ),
    sa.PrimaryKeyConstraint('sesion_id', 'cargo_legislativo_id')
    )
    op.create_table('lista_votos',
    sa.Column('votacion_id', sa.Integer(), nullable=False),
    sa.Column('cargo_legislativo_id', sa.Integer(), nullable=False),
    sa.Column('voto_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cargo_legislativo_id'], ['cargo_legislativo.id'], ),
    sa.ForeignKeyConstraint(['votacion_id'], ['votacion.id'], ),
    sa.ForeignKeyConstraint(['voto_id'], ['voto.id'], ),
    sa.PrimaryKeyConstraint('votacion_id', 'cargo_legislativo_id')
    )
    op.create_table('pareo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('votacion_id', sa.Integer(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['votacion_id'], ['votacion.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lista_pareado',
    sa.Column('pareo_id', sa.Integer(), nullable=False),
    sa.Column('cargo_legislativo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cargo_legislativo_id'], ['cargo_legislativo.id'], ),
    sa.ForeignKeyConstraint(['pareo_id'], ['pareo.id'], ),
    sa.PrimaryKeyConstraint('pareo_id', 'cargo_legislativo_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lista_pareado')
    op.drop_table('pareo')
    op.drop_table('lista_votos')
    op.drop_table('lista_asistencia')
    op.drop_table('distrito_cargo_legislativo')
    op.drop_table('autores_proyecto')
    op.drop_table('votacion')
    op.drop_table('noticia_legislador')
    op.drop_table('favorito')
    op.drop_table('cargo_legislativo')
    op.drop_table('usuario')
    op.drop_table('sesion')
    op.drop_table('proyecto_ley')
    op.drop_table('noticia')
    op.drop_table('legislador')
    op.drop_table('circunscripcion_distrito')
    op.drop_table('voto')
    op.drop_table('tipo_usuario')
    op.drop_table('tipo_legislador')
    op.drop_table('region')
    op.drop_table('periodo')
    op.drop_table('partido_politico')
    op.drop_table('fuente_noticias')
    op.drop_table('estado_noticioso')
    op.drop_table('distrito')
    op.drop_table('circunscripcion')
    op.drop_table('camara')
    # ### end Alembic commands ###

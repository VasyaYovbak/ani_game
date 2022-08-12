"""empty message

Revision ID: 194910d99592
Revises: 
Create Date: 2021-11-17 16:38:45.196776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '194910d99592'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('image', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('character_id')
    )
    op.create_table('token_block_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('permission', sa.String(length=30), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('image', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('guested_character_id', sa.Integer(), nullable=True),
    sa.Column('unguested_character_id', sa.Integer(), nullable=True),
    sa.Column('winner_id', sa.Integer(), nullable=True),
    sa.Column('loser_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('chat', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['guested_character_id'], ['character.character_id'], ),
    sa.ForeignKeyConstraint(['loser_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['unguested_character_id'], ['character.character_id'], ),
    sa.ForeignKeyConstraint(['winner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('game_id')
    )
    op.create_table('user_queue',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('card',
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('is_selected_hero', sa.Boolean(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.character_id'], ),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('user_queue')
    op.drop_table('game')
    op.drop_table('user')
    op.drop_table('token_block_list')
    op.drop_table('character')
    # ### end Alembic commands ###


# User Achievements
    # op.create_table('achievement',
    # sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    # sa.Column('name', sa.String(length=30), nullable=False),
    # sa.Column('experience', sa.Integer(), nullable=False),
    # sa.Column('description', sa.String(length=120), nullable=False),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_table('user_achievement',
    # sa.Column('user_id', sa.Integer(), nullable=False),
    # sa.Column('achievement_id', sa.Integer(), nullable=False),
    # sa.ForeignKeyConstraint(['achievement_id'], ['achievement.id'], ),
    # sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    # sa.PrimaryKeyConstraint('user_id', 'achievement_id')
    # )
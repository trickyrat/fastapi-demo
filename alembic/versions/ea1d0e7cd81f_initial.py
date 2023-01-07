"""initial

Revision ID: ea1d0e7cd81f
Revises: 
Create Date: 2022-10-02 22:53:49.355574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea1d0e7cd81f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_authors_id', table_name='authors')
    op.drop_table('authors')
    op.drop_index('ix_books_id', table_name='books')
    op.drop_index('ix_books_isbn', table_name='books')
    op.drop_index('ix_books_title', table_name='books')
    op.drop_table('books')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.TEXT(length=256), nullable=True),
    sa.Column('price', sa.NUMERIC(precision=18, scale=2), nullable=True),
    sa.Column('isbn', sa.TEXT(length=13), nullable=True),
    sa.Column('publish_date', sa.TEXT(length=10), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.Column('author_id', sa.INTEGER(), nullable=True),
    sa.Column('cover_img', sa.TEXT(length=256), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_books_title', 'books', ['title'], unique=False)
    op.create_index('ix_books_isbn', 'books', ['isbn'], unique=False)
    op.create_index('ix_books_id', 'books', ['id'], unique=False)
    op.create_table('authors',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=32), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=32), nullable=True),
    sa.Column('full_name', sa.VARCHAR(length=65), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_authors_id', 'authors', ['id'], unique=False)
    # ### end Alembic commands ###

"""add quiz_results

Revision ID: a1b2c3d4e5f6
Revises: e5ed4b089dd1
Create Date: 2026-07-28 14:40:00.000000

"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'

down_revision: Union[str, None] = 'e5ed4b089dd1'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:

    op.create_table('quiz_results',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('quiz_id', sa.Uuid(), nullable=False),

    sa.Column('student_id', sa.Uuid(), nullable=False),

    sa.Column('score', sa.Integer(), nullable=False),

    sa.Column('total', sa.Integer(), nullable=False),

    sa.Column('created_at', sa.DateTime(), nullable=False),

    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['student_id'], ['users.id']),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_quiz_results_quiz_id'), 'quiz_results', ['quiz_id'], unique=False)

    op.create_index(op.f('ix_quiz_results_school_id'), 'quiz_results', ['school_id'], unique=False)

    op.create_index(op.f('ix_quiz_results_student_id'), 'quiz_results', ['student_id'], unique=False)

def downgrade() -> None:

    op.drop_index(op.f('ix_quiz_results_student_id'), table_name='quiz_results')

    op.drop_index(op.f('ix_quiz_results_school_id'), table_name='quiz_results')

    op.drop_index(op.f('ix_quiz_results_quiz_id'), table_name='quiz_results')

    op.drop_table('quiz_results')


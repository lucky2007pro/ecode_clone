"""add courses.teacher_id

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-07-28 17:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

revision: str = 'd4e5f6a7b8c9'

down_revision: Union[str, None] = 'c3d4e5f6a7b8'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:

    op.add_column('courses', sa.Column('teacher_id', sa.Uuid(), nullable=True))

    op.create_index(op.f('ix_courses_teacher_id'), 'courses', ['teacher_id'], unique=False)

    op.create_foreign_key('fk_courses_teacher_id', 'courses', 'users', ['teacher_id'], ['id'], ondelete='SET NULL')

def downgrade() -> None:

    op.drop_constraint('fk_courses_teacher_id', 'courses', type_='foreignkey')

    op.drop_index(op.f('ix_courses_teacher_id'), table_name='courses')

    op.drop_column('courses', 'teacher_id')


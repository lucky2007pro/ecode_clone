"""add messages.course_id

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-07-28 16:30:00.000000

"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

revision: str = 'c3d4e5f6a7b8'

down_revision: Union[str, None] = 'b2c3d4e5f6a7'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:

    op.add_column('messages', sa.Column('course_id', sa.Uuid(), nullable=True))

    op.create_index(op.f('ix_messages_course_id'), 'messages', ['course_id'], unique=False)

    op.create_foreign_key('fk_messages_course_id', 'messages', 'courses', ['course_id'], ['id'], ondelete='CASCADE')

def downgrade() -> None:

    op.drop_constraint('fk_messages_course_id', 'messages', type_='foreignkey')

    op.drop_index(op.f('ix_messages_course_id'), table_name='messages')

    op.drop_column('messages', 'course_id')


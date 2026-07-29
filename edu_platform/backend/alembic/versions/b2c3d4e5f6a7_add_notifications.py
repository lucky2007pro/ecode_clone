"""add notifications

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-07-28 15:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

revision: str = 'b2c3d4e5f6a7'

down_revision: Union[str, None] = 'a1b2c3d4e5f6'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:

    op.create_table('notifications',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('user_id', sa.Uuid(), nullable=False),

    sa.Column('title', sa.String(length=255), nullable=False),

    sa.Column('body', sa.Text(), nullable=True),

    sa.Column('is_read', sa.Boolean(), nullable=False),

    sa.Column('created_at', sa.DateTime(), nullable=False),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_notifications_school_id'), 'notifications', ['school_id'], unique=False)

    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)

def downgrade() -> None:

    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')

    op.drop_index(op.f('ix_notifications_school_id'), table_name='notifications')

    op.drop_table('notifications')


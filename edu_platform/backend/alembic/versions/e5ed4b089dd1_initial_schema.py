"""initial schema

Revision ID: e5ed4b089dd1
Revises:
Create Date: 2026-07-28 18:27:09.056458

"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

revision: str = 'e5ed4b089dd1'

down_revision: Union[str, Sequence[str], None] = None

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:

    """Upgrade schema."""

    op.create_table('payments',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),

    sa.Column('provider', sa.String(length=50), nullable=False),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_table('users',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('email', sa.String(length=255), nullable=False),

    sa.Column('hashed_password', sa.String(length=255), nullable=False),

    sa.Column('full_name', sa.String(length=255), nullable=False),

    sa.Column('role', sa.Enum('student', 'curator', 'manager', 'accountant', 'teacher', 'admin', name='role'), nullable=False),

    sa.Column('is_active', sa.Boolean(), nullable=False),

    sa.Column('balance', sa.Float(), nullable=False),

    sa.Column('level', sa.String(length=20), nullable=False),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    op.create_table('videos',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('kinescope_id', sa.String(length=100), nullable=False),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_table('schools',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('name', sa.String(length=255), nullable=False),

    sa.Column('subdomain', sa.String(length=100), nullable=False),

    sa.Column('custom_domain', sa.String(length=255), nullable=True),

    sa.Column('primary_color', sa.String(length=20), nullable=False),

    sa.Column('is_active', sa.Boolean(), nullable=False),

    sa.Column('owner_id', sa.Uuid(), nullable=False),

    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_schools_subdomain'), 'schools', ['subdomain'], unique=True)

    op.create_table('api_keys',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('key', sa.String(length=255), nullable=False),

    sa.Column('name', sa.String(length=100), nullable=False),

    sa.Column('created_at', sa.DateTime(), nullable=False),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_api_keys_key'), 'api_keys', ['key'], unique=True)

    op.create_index(op.f('ix_api_keys_school_id'), 'api_keys', ['school_id'], unique=False)

    op.create_table('courses',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('title', sa.String(length=255), nullable=False),

    sa.Column('slug', sa.String(length=255), nullable=False),

    sa.Column('description', sa.Text(), nullable=True),

    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id'),

    sa.UniqueConstraint('slug')

    )

    op.create_index(op.f('ix_courses_school_id'), 'courses', ['school_id'], unique=False)

    op.create_table('crm_leads',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=True),

    sa.Column('student_id', sa.Uuid(), nullable=True),

    sa.Column('kommo_id', sa.Integer(), nullable=False),

    sa.Column('status', sa.String(length=50), nullable=False),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='SET NULL'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_table('kommo_settings',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('subdomain', sa.String(length=100), nullable=True),

    sa.Column('client_id', sa.String(length=255), nullable=True),

    sa.Column('client_secret', sa.String(length=255), nullable=True),

    sa.Column('access_token', sa.String(length=1000), nullable=True),

    sa.Column('refresh_token', sa.String(length=1000), nullable=True),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id'),

    sa.UniqueConstraint('school_id')

    )

    op.create_table('marketing_settings',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('facebook_pixel_id', sa.String(length=100), nullable=True),

    sa.Column('google_analytics_id', sa.String(length=100), nullable=True),

    sa.Column('yandex_metrika_id', sa.String(length=100), nullable=True),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id'),

    sa.UniqueConstraint('school_id')

    )

    op.create_table('messages',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('sender_id', sa.Uuid(), nullable=False),

    sa.Column('receiver_id', sa.Uuid(), nullable=True),

    sa.Column('content', sa.Text(), nullable=False),

    sa.Column('created_at', sa.DateTime(), nullable=False),

    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_messages_receiver_id'), 'messages', ['receiver_id'], unique=False)

    op.create_index(op.f('ix_messages_school_id'), 'messages', ['school_id'], unique=False)

    op.create_index(op.f('ix_messages_sender_id'), 'messages', ['sender_id'], unique=False)

    op.create_table('school_subscriptions',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('plan_name', sa.String(length=100), nullable=False),

    sa.Column('status', sa.Enum('ACTIVE', 'PAST_DUE', 'CANCELED', name='subscriptionstatus'), nullable=False),

    sa.Column('expires_at', sa.DateTime(), nullable=False),

    sa.Column('created_at', sa.DateTime(), nullable=False),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_school_subscriptions_school_id'), 'school_subscriptions', ['school_id'], unique=False)

    op.create_table('telegram_bot_settings',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('bot_token', sa.String(length=255), nullable=True),

    sa.Column('private_channel_id', sa.String(length=100), nullable=True),

    sa.Column('invite_link', sa.String(length=255), nullable=True),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id'),

    sa.UniqueConstraint('school_id')

    )

    op.create_table('transactions',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('user_id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=True),

    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),

    sa.Column('type', sa.Enum('IN', 'OUT', name='transactiontype'), nullable=False),

    sa.Column('description', sa.String(length=255), nullable=False),

    sa.Column('created_at', sa.DateTime(), nullable=False),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_transactions_school_id'), 'transactions', ['school_id'], unique=False)

    op.create_index(op.f('ix_transactions_user_id'), 'transactions', ['user_id'], unique=False)

    op.create_table('user_schools',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('user_id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='membershipstatus'), nullable=False),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ),

    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_table('enrollments',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('user_id', sa.Uuid(), nullable=False),

    sa.Column('course_id', sa.Uuid(), nullable=False),

    sa.Column('status', sa.Enum('active', 'completed', 'expired', name='enrollmentstatus'), nullable=False),

    sa.Column('progress', sa.Float(), nullable=False),

    sa.Column('source', sa.String(length=20), nullable=False),

    sa.Column('created_at', sa.DateTime(), nullable=False),

    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_enrollments_course_id'), 'enrollments', ['course_id'], unique=False)

    op.create_index(op.f('ix_enrollments_school_id'), 'enrollments', ['school_id'], unique=False)

    op.create_index(op.f('ix_enrollments_user_id'), 'enrollments', ['user_id'], unique=False)

    op.create_table('modules',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('course_id', sa.Uuid(), nullable=False),

    sa.Column('title', sa.String(length=255), nullable=False),

    sa.Column('order', sa.Integer(), nullable=False),

    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_modules_course_id'), 'modules', ['course_id'], unique=False)

    op.create_index(op.f('ix_modules_school_id'), 'modules', ['school_id'], unique=False)

    op.create_table('payment_plans',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('course_id', sa.Uuid(), nullable=False),

    sa.Column('name', sa.String(length=255), nullable=False),

    sa.Column('plan_type', sa.Enum('ONE_TIME', 'INSTALLMENT', 'SUBSCRIPTION', name='plantype'), nullable=False),

    sa.Column('price', sa.Float(), nullable=False),

    sa.Column('months', sa.Integer(), nullable=False),

    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_payment_plans_course_id'), 'payment_plans', ['course_id'], unique=False)

    op.create_index(op.f('ix_payment_plans_school_id'), 'payment_plans', ['school_id'], unique=False)

    op.create_table('lessons',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('course_id', sa.Uuid(), nullable=False),

    sa.Column('module_id', sa.Uuid(), nullable=True),

    sa.Column('title', sa.String(length=255), nullable=False),

    sa.Column('content', sa.Text(), nullable=True),

    sa.Column('video_url', sa.String(length=500), nullable=True),

    sa.Column('lesson_type', sa.Enum('video', 'text', 'quiz', name='lessontype'), nullable=False),

    sa.Column('order', sa.Integer(), nullable=False),

    sa.Column('duration_minutes', sa.Integer(), nullable=False),

    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),

    sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_lessons_course_id'), 'lessons', ['course_id'], unique=False)

    op.create_index(op.f('ix_lessons_module_id'), 'lessons', ['module_id'], unique=False)

    op.create_index(op.f('ix_lessons_school_id'), 'lessons', ['school_id'], unique=False)

    op.create_table('subscriptions',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('user_id', sa.Uuid(), nullable=False),

    sa.Column('plan_id', sa.Uuid(), nullable=False),

    sa.Column('status', sa.Enum('ACTIVE', 'PAST_DUE', 'CANCELED', name='subscriptionstatus'), nullable=False),

    sa.Column('next_payment_date', sa.DateTime(), nullable=False),

    sa.Column('auto_charge', sa.Boolean(), nullable=False),

    sa.ForeignKeyConstraint(['plan_id'], ['payment_plans.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_subscriptions_school_id'), 'subscriptions', ['school_id'], unique=False)

    op.create_index(op.f('ix_subscriptions_user_id'), 'subscriptions', ['user_id'], unique=False)

    op.create_table('homework_submissions',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('lesson_id', sa.Uuid(), nullable=False),

    sa.Column('student_id', sa.Uuid(), nullable=False),

    sa.Column('submission_text', sa.Text(), nullable=False),

    sa.Column('status', sa.Enum('Sent for Review', 'Approved', 'Rejected', name='homeworkstatus'), nullable=False),

    sa.Column('grade', sa.Integer(), nullable=True),

    sa.Column('feedback', sa.Text(), nullable=True),

    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_homework_submissions_lesson_id'), 'homework_submissions', ['lesson_id'], unique=False)

    op.create_index(op.f('ix_homework_submissions_school_id'), 'homework_submissions', ['school_id'], unique=False)

    op.create_index(op.f('ix_homework_submissions_student_id'), 'homework_submissions', ['student_id'], unique=False)

    op.create_table('quizzes',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('school_id', sa.Uuid(), nullable=False),

    sa.Column('lesson_id', sa.Uuid(), nullable=False),

    sa.Column('title', sa.String(length=255), nullable=False),

    sa.Column('passing_score', sa.Integer(), nullable=False),

    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),

    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_quizzes_lesson_id'), 'quizzes', ['lesson_id'], unique=False)

    op.create_index(op.f('ix_quizzes_school_id'), 'quizzes', ['school_id'], unique=False)

    op.create_table('quiz_questions',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('quiz_id', sa.Uuid(), nullable=False),

    sa.Column('text', sa.Text(), nullable=False),

    sa.Column('order', sa.Integer(), nullable=False),

    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_quiz_questions_quiz_id'), 'quiz_questions', ['quiz_id'], unique=False)

    op.create_table('quiz_answers',

    sa.Column('id', sa.Uuid(), nullable=False),

    sa.Column('question_id', sa.Uuid(), nullable=False),

    sa.Column('text', sa.Text(), nullable=False),

    sa.Column('is_correct', sa.Boolean(), nullable=False),

    sa.ForeignKeyConstraint(['question_id'], ['quiz_questions.id'], ondelete='CASCADE'),

    sa.PrimaryKeyConstraint('id')

    )

    op.create_index(op.f('ix_quiz_answers_question_id'), 'quiz_answers', ['question_id'], unique=False)

def downgrade() -> None:

    """Downgrade schema."""

    op.drop_index(op.f('ix_quiz_answers_question_id'), table_name='quiz_answers')

    op.drop_table('quiz_answers')

    op.drop_index(op.f('ix_quiz_questions_quiz_id'), table_name='quiz_questions')

    op.drop_table('quiz_questions')

    op.drop_index(op.f('ix_quizzes_school_id'), table_name='quizzes')

    op.drop_index(op.f('ix_quizzes_lesson_id'), table_name='quizzes')

    op.drop_table('quizzes')

    op.drop_index(op.f('ix_homework_submissions_student_id'), table_name='homework_submissions')

    op.drop_index(op.f('ix_homework_submissions_school_id'), table_name='homework_submissions')

    op.drop_index(op.f('ix_homework_submissions_lesson_id'), table_name='homework_submissions')

    op.drop_table('homework_submissions')

    op.drop_index(op.f('ix_subscriptions_user_id'), table_name='subscriptions')

    op.drop_index(op.f('ix_subscriptions_school_id'), table_name='subscriptions')

    op.drop_table('subscriptions')

    op.drop_index(op.f('ix_lessons_school_id'), table_name='lessons')

    op.drop_index(op.f('ix_lessons_module_id'), table_name='lessons')

    op.drop_index(op.f('ix_lessons_course_id'), table_name='lessons')

    op.drop_table('lessons')

    op.drop_index(op.f('ix_payment_plans_school_id'), table_name='payment_plans')

    op.drop_index(op.f('ix_payment_plans_course_id'), table_name='payment_plans')

    op.drop_table('payment_plans')

    op.drop_index(op.f('ix_modules_school_id'), table_name='modules')

    op.drop_index(op.f('ix_modules_course_id'), table_name='modules')

    op.drop_table('modules')

    op.drop_index(op.f('ix_enrollments_user_id'), table_name='enrollments')

    op.drop_index(op.f('ix_enrollments_school_id'), table_name='enrollments')

    op.drop_index(op.f('ix_enrollments_course_id'), table_name='enrollments')

    op.drop_table('enrollments')

    op.drop_table('user_schools')

    op.drop_index(op.f('ix_transactions_user_id'), table_name='transactions')

    op.drop_index(op.f('ix_transactions_school_id'), table_name='transactions')

    op.drop_table('transactions')

    op.drop_table('telegram_bot_settings')

    op.drop_index(op.f('ix_school_subscriptions_school_id'), table_name='school_subscriptions')

    op.drop_table('school_subscriptions')

    op.drop_index(op.f('ix_messages_sender_id'), table_name='messages')

    op.drop_index(op.f('ix_messages_school_id'), table_name='messages')

    op.drop_index(op.f('ix_messages_receiver_id'), table_name='messages')

    op.drop_table('messages')

    op.drop_table('marketing_settings')

    op.drop_table('kommo_settings')

    op.drop_table('crm_leads')

    op.drop_index(op.f('ix_courses_school_id'), table_name='courses')

    op.drop_table('courses')

    op.drop_index(op.f('ix_api_keys_school_id'), table_name='api_keys')

    op.drop_index(op.f('ix_api_keys_key'), table_name='api_keys')

    op.drop_table('api_keys')

    op.drop_index(op.f('ix_schools_subdomain'), table_name='schools')

    op.drop_table('schools')

    op.drop_table('videos')

    op.drop_index(op.f('ix_users_email'), table_name='users')

    op.drop_table('users')

    op.drop_table('payments')


"""empty message

Revision ID: 6133c1a45545
Revises: 6c02a592c536
Create Date: 2024-03-03 18:44:24.252386

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6133c1a45545'
down_revision: Union[str, None] = '6c02a592c536'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('likes_user_login_post_id_key', 'likes', type_='unique')
    op.create_unique_constraint(None, 'likes', ['user_login', 'post_id', 'vote'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'likes', type_='unique')
    op.create_unique_constraint('likes_user_login_post_id_key', 'likes', ['user_login', 'post_id'])
    # ### end Alembic commands ###

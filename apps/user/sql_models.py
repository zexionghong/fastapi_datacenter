import sqlalchemy

from utils.aiopg_conf import metadata

User = sqlalchemy.Table(
    "data2_operator",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("group_id", sqlalchemy.Integer),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("realname", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("salt", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.Integer),
    sqlalchemy.Column("create_time", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("update_time", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("last_login_time", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("level", sqlalchemy.Integer),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("mobile", sqlalchemy.Integer),
    sqlalchemy.Column("company", sqlalchemy.String),
    sqlalchemy.Column("department_id", sqlalchemy.Integer),
    sqlalchemy.Column("is_del", sqlalchemy.Integer),
)

''''''
import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Table, MetaData, String, DateTime, Boolean, ForeignKey, sql, Enum

metadata = MetaData()

class Roles(enum.Enum):
    super = 0
    rwc = 1
    rw = 2
    r = 3

users_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String(40), unique=True, index=True),
    Column("first_name", String(100)),
    Column("last_name", String(100)),
    Column("department", String(100)),
    Column("hashed_password", String()),
    Column("role", Enum(Roles)),
    Column("is_active", Boolean(), server_default=sql.expression.true(), nullable=False),
)


tokens_table = Table(
    "tokens",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("token", String(), unique=True, nullable=False),
    Column("expires", DateTime()),
    Column("user_id", ForeignKey("users.id")),
)
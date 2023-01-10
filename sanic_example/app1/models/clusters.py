import uuid
from datetime import datetime

from sqlalchemy import Column, Table, MetaData, Integer, String
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

clusters_table = Table(
    "clusters",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String(100)),
    Column("countour_type", String(100)),
    Column("url", String()),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

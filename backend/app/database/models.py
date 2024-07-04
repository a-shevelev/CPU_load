from gino import Gino
from app.database.accessor import PostgresAccessor

db = Gino()
postgres_accessor = PostgresAccessor()

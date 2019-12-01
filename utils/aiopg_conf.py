import databases
import sqlalchemy


# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1/dz_data_test"

database = databases.Database(DATABASE_URL,)

metadata = sqlalchemy.MetaData()


engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

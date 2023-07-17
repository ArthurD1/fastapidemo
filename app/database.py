from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.constants import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Create the database URL based on the connection details
db_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Create the SQLAlchemy engine
engine = create_engine(db_url)

# Create a session factory
Sessionlocal = sessionmaker(bind=engine)

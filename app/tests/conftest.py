import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models import Base, StatsMessage
import psycopg2

DB_USERNAME = "dbusername"
DB_PASSWORD = "dbpwd"
DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "test"


messages = [
    StatsMessage(
        customerid=1,
        type="A",
        amount=0.012,
        uuid="a596b362-08be-419f-8070-9c3055566e7c",
        date="2023-07-01",
    ),
    StatsMessage(
        customerid=2,
        type="B",
        amount=0.024,
        uuid="b096b362-08be-419f-8070-9c3055566e7c",
        date="2023-07-02",
    ),
    StatsMessage(
        customerid=3,
        type="A",
        amount=0.036,
        uuid="c596b362-08be-419f-8070-9c3055566e7c",
        date="2023-07-03",
    ),
    StatsMessage(
        customerid=4,
        type="B",
        amount=0.048,
        uuid="d596b362-08be-419f-8070-9c3055566e7c",
        date="2023-07-04",
    ),
]


def is_postgres_running(host, port, user, password, database):
    try:
        # Attempt to establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        conn.close()
        return True  # Connection successful, PostgreSQL is running
    except psycopg2.OperationalError:
        return False  # Connection failed, PostgreSQL is not running or inaccessible


@pytest.fixture(scope="session")
def engine(docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    db_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    docker_services.wait_until_responsive(
        timeout=60.0,
        pause=0.1,
        check=lambda: is_postgres_running(
            DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME
        ),
    )
    return create_engine(db_url)


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    connection = engine.connect()
    # use the connection with the already started transaction
    session = Session(bind=connection)
    # add all the tables to the session
    session.add_all(messages)
    # commit the changes
    session.commit()
    session.close()


@pytest.fixture(scope="module")
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "app/tests/", "docker-compose.yml")

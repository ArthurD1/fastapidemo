from fastapi.testclient import TestClient
from app.main import app, get_db
import pytest

client = TestClient(app)


@pytest.fixture(scope="module")
def override_get_db(dbsession):
    def get_test_db():
        try:
            yield dbsession
        finally:
            dbsession.close()

    app.dependency_overrides[get_db] = get_test_db


def test_get_messages(override_get_db):
    response = client.get("/")
    assert response.status_code == 200
    assert len(response.json()) == 4
    assert response.json()[0] == {
        "customerid": 1,
        "type": "A",
        "amount": "0.012",
        "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
    }


def test_create_message(override_get_db):
    response = client.post(
        "/",
        json={
            "customerid": 5,
            "type": "C",
            "amount": "0.060",
            "uuid": "e596b362-08be-419f-8070-9c3055566e7c",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "customerid": 5,
        "type": "C",
        "amount": "0.060",
        "uuid": "e596b362-08be-419f-8070-9c3055566e7c",
    }


def test_create_message_duplicate(override_get_db):
    response = client.post(
        "/",
        json={
            "customerid": 1,
            "type": "A",
            "amount": "0.012",
            "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Message already exists"}


def test_get_message_by_uuid(override_get_db):
    response = client.get("/messsage/a596b362-08be-419f-8070-9c3055566e7c")
    assert response.status_code == 200
    assert response.json() == {
        "customerid": 1,
        "type": "A",
        "amount": "0.012",
        "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
    }


def test_get_message_by_uuid_not_found(override_get_db):
    response = client.get("/messsage/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}


def test_get_message_from_parameters(override_get_db):
    response = client.get("/messages/?start_date=2023-07-01&end_date=2023-07-02")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0] == {
        "customerid": 1,
        "type": "A",
        "amount": "0.012",
        "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
    }
    assert response.json()[1] == {
        "customerid": 2,
        "type": "B",
        "amount": "0.024",
        "uuid": "b096b362-08be-419f-8070-9c3055566e7c",
    }


def test_get_message_from_parameters_customerid(override_get_db):
    response = client.get("/messages/?customerid=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {
        "customerid": 1,
        "type": "A",
        "amount": "0.012",
        "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
    }


def test_get_message_from_parameters_type(override_get_db):
    response = client.get("/messages/?type=A")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0] == {
        "customerid": 1,
        "type": "A",
        "amount": "0.012",
        "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
    }
    assert response.json()[1] == {
        "customerid": 3,
        "type": "A",
        "amount": "0.036",
        "uuid": "c596b362-08be-419f-8070-9c3055566e7c",
    }


def test_get_message_from_parameters_customerid_type(override_get_db):
    response = client.get("/messages/?customerid=1&type=A")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {
        "customerid": 1,
        "type": "A",
        "amount": "0.012",
        "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
    }


def test_get_message_from_parameters_customerid_type_start_date(override_get_db):
    response = client.get("/messages/?customerid=1&type=A&start_date=2023-07-01")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {
        "customerid": 1,
        "type": "A",
        "amount": "0.012",
        "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
    }


def test_get_message_from_parameters_customerid_type_start_date_end_date(
    override_get_db,
):
    response = client.get(
        "/messages/?customerid=1&type=A&start_date=2023-07-01&end_date=2023-07-01"
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {
        "customerid": 1,
        "type": "A",
        "amount": "0.012",
        "uuid": "a596b362-08be-419f-8070-9c3055566e7c",
    }


def test_read_stats(override_get_db):
    response = client.get("/stats/?customerid=1&type=A&start_date=2023-07-01&end_date=2023-07-01")
    assert response.status_code == 200
    assert response.json()["total_amount"] == "0.012"
    assert response.json()["messages_count"] == 1

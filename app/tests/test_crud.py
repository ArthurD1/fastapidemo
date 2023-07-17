from app.models import StatsMessage as MessageModel
from app.schemas import Message
import uuid
from app.crud import (
    get_messages,
    create_message,
    get_message_by_uuid,
    get_message_from_parameters,
)
from datetime import datetime

message_data = {
    "customerid": 1,
    "type": "A",
    "amount": 0.012,
    "uuid": "e596b362-08be-419f-8070-9c3055566e7c",
    "date": "2023-07-04",
}


def test_get_messages(dbsession):
    """Test get messages"""
    # Call the get_messages function
    messages = get_messages(dbsession)

    # Assertions
    assert len(messages) == 4
    assert all(isinstance(msg, MessageModel) for msg in messages)


def test_create_message(dbsession):
    """Test create message"""
    # Call the create_message function
    message = create_message(dbsession, Message.model_validate(message_data))

    # Assertions
    assert isinstance(message, MessageModel)
    assert Message.model_validate(message) == Message.model_validate(message_data)


def test_get_message_by_uuid(dbsession):
    """Test get message by UUID"""
    # Prepare test data
    id = uuid.UUID("a596b362-08be-419f-8070-9c3055566e7c")

    # Call the get_message_by_uuid function
    message = get_message_by_uuid(dbsession, id)

    # Assertions
    assert isinstance(message, MessageModel)
    assert message.uuid == id


def test_get_message_from_parameters(dbsession):
    """Test get message from parameters"""
    # Prepare test data
    start_date = "2023-07-01"
    end_date = "2023-07-02"
    customerid = 1
    type = "A"

    # Call the get_message_from_parameters function
    messages = get_message_from_parameters(
        dbsession, start_date, end_date, customerid, type
    )

    # Assertions
    assert len(messages) == 1
    assert all(isinstance(msg, MessageModel) for msg in messages)
    assert messages[0].customerid == customerid
    assert messages[0].type == type
    assert messages[0].date >= datetime.strptime(start_date, "%Y-%m-%d").date()
    assert messages[0].date <= datetime.strptime(end_date, "%Y-%m-%d").date()

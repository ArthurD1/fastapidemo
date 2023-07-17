from sqlalchemy.orm import Session
from pydantic import UUID4
from app.models import StatsMessage as MessageModel
from app.schemas import Message
from datetime import datetime


def get_messages(db: Session) -> list[MessageModel]:
    """
    Retrieve all messages from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        List[MessageModel]: List of messages retrieved from the database.
    """
    return db.query(MessageModel).all()


def create_message(db: Session, message: Message) -> MessageModel:
    """
    Create a new message in the database.

    Args:
        db (Session): SQLAlchemy database session.
        message (Message): Message object representing the message data.

    Returns:
        MessageModel: Created message object.
    """
    db_message = MessageModel(
        **message.model_dump(), date=datetime.date(datetime.now())
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_message_by_uuid(db: Session, uuid: UUID4) -> MessageModel:
    """
    Retrieve a message from the database by UUID.

    Args:
        db (Session): SQLAlchemy database session.
        uuid (UUID4): UUID of the message.

    Returns:
        MessageModel: Retrieved message object or None if not found.
    """
    return db.query(MessageModel).filter(MessageModel.uuid == uuid).first()


def get_message_from_parameters(
    db: Session,
    start_date: str | None = None,
    end_date: str | None = None,
    customerid: int | None = None,
    type: str | None = None,
) -> list[MessageModel]:
    """
    Retrieve messages from the database based on various parameters.

    Args:
        db (Session): SQLAlchemy database session.
        start_date (str | None): Start date of the date range (optional).
        end_date (str | None): End date of the date range (optional).
        customerid (int | None): Customer ID (optional).
        type (str | None): Type of the message (optional).

    Returns:
        List[MessageModel]: List of messages matching the parameters.
    """
    query = db.query(MessageModel)
    if start_date and end_date:
        query = query.filter(MessageModel.date.between(start_date, end_date))
    elif start_date:
        query = query.filter(MessageModel.date >= start_date)
    elif end_date:
        query = query.filter(MessageModel.date <= end_date)
    if customerid:
        query = query.filter(MessageModel.customerid == customerid)
    if type:
        query = query.filter(MessageModel.type == type)
    return query.all()

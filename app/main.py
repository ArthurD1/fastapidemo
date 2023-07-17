from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import Sessionlocal
from pydantic import UUID4
from app import schemas
from app.crud import (
    get_messages,
    get_message_by_uuid,
    create_message,
    get_message_from_parameters,
)
from typing import List, Annotated

app = FastAPI(
    title="Jagaad Stats API",
    description="This is the API for the Jagaad application",
    version="0.1.0",
)


# Dependency
def get_db():
    """
    Dependency function to get the database session.
    """
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=list[schemas.Message])
def read_messages(db: Session = Depends(get_db)):
    """
    API endpoint to read all messages.
    """
    messages = get_messages(db)
    return messages


@app.post("/", response_model=schemas.Message)
def post_message(message: schemas.Message, db: Session = Depends(get_db)):
    """
    API endpoint to create a new message.
    """
    db_message = get_message_by_uuid(db, uuid=message.uuid)
    if db_message:
        raise HTTPException(status_code=400, detail="Message already exists")
    return create_message(db=db, message=message)


@app.get("/messsage/{uuid}", response_model=schemas.Message)
def read_message_from_uuid(uuid: UUID4, db: Session = Depends(get_db)):
    """
    API endpoint to read a message by UUID.
    """
    db_message = get_message_by_uuid(db, uuid=uuid)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message


@app.get("/messages/", response_model=List[schemas.Message])
def read_messages_from_parameters(
    start_date: Annotated[
        str | None,
        Query(
            title="Start Date",
            min_length=6,
            max_length=10,
            description="The start date of the date range, it must be of the form YYYY-MM-DD or YYYYMMDD",
            pattern="^\\d{4}\\W?\\d{2}\\W?\\d{2}$",
        ),
    ] = None,
    end_date: Annotated[
        str | None,
        Query(
            title="End Date",
            min_length=6,
            max_length=10,
            description="The end date of the date range, it must be of the form YYYY-MM-DD or YYYYMMDD",
            pattern="^\\d{4}\\W?\\d{2}\\W?\\d{2}$",
        ),
    ] = None,
    db: Session = Depends(get_db),
    customerid: int = Query(None, title="Customer ID", description="The customer ID"),
    type: str = Query(None, title="Type", description="The type of message"),
):
    """
    API endpoint to read messages based on various parameters.
    """
    messages = get_message_from_parameters(
        db, start_date=start_date, end_date=end_date, customerid=customerid, type=type
    )
    return messages


@app.get("/stats/", response_model=schemas.Stats)
def read_stats(
    start_date: Annotated[
        str | None,
        Query(
            title="Start Date",
            min_length=6,
            max_length=10,
            description="The start date of the date range, it must be of the form YYYY-MM-DD or YYYYMMDD",
            pattern="^\\d{4}\\W?\\d{2}\\W?\\d{2}$",
        ),
    ] = None,
    end_date: Annotated[
        str | None,
        Query(
            title="End Date",
            min_length=6,
            max_length=10,
            description="The end date of the date range, it must be of the form YYYY-MM-DD or YYYYMMDD",
            pattern="^\\d{4}\\W?\\d{2}\\W?\\d{2}$",
        ),
    ] = None,
    customerid: int = Query(None, title="Customer ID", description="The customer ID"),
    type: str = Query(None, title="Type", description="The type of message"),
    db: Session = Depends(get_db),
):
    """
    API endpoint to retrieve statistics based on various parameters.
    """
    messages = get_message_from_parameters(
        db, start_date=start_date, end_date=end_date, customerid=customerid, type=type
    )
    return {
        "messages": [schemas.Message.model_validate(message) for message in messages],
        "messages_count": len(messages),
        "total_amount": sum([message.amount for message in messages]),
    }

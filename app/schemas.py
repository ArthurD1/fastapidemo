from pydantic import BaseModel, Field, UUID4, field_validator, ConfigDict
from decimal import Decimal


class Message(BaseModel):
    """Messages than can be received by the API"""

    model_config = ConfigDict(from_attributes=True)

    customerid: int = Field(description="The customer unique identifier")
    type: str = Field(description="The type of message received")
    amount: str = Field(description="The amount of the message")
    uuid: UUID4 = Field(description="The message unique identifier")

    @field_validator("amount", mode="before")
    def set_amount(cls, value):
        # Set the amount to a string if it is a float or a Decimal
        return str(value) if isinstance(value, float | Decimal) else value

    @field_validator("amount")
    def validate_amount_precision(cls, value):
        # Check if the value has 3 decimal precision
        parts = str(value).split(".")
        if len(parts) > 1 and len(parts[1]) != 3:
            raise ValueError("Amount must have 3 decimal precision")
        return value


class Stats(BaseModel):
    """Stats about the messages"""
    model_config = ConfigDict(from_attributes=True)


    messages: list[Message] = Field(description="The list of messages")
    messages_count: int = Field(description="The number of messages")
    total_amount: Decimal = Field(description="The total amount of messages")

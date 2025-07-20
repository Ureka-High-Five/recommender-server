from pydantic import BaseModel

class UserActionRequestDto(BaseModel):
    user_id: int
    action_type: str
    value: float
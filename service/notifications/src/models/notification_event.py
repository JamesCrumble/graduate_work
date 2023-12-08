from typing import Any

from pydantic import BaseModel


class NotificationEvent(BaseModel):
    is_broadcast: bool
    template_id: int
    user_ids: list[str] | None
    context: dict[str, Any]

    class Config:
        use_enum_values = True

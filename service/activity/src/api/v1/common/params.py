import json
from typing import Annotated

from fastapi import Query


class CommonParams:
    def __init__(
        self,
        page_number: Annotated[int, Query(gt=0, description='page number')] = 1,
        page_size: Annotated[int, Query(le=50, ge=10, description='number of objects on page')] = 10,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

    def build_pagination(self) -> tuple[int, int]:
        from_ = (self.page_number - 1) * self.page_size
        return from_, self.page_size

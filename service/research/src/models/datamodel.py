import uuid
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field

sample_path = Path(__file__).parents[1].joinpath('samplereview.txt')
sample_text = Path(sample_path).read_text()


class AuthorFilmMixin(BaseModel):
    author: uuid.UUID = Field(default=uuid.uuid4())
    film: uuid.UUID = Field(default=uuid.uuid4())


class DataModelLike(AuthorFilmMixin):
    like_value: int = Field(default=5, gt=-1, lt=11)

    def model_dump(self):
        return {
            'like_value': self.like_value,
            'author': str(self.author),
            'film': str(self.film),
        }


class DataModelReview(AuthorFilmMixin):
    text: str = Field(default=sample_text)
    published: datetime = Field(default=datetime.now())

    def model_dump(self):
        return {
            'text': self.text,
            'published': str(self.published),
            'author': str(self.author),
            'film': str(self.film),
        }


class DataModelBookmark(AuthorFilmMixin):

    def model_dump(self):
        return {
            'author': str(self.author),
            'film': str(self.film),
        }

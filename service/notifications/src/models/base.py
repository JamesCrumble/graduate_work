from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    __table_args__ = ({'schema': 'content'},)

from pydantic import BaseModel


class ESBaseModel(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    def to_es(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', False)
        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )
        # Mongo uses `_id` as default key.
        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')
        return parsed

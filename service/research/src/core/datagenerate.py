from schemas.dataschema import dataclass_list


def model_generator():
    for _ in range(1000):
        for itemclass in dataclass_list:
            item = itemclass()
            yield [
                itemclass,
                item.model_dump(),
            ]

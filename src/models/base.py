from dataclasses import asdict


class BaseModel:

    def to_dict(self):
        return asdict(self)

    def to_tuple(self):
        return tuple(asdict(self).values())
import json
from inspect import get_annotations
from typing import Any

from src.field import Field
from src.model_metaclass import ModelMetaclass


class BaseModel(metaclass=ModelMetaclass):
    @classmethod
    def _fields(cls) -> dict[str, type]:
        return get_annotations(cls)

    def __init_subclass__(subcls) -> None:
        super().__init_subclass__()
        for name, type in subcls._fields().items():
            setattr(subcls, name, Field(name, type))

    def __init__(self, **kwargs) -> None:
        for validator in self._root_validators:
            kwargs = validator.__func__(self.__class__, kwargs)
        # By iterating over self._fields instead of kwargs, we ignore any extra non-declared fields
        for name in self._fields():
            value = kwargs.pop(name, None)
            if validators := self._validators.get(name):
                for validator in validators:
                    value = validator.__func__(self.__class__, value)
            setattr(self, name, value)

    def dict(self) -> dict[str, Any]:
        return {
            name: getattr(self, name)
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, Field)
        }

    def json(self) -> str:
        return json.dumps(self.dict())

    def __repr__(self) -> str:
        kwargs = ", ".join(f"{key}={value!r}" for key, value in self.dict().items())
        class_name = self.__class__.__name__
        return f"{class_name}({kwargs})"

    def __str__(self) -> str:
        return " ".join(f"{key}={value!r}" for key, value in self.dict().items())

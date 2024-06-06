from typing import Any


class Field:
    def __init__(self, name: str, field_type: type) -> None:
        self.name = name
        self.field_type = field_type

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, self.field_type):
            type_name = self.field_type.__name__
            msg = f"{self.name}: Input should be a valid {type_name}"
            raise TypeError(msg)

        instance.__dict__[self.name] = value

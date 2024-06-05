from typing import Callable


def validator(*field_names) -> Callable:
    def decorator(func):
        func.field_names = field_names
        func.is_validator = True
        return func

    return decorator


def root_validator() -> Callable:
    def decorator(func):
        func.is_root_validator = True
        return func

    return decorator

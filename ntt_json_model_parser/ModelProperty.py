from typing import (
    Any,
)
from .constants import MODEL_FLAG


def Property(func):
    def getter(instance):
        obj = getattr(instance, f"_{func.__name__}")
        setattr(obj, MODEL_FLAG, False)
        return obj

    def setter(instance, value):
        setattr(instance, f"_{func.__name__}", value)

def ModelProperty(func):
    def getter(instance):
        obj = getattr(instance, f"_{func.__name__}")
        setattr(obj, MODEL_FLAG, True)
        return obj

    def setter(instance, value):
        setattr(instance, f"_{func.__name__}", value)

    return property(getter, setter)
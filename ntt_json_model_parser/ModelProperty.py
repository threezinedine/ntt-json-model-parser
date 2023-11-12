from typing import (
    Any,
    List,
)
from .constants import *


def Model(claClass):
    def wrapper(*args, **kwargs):
        obj = claClass(*args, **kwargs)

        setattr(obj, PROPERTIES_LIST, [])
        setattr(obj, MODEL_PROPERTIES_DICT, {})
        setattr(obj, MODEL_LIST_PROPERTIES_DICT, {})

        strAttributeNames: List[str] = list(filter(lambda x: not x.startswith("_"), dir(obj)))

        for strAttributeName in strAttributeNames:
            getattr(obj, strAttributeName)

        return obj
        
    return wrapper


def Property(func):
    def getter(instance):
        obj = getattr(instance, f"_{func.__name__}")
        strProperties: list = getattr(instance, PROPERTIES_LIST)
        if func.__name__ not in strProperties:
            strProperties.append(func.__name__)
            setattr(instance, PROPERTIES_LIST, strProperties)
        return obj

    def setter(instance, value):
        setattr(instance, f"_{func.__name__}", value)

    return property(getter, setter)

def ModelProperty(claClassName):
    def wrapper(func):
        def getter(instance):
            obj = getattr(instance, f"_{func.__name__}")
            dictProperties: list = getattr(instance, MODEL_PROPERTIES_DICT)
            if func.__name__ not in dictProperties:
                dictProperties[func.__name__] = claClassName
                setattr(instance, MODEL_PROPERTIES_DICT, dictProperties)
            return obj

        def setter(instance, value):
            setattr(instance, f"_{func.__name__}", value)

        return property(getter, setter)
    return wrapper

def ModelListProperty(claPropertyType):
    def wrapper(func):
        def getter(instance):
            obj = getattr(instance, f"_{func.__name__}")
            dictProperties: dict = getattr(instance, MODEL_LIST_PROPERTIES_DICT)
            if func.__name__ not in dictProperties:
                dictProperties[func.__name__] = claPropertyType
                setattr(instance, MODEL_LIST_PROPERTIES_DICT, dictProperties)
            return obj

        def setter(instance, value):
            setattr(instance, f"_{func.__name__}", value)

        return property(getter, setter)

    return wrapper
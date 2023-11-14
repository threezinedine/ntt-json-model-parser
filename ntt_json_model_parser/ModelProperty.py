from typing import (
    Any,
    List,
    Callable,
)
import types
from .constants import *
from .Signal import Signal
from .ObservableList import ObservableList

def Bind(self: object, strAttributeName: str, cbCallback: Callable) -> None:
    getattr(self, f"_{strAttributeName}_signal").AddCallback(cbCallback, bCalled=False)


def Model(claClass):
    def wrapper(*args, **kwargs):
        obj = claClass(*args, **kwargs)

        setattr(obj, PROPERTIES_LIST, [])
        setattr(obj, MODEL_PROPERTIES_DICT, {})
        setattr(obj, MODEL_LIST_PROPERTIES_DICT, {})

        strAttributeNames: List[str] = list(filter(lambda x: not x.startswith("_"), dir(obj)))

        setattr(obj, f"_signal", Signal(f"{claClass.__name__}"))

        for strAttributeName in strAttributeNames:
            getattr(obj, strAttributeName)

        obj.Bind = types.MethodType(Bind, obj) 

        return obj
        
    return wrapper


def Property(func):
    def getter(instance):
        obj = getattr(instance, f"_{func.__name__}")
        strProperties: list = getattr(instance, PROPERTIES_LIST)
        if func.__name__ not in strProperties:
            setattr(instance, f"_{func.__name__}_signal", Signal(f"{func.__name__}"))
            strProperties.append(func.__name__)
            setattr(instance, PROPERTIES_LIST, strProperties)
            if isinstance(obj, ObservableList):
                obj.AttachSignal(getattr(instance, f"_{func.__name__}_signal"))

            getattr(instance, f"_{func.__name__}_signal").AttachSignal(
                getattr(instance, f"_signal")
            )
        return obj

    def setter(instance, value):
        setattr(instance, f"_{func.__name__}", value)
        getattr(instance, f"_{func.__name__}_signal").Emit()

    return property(getter, setter)

def ModelProperty(claClassName, popup=False):
    def wrapper(func):
        def getter(instance):
            obj = getattr(instance, f"_{func.__name__}")

            dictProperties: list = getattr(instance, MODEL_PROPERTIES_DICT)
            if func.__name__ not in dictProperties:
                dictProperties[func.__name__] = claClassName
                setattr(instance, MODEL_PROPERTIES_DICT, dictProperties)

                if popup:
                    setattr(instance, 
                            f"_{func.__name__}_signal", 
                            getattr(obj, f"_signal")
                    )
                else:
                    setattr(instance,
                            f"_{func.__name__}_signal", 
                            Signal(func.__name__))

            return obj

        def setter(instance, value):
            setattr(instance, f"_{func.__name__}", value)

        return property(getter, setter)
    return wrapper

def ModelListProperty(claPropertyType, popup=False):
    def wrapper(func):
        def getter(instance):
            obj = getattr(instance, f"_{func.__name__}")
            dictProperties: dict = getattr(instance, MODEL_LIST_PROPERTIES_DICT)
            if func.__name__ not in dictProperties:
                dictProperties[func.__name__] = claPropertyType
                setattr(instance, MODEL_LIST_PROPERTIES_DICT, dictProperties)
                setattr(instance, f"_{func.__name__}_signal", obj._signal)

                if popup:
                    getattr(instance, f"_{func.__name__}_signal").AttachSignal(getattr(instance, f"_signal"))
            return obj

        return property(getter)

    return wrapper
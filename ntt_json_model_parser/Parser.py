from typing import (
    Any,
    Callable,
    List,
    Dict,
)
import json
from .constants import *
from .ObservableList import ObservableList
from .ModelProperty import ModelRepo


class Parser:
    @staticmethod
    def DeSerializeFromDict(obj: object, dictObjectData: dict) -> Any:
        if dictObjectData is not None:
            for key, value in dictObjectData.items():
                if value is None:
                    continue
                elif not hasattr(obj, key):
                    continue
                else:
                    Parser._LoadAttributeByKeyAndValue(obj, key, value)

            return obj
        else:
            return None

    @staticmethod
    def _LoadAttributeByKeyAndValue(obj: object, key: str, value: Any) -> None:
        if key in getattr(obj, PROPERTIES_LIST):
            if isinstance(value, list):
                lst = getattr(obj, key)
                lst._ClearWithoutNotifying()
                for element in value:
                    lst.append(element)
            else:
                setattr(obj, key, value)
        elif key in getattr(obj, MODEL_PROPERTIES_LIST):
            Parser.DeSerializeFromDict(getattr(obj, key), value)
        elif key in getattr(obj, MODEL_LIST_PROPERTIES_DICT):
            lstClasses = getattr(obj, MODEL_LIST_PROPERTIES_DICT)[key]
            lValues = getattr(obj, key)
            lValues._ClearWithoutNotifying()

            for oElement in value:
                strClassName = oElement["__class__"]
                claObj = ModelRepo.claTypes[strClassName]()
                if claObj is not None:
                    Parser.DeSerializeFromDict(claObj, oElement)
                    lValues.append(claObj)

    @staticmethod
    def _GetClass(strClassName: str, lstClasses: List[callable]) -> callable:
        for classObj in lstClasses:
            if strClassName == classObj.__class__.__name__:
                return classObj

    @staticmethod
    def DeSerializeFromFile(claClassName: Callable, strFileName: str) -> Any:
        with open(strFileName, "r") as file:
            dictData = json.load(file)

        return Parser.DeSerializeFromDict(claClassName, dictData)

    @staticmethod
    def SerializeToDict(obj: Any) -> dict:
        dictObjectData = {}
        
        Parser._SerialzeNormalProperties(obj, dictObjectData)
        Parser._SerialModelProperties(obj, dictObjectData)
        Parser._SerialModelListProperties(obj, dictObjectData)

        return dictObjectData

    @staticmethod
    def _SerialzeNormalProperties(obj: object, dictObjectData: dict) -> None:
        strNormalProperties: List[str] = getattr(obj, PROPERTIES_LIST)

        for strProperty in strNormalProperties:
            dictObjectData[strProperty] = getattr(obj, strProperty)
            dictObjectData["__class__"] = obj.__class__.__name__

    @staticmethod
    def _SerialModelProperties(obj: object, dictObjectData: dict) -> None:
        strModelProperties: List[str] = getattr(obj, MODEL_PROPERTIES_LIST)

        for strProperty in strModelProperties:
            dictObjectData[strProperty] = Parser.SerializeToDict(getattr(obj, strProperty))

    @staticmethod
    def _SerialModelListProperties(obj: object, dictObjectData: dict) -> None:
        strModelProperties: List[str] = getattr(obj, MODEL_LIST_PROPERTIES_DICT).keys()

        for strProperty in strModelProperties:
            mModels: List[object] = getattr(obj, strProperty)

            dictObjectData[strProperty] = [
                Parser.SerializeToDict(mModel)
                for mModel in mModels
            ]

    @staticmethod
    def SerializeToFile(obj: Any, strTargetFile: str) -> None:
        dictObjectData = Parser.SerializeToDict(obj) 

        with open(strTargetFile, "w") as file:
            json.dump(dictObjectData, file, indent=4)
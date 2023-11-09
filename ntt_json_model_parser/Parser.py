from typing import (
    Any,
    Callable,
)
import json
from .constants import MODEL_FLAG


class Parser:
    @staticmethod
    def DeSerializeFromDict(claClassName: Callable, dictObjectData: dict) -> Any:
        obj = claClassName()

        if dictObjectData is not None:
            for key, value in dictObjectData.items():
                attr = getattr(obj, key)

                if value is None:
                    continue
                if not hasattr(attr, MODEL_FLAG):
                    setattr(obj, key, value)
                else:
                    setattr(obj, key, Parser.DeSerializeFromDict(attr.__class__, value))

            return obj
        else:
            return None

    @staticmethod
    def DeSerializeFromFile(claClassName: Callable, strFileName: str) -> Any:
        with open(strFileName, "r") as file:
            dictData = json.load(file)

        return Parser.DeSerializeFromDict(claClassName, dictData)

    @staticmethod
    def SerializeToDict(obj: Any) -> dict:
        strAttributeNames = list(filter(lambda strVal: not strVal.startswith("_"), dir(obj)))
        dictObjectData = {}

        for strAttributeName in strAttributeNames:
            attr = getattr(obj, strAttributeName)

            if not hasattr(attr, MODEL_FLAG):
                dictObjectData[strAttributeName] = attr
            else:
                dictObjectData[strAttributeName] = Parser.SerializeToDict(attr)

        return dictObjectData

    @staticmethod
    def SerializeToFile(obj: Any, strTargetFile: str) -> None:
        dictObjectData = Parser.SerializeToDict(obj) 

        with (strTargetFile, "w") as file:
            json.dump(dictObjectData, file, indent=4)
import unittest
from ntt_json_model_parser import Parser, ModelProperty, Property, Model


@Model
class Lecture:
    def __init__(self) -> None:
        self._strName = ""
        self._nAttempts = 0

    @Property
    def strName(self) -> str:
        return self._strName

    @Property
    def nAttempts(self) -> int:
        return self._nAttempts

@Model
class Person:
    def __init__(self) -> None:
        self._strName = ""
        self._nAge = 0

        self._lecLecture : Lecture = Lecture()

    @Property
    def strName(self) -> str:
        return self._strName

    @Property
    def nAge(self) -> int:
        return self._nAge

    @ModelProperty(Lecture)
    def lecLecture(self) -> Lecture:
        return self._lecLecture
    

class ParserTesting(unittest.TestCase):
    def test_ConvertFromDictToObject(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "nAge": 23,
        }

        perFirstStudent: Person = Parser.DeSerializeFromDict(Person, dictObjectData)

        self.assertEqual(
            perFirstStudent.strName,
            "Thao Nguyen The"
        )

        self.assertEqual(
            perFirstStudent.nAge,
            23,
        )

    def test_ConvertFromDictWithNestingObject(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "nAge": 23,
            "lecLecture": {
                "strName": "Math",
                "nAttempts": 3,
            }
        }

        perFirstStudent: Person = Parser.DeSerializeFromDict(Person, dictObjectData)

        self.assertEqual(
            perFirstStudent.lecLecture.strName,
            "Math",
        )

        self.assertEqual(
            perFirstStudent.lecLecture.nAttempts,
            3,
        )

    def test_ConvertFromDictWithNoneAttribute(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "nAge": 23,
            "lecLecture": None
        }

        perFirstStudent: Person = Parser.DeSerializeFromDict(Person, dictObjectData)

        self.assertEqual(
            perFirstStudent.lecLecture.strName,
            ""
        )
        self.assertEqual(
            perFirstStudent.lecLecture.nAttempts,
            0,
        )

    def test_ConvertFromObjectToDict(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "nAge": 23,
        }

        perFirstStudent: Person = Parser.DeSerializeFromDict(Person, dictObjectData)

        dictSerializedData = Parser.SerializeToDict(perFirstStudent)

        self.assertDictEqual(
            dictSerializedData,
            {
                "strName": "Thao Nguyen The",
                "nAge": 23,
                "lecLecture": {
                    "strName": "",
                    "nAttempts": 0
                }
            }
        )
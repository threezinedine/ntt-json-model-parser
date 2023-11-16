import unittest
from unittest.mock import Mock
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
class Score:
    def __init__(self) -> None:
        self._nScore = 8

    @Property
    def nScore(self) -> int:
        return self._nScore

@Model
class Person:
    def __init__(self) -> None:
        self._strName = ""
        self._nAge = 0

        self._lecLecture : Lecture = Lecture()
        self._scoScore: Score() = Score()

    @Property
    def strName(self) -> str:
        return self._strName

    @Property
    def nAge(self) -> int:
        return self._nAge

    @ModelProperty()
    def lecLecture(self) -> Lecture:
        return self._lecLecture

    @ModelProperty(popup=True)
    def scoScore(self) -> Score:
        return self._scoScore


class ParserTesting(unittest.TestCase):
    def test_ConvertFromDictToObject(self):
        dictObjectData = {
            "__class__": "Person",
            "strName": "Thao Nguyen The",
            "nAge": 23,
        }

        perFirstStudent = Person() 
        Parser.DeSerializeFromDict(perFirstStudent, dictObjectData)

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
            "__class__": "Person",
            "strName": "Thao Nguyen The",
            "nAge": 23,
            "lecLecture": {
                "__class__": "Lecture",
                "strName": "Math",
                "nAttempts": 3,
            }
        }

        perFirstStudent = Person() 
        Parser.DeSerializeFromDict(perFirstStudent, dictObjectData)

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

        perFirstStudent = Person() 
        Parser.DeSerializeFromDict(perFirstStudent, dictObjectData)

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
            "__class__": "Person",
            "strName": "Thao Nguyen The",
            "nAge": 23,
        }

        perFirstStudent = Person() 
        Parser.DeSerializeFromDict(perFirstStudent, dictObjectData)

        dictSerializedData = Parser.SerializeToDict(perFirstStudent)

        self.assertDictEqual(
            dictSerializedData,
            {
                "__class__": "Person",
                "strName": "Thao Nguyen The",
                "nAge": 23,
                "lecLecture": {
                    "__class__": "Lecture",
                    "strName": "",
                    "nAttempts": 0
                },
                "scoScore": {
                    "__class__": "Score",
                    "nScore": 8,
                },
            }
        )

    def test_AddTheCallbackForCheckingChangeInTheNameAttribute(self):
        dictObjectData = {
            "__class__": "Person",
            "strName": "Thao Nguyen The",
            "nAge": 23,
        }
        perFirstStudent = Person() 
        Parser.DeSerializeFromDict(perFirstStudent, dictObjectData)
        testCallback = Mock()
        perFirstStudent.Bind("strName", testCallback)

        perFirstStudent.strName = "Testing"

        testCallback.assert_called_once()

    def test_ObjectPropertyChangedThenTheClassObjectIsNotified(self):
        dictObjectData = {
            "__class__": "Score",
            "nScore": 7,
        }
        scoScore = Score() 
        Parser.DeSerializeFromDict(scoScore, dictObjectData)
        testCallback = Mock()
        getattr(scoScore, f"_signal").AddCallback(testCallback, bCalled=False)

        scoScore.nScore = 3

        testCallback.assert_called_once()


    def test_TheCallbackIsPopup(self):
        dictObjectData = {
            "__class__": "Score",
            "strName": "Thao Nguyen The",
            "nAge": 23,
            "scoScore": {
                "nScore": 9,
            },
        }
        perFirstStudent = Person() 
        Parser.DeSerializeFromDict(perFirstStudent, dictObjectData)
        testCallback = Mock()

        perFirstStudent.Bind("scoScore", testCallback)

        perFirstStudent.scoScore.nScore = 10

        testCallback.assert_called_once()
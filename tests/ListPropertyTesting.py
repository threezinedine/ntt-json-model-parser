from typing import (
    List,
)
import unittest
from unittest.mock import Mock
from ntt_json_model_parser import (
    ModelListProperty,
    Property,
    Parser,
    Model,
    ObservableList,
)


@Model
class Skill:
    def __init__(self, strName: str = "") -> None:
        self._strName = strName

    @Property
    def strName(self) -> str:
        return self._strName

@Model
class User:
    def __init__(self, strName: str = "") -> None:
        self._strName = strName
        self._skiSkills = ObservableList()
        self._strNickNames = ObservableList()
        self._strExNames = ObservableList()
        self._skiObservableSkills = ObservableList()

    @Property
    def strName(self) -> str:
        return self._strName

    @Property
    def strNickNames(self) -> ObservableList:
        return self._strNickNames

    @Property
    def strExNames(self) -> ObservableList:
        return self._strExNames

    @ModelListProperty(Skill)
    def skiSkills(self) -> ObservableList:
        return self._skiSkills

    @ModelListProperty(Skill, popup=True)
    def skiObservableSkills(self) -> ObservableList:
        return self._skiObservableSkills


class ListPropertyTesting(unittest.TestCase):
    def test_ExtractListProperty(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "skiSkills": [
                {
                    "strName": "Programming"
                },
                {
                    "strName": "Singing"
                }
            ]
        }

        uUser = User() 
        Parser.DeSerializeFromDict(uUser, dictObjectData)

        self.assertEqual(
            uUser.strName, 
            "Thao Nguyen The"
        )

        skiSkills: List[Skill] = uUser.skiSkills

        self.assertIsNotNone(skiSkills)
        self.assertEqual(skiSkills[0].strName, "Programming")
        self.assertEqual(skiSkills[1].strName, "Singing")

    def test_SerializeListProperty(self):
        uUser: User = User("Nguyen The Thao")

        uUser.skiSkills.append(
            Skill("Math")
        ) 
        uUser.skiSkills.append(
            Skill("Programming")
        )

        uUser.strNickNames = ObservableList([
            "biu", "threezinedine"
        ])

        dictObjectData: dict = Parser.SerializeToDict(uUser)

        self.assertDictEqual(
            dictObjectData,
            {
                "strName": "Nguyen The Thao",
                "strNickNames": ["biu", "threezinedine"],
                "skiSkills": [
                    {
                        "strName": "Math",
                    },
                    {
                        "strName": "Programming",
                    }
                ],
                "strExNames": [],
                "skiObservableSkills": []
            }
        )

    def test_ListIsObservable(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "strNickNames": ["biu", "threezinedine"],
            "skiSkills": [
                {
                    "strName": "Programming"
                },
                {
                    "strName": "Singing"
                }
            ]
        }
        testCallback = Mock()
        uUser = User() 
        Parser.DeSerializeFromDict(uUser, dictObjectData)

        uUser.skiSkills.Bind(testCallback)

        uUser.skiSkills[0].strName = "Testing"
        uUser.skiSkills.append(Skill("Game"))

        self.assertEqual(testCallback.call_count, 2)

    def test_ListNonModelPropertyIsObservable(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "strNickNames": ["biu", "threezinedine"],
            "skiSkills": [
                {
                    "strName": "Programming"
                },
                {
                    "strName": "Singing"
                }
            ]
        }
        testCallback = Mock()
        uUser = User() 
        Parser.DeSerializeFromDict(uUser, dictObjectData)

        uUser.strNickNames.Bind(testCallback)

        uUser.strNickNames.append("Hello")
        uUser.strNickNames.insert(1, "Testing")
        uUser.strNickNames.remove("Testing")
        uUser.strNickNames.pop()

        self.assertEqual(testCallback.call_count, 4)

    def test_ModelObservableListDoesNotEmitTheParentObjectAsDefault(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "skiSkills": [
                {
                    "strName": "Programming"
                },
                {
                    "strName": "Singing"
                }
            ]
        }
        testCallback = Mock()
        uUser = User() 
        Parser.DeSerializeFromDict(uUser, dictObjectData)

        uUser.Bind("strNickNames", testCallback)

        uUser.skiSkills.append(
            Skill("Hello World")
        )

        testCallback.assert_not_called()

    def test_ModelObservableListEmitsTheParentObject(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "skiSkills": [
                {
                    "strName": "Programming"
                },
                {
                    "strName": "Singing"
                },
            ],
            "skiObservableSkills": [
                {
                    "strName": "Testing"
                }
            ]
        }
        testCallback = Mock()
        uUser = User() 
        Parser.DeSerializeFromDict(uUser, dictObjectData)

        uUser.Bind("skiObservableSkills", testCallback)

        uUser.skiObservableSkills.append(
            Skill("Hello World")
        )
        uUser.skiObservableSkills[-2].strName = "New Name (1)"
        uUser.skiObservableSkills[-1].strName = "New Name (2)"

        uUser.skiObservableSkills.insert(1, Skill("Fucking Test"))
        uUser.skiObservableSkills[1].strName = "I'm sorry"

        self.assertEqual(testCallback.call_count, 5)

    def test_NonModelObservableListEmitsTheParentObject(self):
        dictObjectData = {
            "strName": "Thao Nguyen The",
            "skiSkills": [
                {
                    "strName": "Programming"
                },
                {
                    "strName": "Singing"
                }
            ]
        }
        testCallback = Mock()
        uUser = User() 
        Parser.DeSerializeFromDict(uUser, dictObjectData)

        uUser.Bind("strExNames", testCallback)

        uUser.strExNames.append("Hello World")

        testCallback.assert_called_once()

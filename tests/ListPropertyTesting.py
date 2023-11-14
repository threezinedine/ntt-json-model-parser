from typing import (
    List,
)
import unittest
from ntt_json_model_parser import (
    ModelListProperty,
    Property,
    Parser,
    Model,
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
        self._skiSkills: List[Skill] = []

    @Property
    def strName(self) -> str:
        return self._strName

    @ModelListProperty(Skill)
    def skiSkills(self) -> List[Skill]:
        return self._skiSkills


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
        print(skiSkills)

        self.assertIsNotNone(skiSkills)
        self.assertEqual(skiSkills[0].strName, "Programming")
        self.assertEqual(skiSkills[1].strName, "Singing")

    def test_SerializeListProperty(self):
        uUser: User = User("Nguyen The Thao")

        uUser.skiSkills = [
            Skill("Math"),
            Skill("Programming")
        ]

        dictObjectData: dict = Parser.SerializeToDict(uUser)

        self.assertDictEqual(
            dictObjectData,
            {
                "strName": "Nguyen The Thao",
                "skiSkills": [
                    {
                        "strName": "Math",
                    },
                    {
                        "strName": "Programming",
                    }
                ]
            }
        )
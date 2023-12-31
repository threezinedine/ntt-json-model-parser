# ntt-json-model-parser
The project for parsing the data from .json file (use json format) to a object in Python

## Usage

Firstly, define the model.

```python
from ntt_json_model_parser import Parser, ModelProperty, Model, Property



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
```

Then using

```python
dictObjectData = {
    "strName": "Thao Nguyen The",
    "nAge": 23,
    "lecLecture": None
}

perFirstStudent: Person = Parser.DeSerializeFromDict(Person, dictObjectData)

# The student will have the name: `Nguyen The Thao` and the lecture with default value

```


```python
dictObjectData = {
    "strName": "Thao Nguyen The",
    "nAge": 23,
}

perFirstStudent: Person = Parser.DeSerializeFromDict(Person, dictObjectData)

dictSerializedData = Parser.SerializeToDict(perFirstStudent)
```

The same result for the `Serialize` method
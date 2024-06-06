from src.main import BaseModel
from src.validator import root_validator, validator


def test_validator_handles_multiple_fields():
    class TestModel(BaseModel):
        a: str
        b: str

        @validator("a", "b")
        def lower_case(cls, v):
            return v.lower()

    test_model = TestModel(a="AAA", b="BBB")
    assert test_model.a == "aaa"
    assert test_model.b == "bbb"


def test_validator_handles_applying_multiple_validators_to_single_field():
    class TestModel(BaseModel):
        a: str

        @validator("a")
        def surround_with_x(cls, v):
            return f"x{v}x"

        @validator("a")
        def surround_with_y(cls, v):
            return f"y{v}y"

    test_model = TestModel(a="aaa")
    assert test_model.a == "yxaaaxy"


def test_root_validator_modifies_input_kwargs():
    class TestModel(BaseModel):
        first_name: str
        last_name: str
        full_name: str

        @root_validator()
        def build_full_name(cls, values):
            values["full_name"] = values["first_name"] + " " + values["last_name"]
            return values

    test_model = TestModel(first_name="Uncle", last_name="Bob")
    assert test_model.full_name == "Uncle Bob"

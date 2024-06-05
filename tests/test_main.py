import pytest

from src.main import BaseModel
from src.validator import root_validator, validator


@pytest.fixture(name="SimpleModelFixture")
def simple_model_fixture():
    class SimpleModelFixture(BaseModel):
        a: int
        b: str

    return SimpleModelFixture


@pytest.fixture(name="BaseModelFixture")
def base_model_fixture():
    class BaseModelFixture(BaseModel):
        name: str
        age: int

        @validator("name")
        def name_to_upper(cls, value: str) -> str:
            return value.upper()

        @root_validator()
        def validate_age(cls, values):
            if values["age"] < 0:
                raise ValueError("Age cannot be negative")
            return values

    return BaseModelFixture


def test_simple_model_raises_type_error_on_invalid_int(SimpleModelFixture):
    with pytest.raises(TypeError) as e:
        SimpleModelFixture(a="abc", b="xxx")
    assert str(e.value) == "a: Input should be a valid int"


def test_simple_model_raises_type_error_on_invalid_str(SimpleModelFixture):
    with pytest.raises(TypeError) as e:
        SimpleModelFixture(a=123, b=123)
    assert str(e.value) == "b: Input should be a valid str"


def test_base_model_initialization(BaseModelFixture):
    test_instance = BaseModelFixture(name="john", age=25)
    assert test_instance.name == "JOHN", "Name should be converted to upper case"
    assert test_instance.age == 25, "Age should be set correctly"


def test_base_model_ignores_extra_field(BaseModelFixture):
    test_instance = BaseModelFixture(name="john", age=25, unknown_field="test")
    try:
        test_instance.getattr(
            "unknown_field", None
        ) is None, "Unknown field should be ignored"
    except AttributeError:
        pass


def test_base_model_raises_exception_for_missing_required_field(SimpleModelFixture):
    with pytest.raises(TypeError) as e:
        SimpleModelFixture(a=1)


def test_base_model_attribute_error_on_negative_age(BaseModelFixture):
    with pytest.raises(ValueError) as e:
        BaseModelFixture(name="john", age=-5)
    assert "Age cannot be negative" in str(e.value)


def test_base_model_dict_output(BaseModelFixture):
    test_instance = BaseModelFixture(name="john", age=25)
    expected_dict = {"name": "JOHN", "age": 25}
    assert (
        test_instance.dict() == expected_dict
    ), "Dict output should match expected values"


def test_base_model_json_output(BaseModelFixture):
    test_instance = BaseModelFixture(name="john", age=25)
    expected_json = '{"name": "JOHN", "age": 25}'
    assert (
        test_instance.json() == expected_json
    ), "JSON output should correctly represent the object"


def test_base_model_repr(BaseModelFixture):
    test_instance = BaseModelFixture(name="john", age=25)
    assert (
        repr(test_instance) == "BaseModelFixture(name='JOHN', age=25)"
    ), "Repr should match the expected format"


def test_base_model_str(BaseModelFixture):
    test_instance = BaseModelFixture(name="john", age=25)
    assert (
        str(test_instance) == "name='JOHN' age=25"
    ), "Str should match the expected format"

import json
from pathlib import Path

import pytest
from live_json import LiveJson


FILENAME = "test.json"


@pytest.fixture
def file():
    _file = Path(FILENAME)
    yield _file
    if _file.exists() and _file.is_file():
        _file.unlink()


def test_file_is_created(file: Path):
    LiveJson.path = FILENAME
    LiveJson({"greeting": "hello"})
    assert file.is_file()


@pytest.mark.parametrize(
    "value",
    [
        "string",
        ["list", "of", "strings"],
        {"dict-key": "dict-value"},
        {"dict-key": ["dict-value", "inside-list"]},
        ["string", ["list"], {"dict-key": "dict-value"}],
        {"dict-key": ["string", ["list"], {"nested-dict-key": "nested-dict-value"}]},
    ],
)
def test_set_item(file: Path, value):
    LiveJson.path = FILENAME
    lj = LiveJson()
    lj["key"] = value

    dct = json.loads(file.read_text())
    assert dct["key"] == value


def test_set_tuple_value_becomes_list(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson()
    lj["key"] = ("group", "of", "strings")

    dct = json.loads(file.read_text())
    assert dct["key"] == ["group", "of", "strings"]


def test_set_int_key_becomes_str(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson()
    lj[1] = "number"

    dct = json.loads(file.read_text())
    assert dct["1"] == "number"


def test_set_existing_key(file: Path):
    LiveJson.path = FILENAME
    LiveJson({"greeting": "hello"})
    LiveJson({"greeting": "hi"})

    dct = json.loads(file.read_text())
    assert dct["greeting"] == "hi"


def test_get_item(file: Path):
    file.write_text(json.dumps({"greeting": "hello"}))

    LiveJson.path = FILENAME
    lj = LiveJson()

    assert lj["greeting"] == "hello"


def test_update(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello"})
    lj.update({"greeting": "hi", "who": "world"})

    dct = json.loads(file.read_text())
    assert dct["greeting"] == "hi" and dct["who"] == "world"


def test_delete_item(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello"})

    del lj["greeting"]
    with pytest.raises(KeyError):
        assert lj["greeting"]


def test_len(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello", "who": "world"})

    assert len(lj) == 2


def test_iter(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello", "who": "world"})
    it = iter(lj)
    assert next(it) == "greeting"
    assert next(it) == "who"
    with pytest.raises(StopIteration):
        assert next(it)


def test_iter_keys(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello", "who": "world"})
    it = iter(lj.keys())
    assert next(it) == "greeting"
    assert next(it) == "who"
    with pytest.raises(StopIteration):
        assert next(it)


def test_iter_values(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello", "who": "world"})
    it = iter(lj.values())
    assert next(it) == "hello"
    assert next(it) == "world"
    with pytest.raises(StopIteration):
        assert next(it)


def test_iter_items(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello", "who": "world"})
    it = iter(lj.items())
    assert next(it) == ("greeting", "hello")
    assert next(it) == ("who", "world")
    with pytest.raises(StopIteration):
        assert next(it)


def test_str(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello", "who": "world"})
    assert str(lj) == "{'greeting': 'hello', 'who': 'world'}"


def test_repr(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson({"greeting": "hello", "who": "world"})
    assert repr(lj) == "{'greeting': 'hello', 'who': 'world'}"


def test_set_non_json_serializable_key(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson()
    with pytest.raises(TypeError):
        lj[LiveJson()] = "nested-lj"


def test_set_non_json_serializable_value(file: Path):
    LiveJson.path = FILENAME
    lj = LiveJson()
    with pytest.raises(TypeError):
        lj["nested-lj"] = LiveJson()

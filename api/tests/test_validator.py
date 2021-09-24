import pytest
from pydantic import BaseModel

from src.validator import InvalidSchemaException, LDJsonValidator


class Item(BaseModel):
    hoge: str
    fuga: int


@pytest.fixture
def validator() -> LDJsonValidator:
    return LDJsonValidator(Item)


@pytest.mark.asyncio
async def test_valid_data(validator: LDJsonValidator):
    validator.write(b'{"hoge": "test", "fuga": 1}\n')
    assert validator._buffer == b''


@pytest.mark.asyncio
async def test_invalid_data(validator: LDJsonValidator):
    with pytest.raises(InvalidSchemaException):
        validator.write(b'{"hoge": "test"}\n')


@pytest.mark.asyncio
async def test_write_some_chunk(validator: LDJsonValidator):
    validator.write(
        b'{"hoge": "test1", "fuga": 1}\n{"hoge": "test1", "fuga": 2}\n')
    assert validator._buffer == b''
    validator.write(
        b'{"hoge": "test2", "fuga": 3}\n{"hoge": "test2", "fuga": 4}\n')
    assert validator._buffer == b''


@pytest.mark.asyncio
async def test_write_with_small_chunk(validator: LDJsonValidator):
    validator.write(b'{"hoge": "test1')
    assert validator._buffer == b'{"hoge": "test1'
    validator.write(b'", "fuga"')
    assert validator._buffer == b'{"hoge": "test1", "fuga"'
    validator.write(b': 1}\n')
    assert validator._buffer == b''


@pytest.mark.asyncio
async def test_write_with_large_chunk(validator: LDJsonValidator):
    validator.write(
        b'{"hoge": "test1", "fuga": 1}\n'
        b'{"hoge": "test1", "fuga": 2}\n{"hoge": "test2"')
    assert validator._buffer == b'{"hoge": "test2"'

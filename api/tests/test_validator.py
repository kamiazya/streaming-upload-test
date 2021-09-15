import pytest
from pydantic import BaseModel, ValidationError

from src.validator import JDJsonValidator


class Item(BaseModel):
    hoge: str
    fuga: int


@pytest.fixture
def validator() -> JDJsonValidator:
    return JDJsonValidator(Item)


@pytest.mark.asyncio
async def test_valid_data(validator: JDJsonValidator):
    await validator.write(b'{"hoge": "test", "fuga": 1}\n')
    assert validator._buffer == b''


@pytest.mark.asyncio
async def test_invalid_data(validator: JDJsonValidator):
    with pytest.raises(ValidationError):
        await validator.write(b'{"hoge": "test"}\n')


@pytest.mark.asyncio
async def test_write_some_chunk(validator: JDJsonValidator):
    await validator.write(b'{"hoge": "test1", "fuga": 1}\n{"hoge": "test1", "fuga": 2}\n')
    assert validator._buffer == b''
    await validator.write(b'{"hoge": "test2", "fuga": 3}\n{"hoge": "test2", "fuga": 4}\n')
    assert validator._buffer == b''


@pytest.mark.asyncio
async def test_write_with_small_chunk(validator: JDJsonValidator):
    await validator.write(b'{"hoge": "test1')
    assert validator._buffer == b'{"hoge": "test1'
    await validator.write(b'", "fuga"')
    assert validator._buffer == b'{"hoge": "test1", "fuga"'
    await validator.write(b': 1}\n')
    assert validator._buffer == b''


@pytest.mark.asyncio
async def test_write_with_large_chunk(validator: JDJsonValidator):
    await validator.write(b'{"hoge": "test1", "fuga": 1}\n{"hoge": "test1", "fuga": 2}\n{"hoge": "test2"')
    assert validator._buffer == b'{"hoge": "test2"'

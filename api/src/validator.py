# from io import BinaryIO
from typing import Any
from typing import Dict
from typing import List
from typing import Type

import orjson
from pydantic import BaseModel
from pydantic import ValidationError


class InvalidSchemaException(Exception):
    line: int
    data: Dict[str, Any]
    errors: List[Dict[str, Any]]

    def __init__(self, line: int, data: Dict[str, Any], errors: List[Dict[str, Any]]) -> None:
        self.line = line
        self.data = data
        self.errors = errors

    def dict(self):
        return {
            "line": self.line,
            "data": self.data,
            "errors": self.errors,
        }


class LDJsonValidator:
    def __init__(self, model_cls: Type[BaseModel]) -> None:
        self.model_cls = model_cls
        self._buffer = bytes()
        self.line = 1

    def write(self, chunk: bytes) -> None:
        try:
            if len(self._buffer) >= 1:
                chunk = self._buffer + chunk
                self._buffer = bytes()
            for line in chunk.splitlines(True):
                if line.endswith(b"\n"):
                    data = orjson.loads(line)
                    self.model_cls(**data)
                else:
                    self._buffer += line
                self.line += 1
        except ValidationError as err:
            raise InvalidSchemaException(
                line=self.line,
                data=data,
                errors=err.errors(),
            )

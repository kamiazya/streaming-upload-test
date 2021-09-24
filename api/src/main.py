from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from pydantic import BaseModel

from validator import InvalidSchemaException
from validator import LDJsonValidator

app = FastAPI()


class Item(BaseModel):
    hoge: str
    fuga: int


@app.post("/")
async def upload(request: Request, response: Response):
    chunk_sizes = []
    validator = LDJsonValidator(Item)
    try:
        async for chunk in request.stream():
            validator.write(chunk)
            if chunk_size := len(chunk):
                chunk_sizes.append(chunk_size)

        return {
            "chunkSizes": chunk_sizes,
            "totalSize": sum(chunk_sizes),
            "maxSize": max(chunk_sizes),
            "minSize": min(chunk_sizes),
        }
    except InvalidSchemaException as err:
        response.status_code = 400
        return err.dict()

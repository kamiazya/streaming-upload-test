from fastapi import FastAPI
from fastapi import Request, Response
from pydantic import BaseModel

from validator import JDJsonValidator, InvalidSchemaException

app = FastAPI()


class Item(BaseModel):
    hoge: str
    fuga: int

@app.post("/")
async def upload(request: Request, response: Response):
    chunk_sizes = []
    validator = JDJsonValidator(Item)
    try:
        async for chunk in request.stream():
            validator.write(chunk)
            chunk_sizes.append(len(chunk))

        return {
            "chunkSizes": chunk_sizes,
            "totalSize": sum(chunk_sizes),
            "maxSize": max(chunk_sizes),
            "minSize": min(chunk_sizes),
        }
    except InvalidSchemaException as err:
        response.status_code = 400
        return err.dict()

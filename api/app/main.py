from fastapi import FastAPI, Request

app = FastAPI()

@app.post('/')
async def upload(request: Request):
    chunk_sizes = [len(chunk) async for chunk in request.stream()][:-1]
    return {
        'chunkSizes': chunk_sizes,
        'totalSize': sum(chunk_sizes),
        'maxSize': max(chunk_sizes),
        'minSize': min(chunk_sizes),
    }

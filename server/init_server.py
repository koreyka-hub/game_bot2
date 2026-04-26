from fastapi import FastAPI
from fastapi.responses import FileResponse
def init_fastapi():
    app = FastAPI()
    @app.get('/')
    async def main():
        return FileResponse('site_abtme.html')
    return app
app = init_fastapi()
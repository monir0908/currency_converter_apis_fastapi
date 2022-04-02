from fastapi import FastAPI, APIRouter
from starlette.responses import RedirectResponse
import uvicorn
from apis import currency_apis, home

# instance created (i.e. app) of the FastAPI blueprint
app = FastAPI()

# home and currency_apis routers are hooked up with the 'app'
app.include_router(currency_apis.router)
app.include_router(home.router)



@app.get("/documentation", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)


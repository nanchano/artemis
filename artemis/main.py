from fastapi import FastAPI

from artemis import routes

app = FastAPI(
    title="Artemis",
    description="Create, Read, Update and Delete events through a REST API",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


@app.get("/ping")
def ping() -> str:
    return "pong"


app.include_router(routes.router)

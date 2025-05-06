from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine,get_db
from api.endpoints import brief_router, top_influencers_router
Base.metadata.create_all(bind=engine)

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = FastAPI.openapi(app)  
    openapi_schema["info"]["title"] = "Marketing Backend"
    openapi_schema["info"]["version"] = "1.1.0"
    openapi_schema["info"]["description"] = "This API serves as the backend for WOFR."
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#app.mount("/static", StaticFiles(directory="static"), name="static")

#app.include_router(user_router, prefix="/api", tags=["User Auth"])
app.include_router(brief_router, prefix="/api", tags=["marketing campaign"])
app.include_router(top_influencers_router, prefix="/api", tags=["top influencers"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8004, reload= True, host="0.0.0.0")
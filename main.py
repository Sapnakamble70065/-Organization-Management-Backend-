from fastapi import FastAPI
from .routers import orgs, auth

app = FastAPI(title="Org Management Service")

# Connecting Routers
app.include_router(auth.router, tags=["Admin Auth"])
app.include_router(orgs.router, tags=["Organizations"])

@app.get("/")
async def home():
    return {"message": "Org Management Service Running"}

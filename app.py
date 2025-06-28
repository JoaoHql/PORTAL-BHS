from fastapi import FastAPI
from routes import router as rest_router
from socket_server import router as ws_router

app = FastAPI()

# Include REST API routes
app.include_router(rest_router)

# Include WebSocket routes
app.include_router(ws_router)
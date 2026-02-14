
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, data

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(data.router, prefix="/api", tags=["data"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to NEPSE Hub API"}

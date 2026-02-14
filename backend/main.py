
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, data
import os

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(data.router, prefix="/api", tags=["data"])

# Serve Static Files (Frontend)
# We serve the root directory as static to handle the existing structure
# index.html is in the root, /src and /pages are subdirectories.
# This might need adjustment depending on how you want to serve the app.
# For now, we mount specific directories and a catch-all for root files.

# Serve Static Files (Frontend) - Only if they exist
static_dirs = ["src", "pages", "img", "docs"]
for dir_name in static_dirs:
    dir_path = os.path.join(os.getcwd(), dir_name)
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        app.mount(f"/{dir_name}", StaticFiles(directory=dir_name), name=dir_name)

from fastapi.responses import FileResponse

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/{filename}")
async def read_root_file(filename: str):
    # Security: Ensure filename doesn't contain path traversal
    if ".." in filename or "/" in filename:
        return FileResponse('index.html') # Fallback
        
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse('index.html') # Fallback for SPA routing if needed

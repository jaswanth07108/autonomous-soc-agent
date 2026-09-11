import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from data.database import init_db
from data.seed_data import seed_sandbox_data
from api.routes import router as api_router

app = FastAPI(
    title="AegisSOC - Autonomous SOC Investigation & Response Agent",
    description="Agentic AI SOC Investigation & Response Engine for Tech Zephyr 4.0 Hackathon",
    version="1.0.0"
)

# Enable CORS for React frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    try:
        seed_sandbox_data()
    except Exception as e:
        print(f"Startup seed notice: {e}")

# Include API routes
app.include_router(api_router)

# Mount React static build files if present
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        if full_path.startswith("api"):
            return None
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "system": "AegisSOC Engine", "mode": "SANDBOX_SIMULATED"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

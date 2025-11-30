from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    """
    Application factory for better structure and easier testing.
    """
    app = FastAPI(
        title="User Registration API",
        version="1.0.0",
        description="Simple API supporting user registration and activation with 4-digit code.",
    )

    # Allow any frontend to call the API (optional, but common in real APIs)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Optional: health check endpoint
    @app.get("/health", tags=["system"])
    def health_check():
        return {"status": "ok"}

    return app


# Create the FastAPI app instance
app = create_app()

from fastapi.middleware.cors import CORSMiddleware

def add_cors(app, origins: list[str] | None = None):
    origins = origins or ["*"]  # dev-only; tighten in prod
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

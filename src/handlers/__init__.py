from .download import router as download_router
from .start import router as start_router


routers = [
    start_router,
    download_router,
]

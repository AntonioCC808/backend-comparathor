from fastapi import FastAPI, APIRouter

from app.middlewares.cors import add_cors
from app.routes import auth, products, comparisons

# Initialize FastAPI
app = FastAPI(
    title="Comparathor",
    version="1.0.0",
    docs_url="/api/docs",
    description="Application 'Comparathor' for managing products, comparisons, "
    "and metadata.",
)

add_cors(app)

# Create API Router
api_router = APIRouter(
    prefix="/api/v1",
)

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(
    comparisons.router, prefix="/comparisons", tags=["Comparisons"]
)

# Add API Router to the main app
app.include_router(api_router)

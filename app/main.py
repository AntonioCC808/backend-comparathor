from fastapi import FastAPI
from app.routes import auth, products, comparisons
from app.database import Base, engine

# Inicializar FastAPI
app = FastAPI()

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(comparisons.router, prefix="/comparisons", tags=["Comparisons"])
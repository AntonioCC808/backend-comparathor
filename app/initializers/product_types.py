import yaml
from pkg_resources import resource_filename
from app.database import SessionLocal
from app.models.product import ProductType
from app.utils import get_logger

logger = get_logger("PRODUCT-TYPES-INITIALIZER")


def _init_product_types(product_types: list):
    logger.info("Initializing product types...")

    with SessionLocal() as session:
        init_product_types = [
            ProductType(
                id=product_type["id"],
                name=product_type["name"],
                description=product_type["description"],
                metadata_schema=product_type["metadata_schema"],
            )
            for product_type in product_types
        ]
        for product_type in init_product_types:
            if session.query(ProductType).filter(ProductType.id == product_type.id).first():
                logger.debug(f"Skipping product type {product_type.id}, already exists.")
                continue
            session.add(product_type)
        session.commit()
        logger.info("Product types initialized.")


def load():
    with open(resource_filename("app", "resources/products.yml")) as f:
        data = yaml.safe_load(f)
    _init_product_types(data["product_types"])

import yaml
from pkg_resources import resource_filename
from app.database import SessionLocal
from app.models.product import ProductMetadata
from app.utils.logger import get_logger

logger = get_logger("PRODUCT-METADATA-INITIALIZER")


def _init_product_metadata(metadata: list):
    logger.info("Initializing product metadata...")

    with SessionLocal() as session:
        init_metadata = [
            ProductMetadata(
                id=meta["id"],
                id_product=meta["id_product"],
                attribute=meta["attribute"],
                value=meta["value"],
                score=meta["score"],
            )
            for meta in metadata
        ]
        for meta in init_metadata:
            if session.query(ProductMetadata).filter(ProductMetadata.id == meta.id).first():
                logger.debug(f"Skipping metadata {meta.id}, already exists.")
                continue
            session.add(meta)
        session.commit()
        logger.info("Product metadata initialized.")


def load():
    with open(resource_filename("app", "resources/products.yml")) as f:
        data = yaml.safe_load(f)
    _init_product_metadata(data["product_metadata"])

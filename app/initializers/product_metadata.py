import yaml
from pkg_resources import resource_filename
from app.database import get_db
from app.models.product import ProductMetadata
from app.utils import get_logger

logger = get_logger("PRODUCT-METADATA-INITIALIZER")


def _init_product_metadata(metadata: list):
    logger.info("Initializing product metadata...")

    # Use get_db to get a session
    session = next(get_db())
    init_metadata = [
        ProductMetadata(
            id=meta["id"],
            product_id=meta["product_id"],
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

import yaml
from pkg_resources import resource_filename
from app.database import get_db
from app.models.comparison import ComparisonProduct
from app.utils import get_logger

logger = get_logger("COMPARISON-PRODUCTS-INITIALIZER")


def _init_comparison_products(comparison_products: list):
    logger.info("Initializing comparison products...")

    # Use get_db to get a session
    session = next(get_db())
    init_comparison_products = [
        ComparisonProduct(
            id=cp["id"],
            comparison_id=cp["comparison_id"],
            product_id=cp["product_id"],
        )
        for cp in comparison_products
    ]
    for cp in init_comparison_products:
        if session.query(ComparisonProduct).filter(ComparisonProduct.id == cp.id).first():
            logger.debug(f"Skipping comparison product {cp.id}, already exists.")
            continue
        session.add(cp)
    session.commit()
    logger.info("Comparison products initialized.")


def load():
    with open(resource_filename("app", "resources/comparisons.yml")) as f:
        data = yaml.safe_load(f)
    _init_comparison_products(data["comparison_products"])

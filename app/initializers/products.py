from typing import List
import yaml
from app.database import get_db
from app.models.product import Product, ProductType
from app.utils import get_logger
from pkg_resources import resource_filename

logger = get_logger("PRODUCTS-INITIALIZER")


def _init_products(products: List[dict], product_types: List[dict]):
    """
    Initialize product types and products in the database.

    Parameters
    ----------
    products : List[dict]
        A list of products data to initialize in the database.
    product_types : List[dict]
        A list of product type data to initialize in the database.

    Returns
    -------
    None
        This function does not return a value.
    """
    logger.info("Initializing product types and products...")

    # Use get_db to get a session
    session = next(get_db())
    # Initialize Product Types
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
            logger.debug(f"Skipping product type {product_type.id} as it already exists")
            continue
        session.add(product_type)

    # Initialize Products
    init_products = [
        Product(
            id=product["id"],
            product_type_id=product["product_type_id"],
            user_id=product["user_id"],
            name=product["name"],
            price=product["price"],
            image_base64=product["image"],
            brand=product["brand"],
            score=product["score"],
        )
        for product in products
    ]

    for product in init_products:
        if session.query(Product).filter(Product.id == product.id).first():
            logger.debug(f"Skipping product {product.id} as it already exists")
            continue
        session.add(product)

    # Commit
    session.commit()
    logger.info("Products and product types initialized")


def load():
    """
    Load products and product types from a YAML file.

    Returns
    -------
    None
        This function does not return a value.
    """
    with open(resource_filename("app", "resources/products.yml")) as f:
        data = yaml.safe_load(f)

    _init_products(data["products"], data["product_types"])

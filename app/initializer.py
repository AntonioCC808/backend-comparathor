from app.initializers import users, product_types, products, product_metadata, comparisons, comparison_products

def initialize_all():
    """
    Initialize all database tables with predefined data from YAML files.

    This function sequentially calls the `load` functions of all the initializers
    to populate the database with data for testing or seeding purposes.

    Steps performed:
        - Load users data from `users.yml`.
        - Load product types data from `product_types.yml`.
        - Load products data from `products.yml`.
        - Load product metadata data from `product_metadata.yml`.
        - Load comparisons data from `comparisons.yml`.
        - Load comparison products data from `comparison_products.yml`.

    Returns
    -------
    None
        This function does not return a value.
    """
    users.load()
    product_types.load()
    products.load()
    product_metadata.load()
    comparisons.load()
    comparison_products.load()


from typing import List
import yaml
from pkg_resources import resource_filename
from app.database import get_db
from app.models.comparison import Comparison
from app.utils import get_logger

logger = get_logger("COMPARISONS-INITIALIZER")


def _init_comparisons(comparisons: List[dict]):
    """
    Initialize comparisons in the database.

    Parameters
    ----------
    comparisons : List[dict]
        A list of comparison data to initialize in the database.

    Returns
    -------
    None
        This function does not return a value.
    """
    logger.info("Initializing comparisons...")

    # Use get_db to get a session
    session = next(get_db())
    init_comparisons = [
        Comparison(
            id=comparison["id"],
            id_user=comparison["id_user"],
            title=comparison["title"],
            description=comparison["description"],
            date_created=comparison["date_created"],
            product_type_id=comparison["product_type_id"],
        )
        for comparison in comparisons
    ]

    for comparison in init_comparisons:
        if session.query(Comparison).filter(Comparison.id == comparison.id).first():
            logger.debug(f"Skipping comparison {comparison.id} as it already exists")
            continue
        session.add(comparison)

    session.commit()
    logger.info("Comparisons initialized")


def load():
    """
    Load comparisons from a YAML file.

    Returns
    -------
    None
        This function does not return a value.
    """
    with open(resource_filename("app", "resources/comparisons.yml")) as f:
        data = yaml.safe_load(f)

    _init_comparisons(data["comparisons"])

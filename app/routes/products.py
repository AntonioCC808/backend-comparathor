from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductDTO
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=list[ProductDTO])
def get_products(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[ProductDTO]:
    """
    Retrieve a list of products.

    Parameters
    ----------
    skip : int, optional
        The number of records to skip (default is 0).
    limit : int, optional
        The maximum number of records to return (default is 10).
    db : Session
        The database session dependency.

    Returns
    -------
    list[ProductOut]]
        A list of product records.
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return [
        ProductDTO(
            name=product.name,
            brand=product.brand,
            score=product.score,
            id=product.id,
            id_user=product.id_user,
        )
        for product in products
    ]


@router.post("/", response_model=ProductDTO)
def create_product(product: ProductCreate, db: Session = Depends(get_db)) -> ProductDTO:
    """
    Create a new product record.

    Parameters
    ----------
    product : ProductCreate
        The details of the product to be created.
    db : Session
        The database session dependency.

    Returns
    -------
    ProductDTO
        The newly created product record.
    """
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return ProductDTO(
        name=new_product.name,
        brand=new_product.brand,
        score=new_product.score,
        id=new_product.id,
        id_user=new_product.id_user,
    )


@router.put("/{product_id}", response_model=ProductDTO)
def update_product(
    product_id: int, product: ProductCreate, db: Session = Depends(get_db)
) -> ProductDTO:
    """
    Update an existing product record.

    Parameters
    ----------
    product_id : int
        The ID of the product to update.
    product : ProductCreate
        The updated product details.
    db : Session
        The database session dependency.

    Returns
    -------
    ProductOutº
        The updated product record.

    Raises
    ------
    HTTPException
        If the product is not found.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return ProductDTO(
        name=db_product.name,
        brand=db_product.brand,
        score=db_product.score,
        id=db_product.id,
        id_user=db_product.id_user,
    )


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a product record.

    Parameters
    ----------
    product_id : int
        The ID of the product to delete.
    db : Session
        The database session dependency.

    Returns
    -------
    dict
        A confirmation message indicating successful deletion.

    Raises
    ------
    HTTPException
        If the product is not found.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted successfully"}

@router.get("/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductDTO:
    """
    Retrieve a single product by its ID.

    Parameters
    ----------
    product_id : int
        The ID of the product to retrieve.
    db : Session
        The database session dependency.

    Returns
    -------
    ProductDTO
        The product record.

    Raises
    ------
    HTTPException
        If the product is not found.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductDTO(
        name=product.name,
        brand=product.brand,
        score=product.score,
        id=product.id,
        id_user=product.id_user,
    )
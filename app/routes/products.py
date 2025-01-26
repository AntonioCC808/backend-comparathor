from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product, ProductType
from app.schemas.product import ProductCreate, ProductDTO, ProductTypeDTO
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
    return [ProductDTO.model_validate(product)for product in products]


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
    return ProductDTO.model_validate(new_product)


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
    return ProductDTO.model_validate(product)


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
    return ProductDTO.model_validate(product)


@router.get("/product-types", response_model=List[ProductTypeDTO])
def get_product_types(db: Session = Depends(get_db)) -> List[ProductTypeDTO]:
    """
    Retrieve a list of all product types.

    Parameters
    ----------
    db : Session
        The database session dependency.

    Returns
    -------
    list[ProductTypeDTO]
        A list of all product types.
    """
    product_types = db.query(ProductType).all()
    return [ProductTypeDTO.model_validate(product_type) for product_type in product_types]

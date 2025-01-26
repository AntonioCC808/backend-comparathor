from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product, ProductMetadata
from app.schemas.product import ProductCreate, ProductDTO, ProductUpdate
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
    return [ProductDTO.model_validate(product) for product in products]


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

    db.flush()  # Get the ID of the newly created product

    # Add metadata
    for meta in product.product_metadata or []:
        new_metadata = ProductMetadata(
            id_product=new_product.id,
            attribute=meta.attribute,
            value=meta.value,
            score=meta.score,
        )
        db.add(new_metadata)

    db.commit()
    db.refresh(new_product)
    return ProductDTO.model_validate(new_product)


@router.put("/{product_id}", response_model=ProductDTO)
def update_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
) -> ProductDTO:
    """
    Update an existing product record.

    Parameters
    ----------
    product_id : int
        The ID of the product to update.
    product : ProductUpdate
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
    # Update product details
    for key, value in product.model_dump().items():
        if key != "product_metadata" and value is not None:
            setattr(db_product, key, value)

    # Update metadata
    for meta in product.product_metadata or []:
        if meta.id:
            db_metadata = db.query(ProductMetadata).filter(ProductMetadata.id == meta.id).first()
            if db_metadata:
                for key, value in meta.model_dump().items():
                    if value is not None:
                        setattr(db_metadata, key, value)
        else:
            new_metadata = ProductMetadata(
                id_product=product_id,
                attribute=meta.attribute,
                value=meta.value,
                score=meta.score,
            )
            db.add(new_metadata)

    db.commit()
    db.refresh(db_product)
    return ProductDTO.model_validate(db_product)


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

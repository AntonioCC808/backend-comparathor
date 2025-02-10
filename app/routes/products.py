from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product, ProductMetadata
from app.schemas.product import ProductCreate, ProductDTO, ProductUpdate
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=list[ProductDTO])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[ProductDTO]:
    """
    Retrieve a list of products.
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return [ProductDTO.model_validate(product) for product in products]


@router.post("/", response_model=ProductDTO)
def create_product(product: ProductCreate, db: Session = Depends(get_db)) -> ProductDTO:
    """
    Create a new product record with an image in Base64 format.
    """
    new_product = Product(
        name=product.name,
        brand=product.brand,
        score=product.score,
        id_user=product.id_user,
        product_type_id=product.product_type_id,
        image_base64=product.image_base64,  # ✅ Save image in Base64 format
    )

    db.add(new_product)
    db.flush()  # Get the new product ID

    # Add metadata attributes
    for meta in product.product_metadata or []:
        new_metadata = ProductMetadata(
            product_id=new_product.id,
            attribute=meta.attribute,
            value=meta.value,
            score=meta.score,
        )
        db.add(new_metadata)

    db.commit()
    db.refresh(new_product)
    return ProductDTO.model_validate(new_product)


@router.put("/{product_id}", response_model=ProductDTO)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)) -> ProductDTO:
    """
    Update an existing product record, including updating the image in Base64.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update product details including the Base64 image
    for key, value in product.model_dump().items():
        if key != "product_metadata" and value is not None:
            setattr(db_product, key, value)

    # Update or add metadata attributes
    for meta in product.product_metadata or []:
        if meta.product_id:
            db_metadata = db.query(ProductMetadata).filter(ProductMetadata.id == meta.product_id).first()
            if db_metadata:
                for key, value in meta.model_dump().items():
                    if value is not None:
                        setattr(db_metadata, key, value)
        else:
            new_metadata = ProductMetadata(
                product_id=product_id,
                attribute=meta.attribute,
                value=meta.value,
                score=meta.score,
            )
            db.add(new_metadata)

    db.commit()
    db.refresh(db_product)
    return ProductDTO.model_validate(db_product)


@router.get("/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductDTO:
    """
    Retrieve a single product by its ID, including the Base64 image.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductDTO.model_validate(product)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a product record.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted successfully"}

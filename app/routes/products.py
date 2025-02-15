from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product, ProductMetadata
from app.models.user import User
from app.schemas.product import ProductCreate, ProductDTO, ProductUpdate
from app.database import get_db
from app.utils import get_current_user

router = APIRouter()


@router.get("/", response_model=list[ProductDTO])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[ProductDTO]:
    """
    Retrieve a list of products.
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return [ProductDTO.model_validate(product) for product in products]


@router.get("/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductDTO:
    """
    Retrieve a single product by its ID, including the Base64 image.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductDTO.model_validate(product)


router = APIRouter()


@router.post("/", response_model=ProductDTO)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ✅ Require authentication
) -> ProductDTO:
    """
    Create a new product record with an image in Base64 format.
    """
    new_product = Product(
        name=product.name,
        brand=product.brand,
        score=product.score,
        user_id=current_user.user_id,
        product_type_id=product.product_type_id,
        image_base64=product.image_base64,
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
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ✅ Require authentication
) -> ProductDTO:
    """
    Update an existing product record, ensuring only the owner or an admin can modify it.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ensure only the product owner or an admin can update the product
    if db_product.user_id != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to edit this product")

    # Update product details
    for key, value in product.model_dump().items():
        if key not in ["product_metadata", "user_id", "product_type_id"] and value is not None:
            setattr(db_product, key, value)

    # Update or add metadata attributes
    for meta in product.product_metadata or []:
        db_metadata = db.query(ProductMetadata).filter(
            ProductMetadata.product_id == product_id, ProductMetadata.attribute == meta.attribute
        ).first()
        if db_metadata:
            for key, value in meta.model_dump().items():
                if value is not None:
                    setattr(db_metadata, key, value)

    db.commit()
    db.refresh(db_product)
    return ProductDTO.model_validate(db_product)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ✅ Require authentication
) -> dict:
    """
    Delete a product record, ensuring only the owner or an admin can delete it.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ensure only the product owner or an admin can delete the product
    if db_product.user_id != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")

    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted successfully"}



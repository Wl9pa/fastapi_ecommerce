from pydantic import BaseModel, EmailStr, conint


class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class CreateReview(BaseModel):
    product_id: int
    comment: str
    grade: int = conint(ge=1, le=5)

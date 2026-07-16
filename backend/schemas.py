from pydantic import BaseModel, EmailStr
from typing import Optional, List


# ---------- Plant ----------

class PlantCreate(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    description: str = ""
    image_url: str = ""


class PlantUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class PlantOut(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int
    description: str
    image_url: str

    class Config:
        from_attributes = True


# ---------- Auth / User ----------

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Cart ----------

class CartItemAdd(BaseModel):
    plant_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    id: int
    plant_id: int
    quantity: int
    plant: PlantOut

    class Config:
        from_attributes = True


# ---------- Order ----------

class OrderItemOut(BaseModel):
    plant_id: int
    quantity: int
    price_at_purchase: float
    plant: PlantOut

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    total: float
    status: str
    items: List[OrderItemOut]

    class Config:
        from_attributes = True

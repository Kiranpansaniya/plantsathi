from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db, Plant, Customer, CartItem, Order, OrderItem
from schemas import (
    PlantOut, PlantCreate, PlantUpdate,
    UserSignup, UserLogin, TokenResponse, UserOut,
    CartItemAdd, CartItemUpdate, CartItemOut,
    OrderOut,
)
from auth import hash_password, verify_password, create_access_token, get_current_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== AUTH ====================

@app.post("/api/auth/signup", response_model=TokenResponse)
def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = Customer(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "user": new_user}


@app.post("/api/auth/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(Customer).filter(Customer.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "user": user}


@app.get("/api/auth/me", response_model=UserOut)
def get_me(current_user: Customer = Depends(get_current_user)):
    return current_user


# ==================== PLANTS (Public - view only) ====================

@app.get("/api/plants", response_model=List[PlantOut])
def get_plants(db: Session = Depends(get_db)):
    return db.query(Plant).all()


@app.get("/api/plants/{plant_id}", response_model=PlantOut)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


# ==================== PLANTS (Login required - any user) ====================

@app.post("/api/plants", response_model=PlantOut)
def create_plant(plant_data: PlantCreate, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    new_plant = Plant(**plant_data.model_dump())
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant


@app.put("/api/plants/{plant_id}", response_model=PlantOut)
def update_plant(plant_id: int, plant_data: PlantUpdate, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    update_data = plant_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plant, key, value)

    db.commit()
    db.refresh(plant)
    return plant


@app.delete("/api/plants/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    db.delete(plant)
    db.commit()
    return {"message": f"Plant '{plant.name}' deleted successfully"}


# ==================== CART (Login required) ====================

@app.get("/api/cart", response_model=List[CartItemOut])
def get_cart(db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    return db.query(CartItem).filter(CartItem.user_id == current_user.id).all()


@app.post("/api/cart", response_model=CartItemOut)
def add_to_cart(item_data: CartItemAdd, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    plant = db.query(Plant).filter(Plant.id == item_data.plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    existing_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.plant_id == item_data.plant_id,
    ).first()

    if existing_item:
        existing_item.quantity += item_data.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    new_item = CartItem(
        user_id=current_user.id,
        plant_id=item_data.plant_id,
        quantity=item_data.quantity,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.put("/api/cart/{item_id}", response_model=CartItemOut)
def update_cart_item(item_id: int, item_data: CartItemUpdate, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id,
    ).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    item.quantity = item_data.quantity
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/cart/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id,
    ).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}


# ==================== ORDERS / CHECKOUT (Login required) ====================

@app.post("/api/checkout", response_model=OrderOut)
def checkout(db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0.0
    order_items_data = []

    for item in cart_items:
        plant = item.plant
        if plant.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {plant.name}",
            )
        line_total = plant.price * item.quantity
        total += line_total
        order_items_data.append((plant, item.quantity, plant.price))

    new_order = Order(user_id=current_user.id, total=total, status="Confirmed")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for plant, qty, price in order_items_data:
        order_item = OrderItem(
            order_id=new_order.id,
            plant_id=plant.id,
            quantity=qty,
            price_at_purchase=price,
        )
        db.add(order_item)
        plant.stock -= qty

    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(new_order)
    return new_order


@app.get("/api/orders", response_model=List[OrderOut])
def get_my_orders(db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()


@app.get("/api/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id,
    ).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
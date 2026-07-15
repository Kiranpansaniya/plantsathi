from fastapi import FastAPI, Depends , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import get_db, Plant,Customer,CartItem,Order,OrderItem
from schemas import PlantOut,TokenResponse,UserSignup,UserLogin,UserOut,PlantCreate,PlantUpdate,CartItemAdd,CartItemUpdate,CartItemOut,OrderOut
from auth import hash_password,verify_password,create_access_token,get_current_user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_admin(current_user: Customer = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail=" Admin access required")
    return current_user

# Auth
@app.post("/api/auth/signup",response_model=TokenResponse)
def signup(user_data:UserSignup,db:Session=Depends(get_db)):
    existing=db.query(Customer).filter(Customer.email==user_data.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="Email already registered")
    new_user=Customer(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "user": new_user}

@app.post("/api/auth/login",response_model=TokenResponse)
def login(credentials:UserLogin,db:Session=Depends(get_db)):
    user=db.query(Customer).filter(Customer.email==credentials.email).first()

    if not user or not verify_password(credentials.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid email or password")
    token = create_access_token({"sub":str(user.id)})
    return {"access_token":token,"user":user}

@app.get("/api/auth/me",response_model=UserOut)
def get_me(current_user:Customer=Depends(get_current_user)):
    return current_user 



# Plants public
@app.get("/api/plants", response_model=List[PlantOut])
def get_plants(db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return plants

@app.get("/api/plants/{plant_id}", response_model=PlantOut)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant Not Found")
    return plant

#Plants (Admin only)
@app.post("/api/plants", response_model=PlantOut)
def create_plant(plant_date: PlantCreate, db: Session = Depends(get_db), admin: Customer = Depends(verify_admin)):
    new_plant = Plant(**plant_date.model_dump())
    db.add(new_plant)
    db.commit()
    return new_plant

@app.put("/api/plants/{plant_id}", response_model=PlantOut)
def update_plant(plant_id: int,plant_data: PlantUpdate, db: Session = Depends(get_db),admin: Customer = Depends(verify_admin)):
    plant= db.query(Plant).filter(Plant.id ==plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail=" Plant Not Found")
    update_data = plant_data.model_dump(exclude_unset =True)
    for key, value in update_data.items():
        setattr(plant,key,value)

    db.commit()
    db.refresh(plant)
    return plant

@app.delete("/api/plants/{plant_id}")
def delete_plant(plant_id: int,db:Session = Depends(get_db),admin: Customer = Depends(verify_admin)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail ="Plant Not Found")
    
    db.delete(plant)
    db.commit()

    return {"message": f"Plant '{plant.name}' Deleted Successfilly"}

#Order/Checkout 

@app.post("/api/checkout", response_model=OrderOut)
def checkout(db: Session = Depends(get_db), current_user: Customer =Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    total = 0.0
    order_items_data = []
    for item in cart_items:
        plant = item.plant
        if plant.stock < item.quantity:
            raise HTTPException (
                status_code=400,
                detail=f"Not Enough Stock For {plant.name}",
            )
        line_total = plant.price * item.quantity
        total += line_total
        order_items_data.append((plant, item.quantity, plant.price))

    new_order = Order(user_id= current_user.id , total = total, status = " Confirmed")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for plant , qty, price in order_items_data:
        order_item = OrderItem(
            order_id =new_order.id,
            plant_id = plant.id,
            quantity = qty,
            price_at_purchase = price,
        )
        db.add(order_item)
        plant.stock -= qty

    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/api/orders", response_model = List[OrderOut])
def get_my_orders(db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()

@app.get("/api/orders/{order_id}",response_model = OrderOut)
def get_order(order_id: int, db: Session = Depends( get_db ), current_user: Customer = Depends (get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id,

    ).first()

    if order is None:
        raise HTTPException(status_code=404, detail= "Order Not Found")
    
    return order

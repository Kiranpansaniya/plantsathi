from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey,Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///./plants.db", connect_args={"check_same_thread": False})

Base = declarative_base()

class Customer(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")
    is_admin = Column(Boolean,default= False)

class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    description = Column(String, default="")
    image_url = Column(String, default="")

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    quantity = Column(Integer, default=1)

    user = relationship("Customer", back_populates="cart_items")
    plant = relationship("Plant")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, default="Confirmed")

    user = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    plant = relationship("Plant")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
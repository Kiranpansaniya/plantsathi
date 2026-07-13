from pydantic import BaseModel

class PlantCreate(BaseModel):
    name : str
    category : str
    price : float
    stock : int
    description : str = ""
    image_url : str = ""

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

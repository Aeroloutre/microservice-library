from pydantic import BaseModel, ConfigDict

# Recu lors de la creation
class BookCreate(BaseModel):
    title: str
    author: str

# Stocké en bdd
class Book(BaseModel):
    id: int
    title: str
    author: str
    available: bool

# Reponse API
class BookRead(BaseModel):
    id: int
    title: str
    author: str
    available: bool

model_config = ConfigDict(from_attributes=True)
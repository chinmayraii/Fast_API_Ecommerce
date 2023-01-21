from typing import List,Optional
import uuid
from pydantic import BaseModel

class categoryitem(BaseModel):
    name:str
    description:str


class subcategoryitem(BaseModel):
    category_id:int
    name:str
    description:str    

class productitem(BaseModel):
    subcategory_id:int
    product_name:str
    brand:str
    selling_price:int
    discount_price:int
    description:str       
from typing import List,Optional
import uuid
from pydantic import BaseModel

class categoryitem(BaseModel):
    name:str
    description:str

class categoryupdate(BaseModel):
    id:int
    name:str
    description:str

class categorydelete(BaseModel):
    category_id:int    

class subcategoryitem(BaseModel):
    category_id:int
    name:str
    description:str 

class subcategory_update(BaseModel):
    id:int
    category_id:int
    name:str
    description:str  

class subcategorydelete(BaseModel):
    subcategory_id:int            

class productitem(BaseModel):
    category_id:int
    subcategory_id:int
    product_name:str
    brand:str
    selling_price:int
    discount_price:int
    description:str  

class productitem_update(BaseModel):
    id:int
    category_id:int
    subcategory_id:int
    product_name:str
    brand:str
    selling_price:int
    discount_price:int
    description:str  

class UserAdmin(BaseModel):
    email:str
    Full_name:str
    mobile:str
    password:str

# use for login token
class Token(BaseModel):
    access_token:str
    token_type:str='bearer' 

class AdminLogin(BaseModel):
    email:str
    password:str                   
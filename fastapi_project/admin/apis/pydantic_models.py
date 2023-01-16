from typing import List,Optional
import uuid
from pydantic import BaseModel

class categoryitem(BaseModel):
    name:str
    description:str
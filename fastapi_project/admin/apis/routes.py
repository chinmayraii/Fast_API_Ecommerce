from .models import *
from fastapi.responses import JSONResponse
from fastapi import APIRouter,Depends,UploadFile,File
from admin.apis.pydantic_models import categoryitem
import os
from slugify import slugify
from datetime import datetime
from configs import appinfo
from functools import lru_cache

# @lru_cache()
# def app_setting():
#     return appinfo.Setting()

# settings=app_setting()
# app_url=settings.app_url    


router=APIRouter()

@router.post('/category/')
async def create_category(data: categoryitem=Depends(),category_image:UploadFile=File(...)):
    if await Category.exists(name=data.name):
        return{"status":False,"message":"category already exists"}
    else:
        slug=slugify(data.name)

        FILEPATH='static/images/category'

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename=category_image.filename
        extention=filename.split(".")[1]
        imagename=filename.split(".")[0] 

        if extention not in ['png','jpg','jpeg']:
            return {'status':'error',"details":'file extension not allowed'}

        dt=datetime.now()
        dt_timestamp=round(datetime.timestamp(dt))

        modified_image_name=imagename+" "+str(dt_timestamp)+" "+extention
        generated_name=FILEPATH+modified_image_name
        file_content=await category_image.read()

        with open(generated_name,"wb") as file:
            file.write(file_content) 
            file.close()
        # image_url=app_url+generated_name

        category_obj=await Category.create(
            category_image=generated_name,
            description=data.description,
            name=data.name,
            slug=slug
        )

        if category_obj:
            return {"status":True,"message":" category added"}
        else:
            return {"status":False,"message":" something wrong"}       
                       

@router.get('/categoryall/')
async def get_category():
    category_obj = await Category.all()
    return category_obj

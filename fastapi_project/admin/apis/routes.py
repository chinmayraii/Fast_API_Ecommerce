from .models import Category, SubCategory,Product
from fastapi.responses import JSONResponse
from fastapi import APIRouter,Depends,UploadFile,File
from admin.apis.pydantic_models import categoryitem,subcategoryitem,productitem
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

@router.post('/subcategory/')
async def create_subcategory(data: subcategoryitem = Depends(), subcategory_image: UploadFile = File(...)):
    if await Category.exists(id=data.category_id):
        category_obj = await Category.get(id=data.category_id)

        if await SubCategory.exists(name=data.name):
            return{"status": False, "message": "subcategory already exists"}
        else:
            slug = slugify(data.name)

            FILEPATH = "static/images/subcategory"

            if not os.path.isdir(FILEPATH):
                os.mkdir(FILEPATH)

            filename = subcategory_image.filename
            extension = filename.split(".")[1]
            imagename = filename.split(".")[0]

            if extension not in ['png', 'jpg', 'jpeg']:
                return {"status": "error", "detail": "file extension not allowed"}

            dt = datetime.now()
            dt_timestamp = round(datetime.timestamp(dt))

            modified_image_name = imagename+"_"+str(dt_timestamp)+" "+extension
            generated_name = FILEPATH+modified_image_name

            file_content = await subcategory_image.read()

            with open(generated_name, "wb") as file:
                file.write(file_content)
                file.close()
            # image_url = generated_name

            subcategory_obj = await SubCategory.create(
                subcategory_image=generated_name,
                description=data.description,
                category = category_obj,
                name=data.name,
                slug=slug
            )

            if subcategory_obj:
                return{"status": True, "message": "sub category added"}
            else:
                return{"status": False, "message": "something wrong"}

@router.post('/product/')
async def create_product(data: productitem=Depends(),product_image:UploadFile=File(...)):
    if await Category.exists(id=data.category_id):
            category_obj = await Category.get(id=data.category_id)

            if await SubCategory.exists(id=data.subcategory_id):
                subcat_obj = await SubCategory.get(id=data.subcategory_id)
                    

                if await Product.exists(product_name=data.product_name):
                    return{"status":False,"message":"Product already exists"}
                else:
                    slug=slugify(data.product_name)

                    FILEPATH='static/images/product'

                    if not os.path.isdir(FILEPATH):
                        os.mkdir(FILEPATH)

                    filename=product_image.filename
                    extention=filename.split(".")[1]
                    imagename=filename.split(".")[0] 

                    if extention not in ['png','jpg','jpeg']:
                        return {'status':'error',"details":'file extension not allowed'}

                    dt=datetime.now()
                    dt_timestamp=round(datetime.timestamp(dt))

                    modified_image_name=imagename+"_"+str(dt_timestamp)+"."+extention
                    generated_name=FILEPATH+modified_image_name
                    file_content=await product_image.read()

                    with open(generated_name,"wb") as file:
                        file.write(file_content) 
                        file.close()
                    # image_url=app_url+generated_name

                    product_obj=await Product.create(
                        category_image=generated_name,
                        product_name=data.product_name,
                        brand=data.brand,
                        selling_price=data.selling_price,
                        discount_price=data.discount_price,
                        description=data.description,
                        category=category_obj,
                        SubCategory=subcat_obj,
                        slug=slug,
                    )

                    if product_obj:
                        return {"status":True,"message":" product added"}
                    else:
                        return {"status":False,"message":" something wrong"} 
            
                        
                        


   
   
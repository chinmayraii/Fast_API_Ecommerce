from .models import Category, SubCategory,Product,Admin
from fastapi.responses import JSONResponse
from fastapi import APIRouter,Depends,UploadFile,File
from admin.apis.pydantic_models import *
import os
from slugify import slugify
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from fastapi_login import LoginManager
from fastapi.encoders import jsonable_encoder
import json
import jwt
from passlib.context import CryptContext

from configs import appinfo
from functools import lru_cache

# @lru_cache()
# def app_setting():
#     return appinfo.Setting()

# settings=app_setting()
# app_url=settings.app_url    



SECRET='your-secret-key'
router=APIRouter()
manager=LoginManager(SECRET,token_url='/admin_login/')
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

def verify_password(plane_password,hashed_password):
    return pwd_context.verify(plane_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@manager.user_loader()
async def load_user(email:str):
    if await Admin.exists(email=email):
        user=await Admin.get(email=email)
        return user 

@router.post('/admin_login/')
async def login(data:AdminLogin):
    print(data.email)
    email=data.email
    user=await load_user(email)

    if not user:
        return JSONResponse({'status':False,'message':'user not registered'},status_code=403)         
    elif not verify_password(data.password,user.password):
        return JSONResponse({'status':False,'message':'invalid password'},status_code=403)         
    access_token=manager.create_access_token(data={'sub':jsonable_encoder(user.email),'Full_name':jsonable_encoder(user.Full_name),'mobile':jsonable_encoder(user.mobile)})
    new_dict=jsonable_encoder(user)
    new_dict.update({'access_token':access_token})
    res=Token(access_token=access_token,token_type='bearer')
    print(res)
    return res

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

# update all category details

@router.put('/updatecategory/')
async def update_category_details(data: categoryupdate=Depends(),category_image:UploadFile=File(...)):
    if await Category.exists(id=data.id):
        slug=slugify(data.name)

        FILEPATH='static/images/category/'

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

        cat_obj=await Category.filter(id=data.id).update(
            category_image=generated_name,
            description=data.description,
            name=data.name,
            slug=slug
        )

        if cat_obj:
            return {"status":True,"message":" category added"}
        else:
            return {"status":False,"message":" something wrong"} 

@router.delete('/delete_category',)
async def read_item(data:categorydelete):
    delete_category=await Category.filter(id=data.category_id).delete()
    return{'message':'category deleted sucessfully'}                
                       

@router.get('/categoryall/')
async def get_category():
    category_obj = await Category.all()
    return category_obj

@router.get('/subcategoryall/')
async def get_category():
    subcategory_obj = await SubCategory.all()
    return subcategory_obj    

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

@router.put('/subcategory_update/')
async def update_subcategory_details(data: subcategory_update=Depends(),category_image:UploadFile=File(...)):
    if await SubCategory.exists(id=data.id):
        category=await Category.get(id=data.category_id)
        slug=slugify(data.name)

        FILEPATH='static/images/category/'

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

        subcat_obj=await SubCategory.filter(id=data.id).update(
            subcategory_image=generated_name,
            category=category,
            description=data.description,
            name=data.name,
            slug=slug
        )

        if subcat_obj:
            return {"status":True,"message":" subcategory added"}
        else:
            return {"status":False,"message":" something wrong"}  


@router.delete('/delete_subcategory',)
async def read_item(data:subcategorydelete):
    delete_category=await SubCategory.filter(id=data.subcategory_id).delete()
    return{'message':'subcategory deleted sucessfully'}                           

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

@router.put('/updateproduct/')
async def update_category_details(data: productitem_update=Depends(),product_image:UploadFile=File(...)):
    if await Product.exists(id=data.id):
        category=await Category.get(id=data.category_id)
        subcategory=await SubCategory.get(id=data.subcategory_id)
        slug=data.product_name

        FILEPATH='static/images/category/'

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename=product_image.filename
        extention=filename.split(".")[1]
        imagename=filename.split(".")[0] 

        if extention not in ['png','jpg','jpeg']:
            return {'status':'error',"details":'file extension not allowed'}

        dt=datetime.now()
        dt_timestamp=round(datetime.timestamp(dt))

        modified_image_name=imagename+" "+str(dt_timestamp)+" "+extention
        generated_name=FILEPATH+modified_image_name
        file_content=await product_image.read()

        with open(generated_name,"wb") as file:
            file.write(file_content) 
            file.close()
        # image_url=app_url+generated_name

        cat_obj=await Product.filter(id=data.id).update(
            product_image=generated_name,
            product_name=data.product_name,
            description=data.description,
            category=category,
            subcategory=subcategory,
            brand=data.brand,
            selling_price=data.selling_price,
            discount_price=data.discount_price,
            slug=slug
        )

        if cat_obj:
            return {"status":True,"message":" product added"}
        else:
            return {"status":False,"message":" something wrong"} 

@router.post('/admin_registration/')    
async def create_admin(data:UserAdmin):
        try: 
            valid=validate_email(data.email)
        except EmailNotValidError as e:
            return{'status':False,"message":'Invalid email id'}
        if len(data.mobile) !=10:
            return{'status':False,"message":'Invalid number'}                
            
        if await Admin.exists(mobile=data.mobile):
            return{'status':False,"message":'This number already registered'}
        elif await Admin.exists(email=data.email):
            return{'status':False,"message":'email id already registered'}
        else:
            add_user=await Admin.create(email=data.email,Full_name=data.Full_name,mobile=data.mobile,password=get_password_hash(data.password))
            return JSONResponse({
                'status':True,
                'message':'registered sucessfully'
            })            
            
            
                        
                        


   
   
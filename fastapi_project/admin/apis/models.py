from fastapi import FastAPI
from tortoise.models import Model
from tortoise import Tortoise,fields


class Category(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(200, unique=True)
    slug=fields.CharField(200)
    category_image=fields.TextField()
    description=fields.TextField()
    is_active=fields.BooleanField(default=True)
    updated_at=fields.DatetimeField(auto_now=True)
    created_at=fields.DatetimeField(auto_now=True)

class SubCategory(Model):
    id= fields.IntField(pk=True)
    name=fields.CharField(200, unique=True)
    slug = fields.CharField(200)
    subcategory_image= fields.TextField()
    description = fields.TextField()
    category=fields.ForeignKeyField("models.Category" ,related_name="subcategory", on_delete="CASCADE")
    is_active= fields.BooleanField(defualt=True,null=True)
    updated_at= fields.DatetimeField(auto_now=True)
    create_at = fields.DatetimeField(auto_now_add=True)

class Product(Model):
    id=fields.IntField(pk=True)
    product_name=fields.CharField(200,unique=True)
    brand= fields.CharField(300)
    selling_price= fields.IntField()
    discount_price=fields.IntField()
    description=fields.CharField(300)
    is_active= fields.BooleanField(defualt=True,null=True)
    updated_at= fields.DatetimeField(auto_now=True)
    create_at = fields.DatetimeField(auto_now_add=True)
# from django.db import models
# from django.db.models.signals import post_delete
# from django.dispatch import receiver

# # Create your models here.


# class Category(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(
#         verbose_name="Category Name",
#         unique=True,
#         max_length=50,
#     )
#     slug = models.SlugField(
#         verbose_name="Category Slug",
#         unique=True,
#         editable=False,
#         max_length=50,
#     )

#     def __str__(self):
#         return self.name


# class Item(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(
#         verbose_name="Item Name",
#         max_length=50
#     )
#     sku = models.CharField(
#         verbose_name="SKU",
#         unique=True, 
#         max_length=50
#     )
#     slug = models.SlugField(
#         verbose_name="Item Slug",
#         editable=False,
#         max_length=50,
#     )
#     price = models.IntegerField(
#         verbose_name="Price",
#         default=0
#     )
#     description = models.TextField(
#         verbose_name="Description",
#         max_length=1000
#     )
#     category = models.ForeignKey(
#         to=Category,
#         verbose_name="category",
#         on_delete=models.CASCADE
#     )
#     sub_category = models.CharField(
#         verbose_name="sub_category",
#         max_length=50,
#     )
#     recordedAt = models.DateTimeField(
#         verbose_name="recordedAt",
#         auto_now_add=True
#     )
#     updatedAt = models.DateTimeField(verbose_name="updatedAt", auto_now=True)

#     def __str__(self):
#         return self.name


# class Stock(models.Model):
#     id = models.AutoField(primary_key=True)
#     item = models.OneToOneField(
#         to='Item',
#         on_delete=models.CASCADE,
#         verbose_name='Item'
#     )
#     name = models.CharField(
#         verbose_name="Name",
#         max_length=50
#     )
#     sku = models.CharField(
#         verbose_name="SKU",
#         unique=True, max_length=50
#     )
#     slug = models.SlugField(
#         verbose_name="Stock Slug",
#         # unique=True,
#         editable=False,
#         max_length=50,
#     )
#     qty_in_stock = models.IntegerField(default=0)
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.item.name} - {self.qty_in_stock} in stock"


# @receiver(signal=post_delete, sender=Item)
# def delete_category_if_no_items_left(sender, instance, **kwargs):
#     category = instance.category

#     if not category.item_set.exists():
#         category.delete()

from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.


class Category(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(
        verbose_name="Category Name",
        unique=True,
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name="Category Slug",
        unique=True,
        editable=False,
        max_length=50,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(
        verbose_name="SubCategory Name",
        unique=True,
        max_length=50
    )
    slug = models.SlugField(
        verbose_name="SubCategory Slug",
        unique=True,
        editable=False,
        max_length=50,
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name="category",
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(
        verbose_name="Item Name",
        max_length=50
    )
    sku = models.CharField(
        verbose_name="SKU",
        unique=True, 
        max_length=50
    )
    slug = models.SlugField(
        verbose_name="Item Slug",
        unique=True,
        editable=False,
        max_length=50,
    )
    price = models.PositiveIntegerField(
        verbose_name="Price",
        default=0
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=1000
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name="category",
        on_delete=models.CASCADE
    )
    sub_category = models.ForeignKey(
        to=SubCategory,
        verbose_name="sub_category",
        on_delete=models.CASCADE
    )
    recordedAt = models.DateTimeField(
        verbose_name="recordedAt",
        auto_now_add=True
    )
    updatedAt = models.DateTimeField(
        verbose_name="updatedAt",
        auto_now=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sku)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Stock(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    item = models.OneToOneField(
        to='Item',
        on_delete=models.CASCADE,
        verbose_name='Item'
    )
    qty_in_stock = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.qty_in_stock} in stock"


# class Supplier(models.Model):
#     id = models.AutoField(verbose_name="ID", primary_key=True)
#     name_of_person = models.CharField(
#         verbose_name="Person Name",
#         max_length=50
#     )
#     item = models.OneToOneField(
#         to='Item',
#         verbose_name="Item Name",
#         on_delete=models.CASCADE
#     )
#     email = models.EmailField(
#         verbose_name="Email",
#         max_length=100
#     )
#     phone_num = models.BigIntegerField(verbose_name="Phone Number", default=0)
#     qty_supplied = models.PositiveIntegerField(default=0)
#     last_updated = models.DateTimeField(auto_now=True)


#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.sku)
#         return super().save(*args, **kwargs)
    
    
#     def save(self, *args, **kwargs):
#         # Get the stock for the corresponding item
#         try:
#             stock = Stock.objects.get(item__name=self.name_of_item)
            
#             # Check if enough stock is available
#             if stock.qty_in_stock >= self.qty_supplied:
#                 # Reduce the stock quantity
#                 stock.qty_in_stock -= self.qty_supplied
#                 stock.save()  # Save the updated stock value
#             else:
#                 raise ValueError("Insufficient stock available.")

#         except Stock.DoesNotExist:
#             raise ValueError(f"No stock available for {self.name_of_item}")

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.qty_supplied} of {self.name_of_item} supplied."

    
# class Supply(models.Model):
#     id = models.AutoField(verbose_name="ID", primary_key=True)
#     item = models.OneToOneField(
#         to='Item',
#         on_delete=models.CASCADE,
#         verbose_name='Item'
#     )
#     qty_supplied = models.PositiveIntegerField(default=0)
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.item.name} - {self.qty_in_stock} in stock"
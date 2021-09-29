from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.

class Carousel(models.Model):
    image1 = models.ImageField(upload_to="uploads/carouselimages",default="")
    image2 = models.ImageField(upload_to="uploads/carouselimages",default="")
    image3 = models.ImageField(upload_to="uploads/carouselimages",default="")
class Brand(models.Model):
    name = models.CharField(max_length=200,default="")
    image = models.ImageField(upload_to="uploads/brands",default="")

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200,default="")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class ChildCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default="")
    name = models.CharField(max_length=200,default="")

    class Meta:
        verbose_name_plural = "childcategories"

    def __str__(self):
        return self.name


class Business(models.Model):
    firmname = models.CharField(max_length=300)
    gstin = models.CharField(max_length=300,unique=True)
    city = models.CharField(max_length=200,default="")
    ownername = models.CharField(max_length=200)
    contact = models.PositiveIntegerField(default=+91)
    ownerphoto = models.ImageField(upload_to="uploads/owners")
    firmphoto = models.ImageField(upload_to="uploads/firms")
    billphoto = models.ImageField(upload_to="uploads/bills")
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.firmname


class Product(models.Model):
    name = models.CharField(max_length=200,default="")
    description = models.TextField(max_length=255)
    image1 = models.ImageField(upload_to="uploads/products")
    image2 = models.ImageField(upload_to="uploads/products",null=True,blank=True)
    image3 = models.ImageField(upload_to="uploads/products",null=True,blank=True)
    image4 = models.ImageField(upload_to="uploads/products",null=True,blank=True)
    image5 = models.ImageField(upload_to="uploads/products",null=True,blank=True)
    image6 = models.ImageField(upload_to="uploads/products",null=True,blank=True)
    image7 = models.ImageField(upload_to="uploads/products",null=True,blank=True)
    price = models.PositiveIntegerField(default=0)
    pricefor = models.CharField(max_length=300,default="")
    minimumquantity = models.PositiveIntegerField(default=10)
    firmname = models.CharField(max_length=200,default="")
    gstin = models.CharField(max_length=100,default="")
    discount = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    childcategory = models.ForeignKey(ChildCategory,on_delete=models.CASCADE,null=True,blank=True)
    is_available = models.BooleanField(default=False)
    onboard_status = [
        ('under review','under review'),
        (' Congratulations,onboarded','onboarded')
    ]
    status = models.CharField(choices=onboard_status,max_length=100,default="under review")

    @staticmethod
    def product_by_categories(category_id):
        if category_id:
            return Product.objects.filter(category=category_id,is_available=True)
        else:
            return Product.objects.filter(is_available=True)    

    def product_by_childcategories(childcategory_id):
        if childcategory_id:
            return Product.objects.filter(childcategory=childcategory_id,is_available=True)
        else:
            return Product.objects.filter(is_available=True)    

    def __str__(self):
        return self.name
                
class Ad(models.Model):
    image = models.ImageField(upload_to="uploads/ads")

class Register(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="")
    mobile  = models.PositiveIntegerField(default="")
    address = models.TextField(max_length=2000)
    city = models.CharField(max_length=300)
    pincode = models.IntegerField(default="")
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name

class Contact(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField(default=0)
    message = models.TextField(max_length=5000,default="")

    def __str__(self):
        return self.firstname

class Career(models.Model):
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    vacancies = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)
    company = models.CharField(max_length=200,default="mart")
    jd = models.TextField(max_length=5000,default="")
    contact =  models.PositiveIntegerField(default=7375865792)
    mail = models.EmailField(default="amanvyas200@gmail.com")

    def __str__(self):
        return self.position        

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)

    statuses = [
        ('success','success'),
        ('fail','fail')
    ]        
    status = models.CharField(choices=statuses,max_length=200)
    orderid = models.CharField(max_length=300,default="")
    paymentid = models.CharField(max_length=300,default="")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.first_name

class Userproduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    orderid = models.CharField(max_length=200,default="")
    paymentid = models.CharField(max_length=200,default="")
    totalprice = models.FloatField(default=0)
    delstatus = [
        ('Accepted','Accepted'),
        ('Packed','Packed'),
        ('Shipped','Shipped'),
        ('on the way','on the way'),
        ('delievered','delievered')
    ]

    status = models.CharField(choices=delstatus,max_length=300,default="Accepted")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


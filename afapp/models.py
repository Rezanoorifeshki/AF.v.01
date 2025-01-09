from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal,InvalidOperation
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    zirname=models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',verbose_name='دسته بندی')
    name=models.CharField(max_length=50,verbose_name='نام محصول')
    zirname=models.CharField(max_length=50,verbose_name='محصول نول دارد؟',blank=True,default='')
    faz=models.CharField(max_length=50,verbose_name='مقدار فاز ')
    flux=models.CharField(max_length=50,blank=True,default='',verbose_name='جریان')
    pol=models.CharField(max_length=50,blank=True,default='',verbose_name='تعداد پل')
    power=models.CharField(max_length=50,verbose_name='قدرت قطع',blank=True,default='')
    isnew=models.BooleanField(default=False,verbose_name='آیا محصول جدید است؟')
    creatat=models.DateTimeField(auto_now_add=True)
    discount=models.BooleanField(default=False,verbose_name='آیا محصول تخفیف دارد؟')
    discountpercentage=models.PositiveIntegerField(default=0,verbose_name='درصد تخفیف چقدر است؟')
    discountutil=models.DateTimeField(blank=True,null=True,verbose_name='مدت زمان تخفیف چفدر است؟')
    price=models.IntegerField(verbose_name='قیمت محصول چقدر است؟')
    discountprice=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True,verbose_name='قیمت محصول بعد از تخفیف')
    codproduct=models.CharField(max_length=50,verbose_name='کد کالا')
    brand=models.CharField(max_length=50,verbose_name='برند کالا')
    image=models.ImageField(upload_to='photo',verbose_name='عکس محصول')
    image2=models.ImageField(upload_to='photo',verbose_name='2عکس محصول',null=True,blank=True)
    sold_count=models.IntegerField(default=0,verbose_name="تعداد فروش")
    imformation=RichTextField(verbose_name='توضیحات بیشتر',null=True,blank=True)
    def isreturn(self):
        return self.isnew and (timezone.now()<= self.creatat + timedelta(hours=24))
    def save(self,*args,**kwargs):
        if self.discount and self.discountpercentage:
            try:
                discountdecimal=Decimal(self.discountpercentage)
                self.discountprice = Decimal(self.price) * (1 - discountdecimal / 100)
            except (InvalidOperation, ValueError) as e:
                self.discountprice = Decimal(self.price)
        if self.discountutil and self.discountutil < timezone.now() :
            self.discount=False
            self.discountpercentage=0
            self.discountprice = self.price
        super().save(*args,**kwargs)
    def get_related_products(self, limit=4):
        return Product.objects.filter(category=self.category).exclude(id=self.id)[:limit]
    def clean(self):
        if self.discount:
            if self.discountpercentage is None:
                raise ValidationError('مقدار درصد تخفیف نباید خالی باشد.')
            if not (0 <= self.discountpercentage <= 100):
                raise ValidationError('درصد تخفیف باید بین ۰ تا ۱۰۰ باشد.')
    def __str__(self):
        return self.name
class Contactus(models.Model): 
    text=models.CharField(max_length=500)
    flname=models.CharField(max_length=50)
    email=models.EmailField()
    def __str__(self):
        return self.flname
class Aboutus(models.Model):
    titell=models.CharField(max_length=50,verbose_name='تیتر اول')
    textt=RichTextField(verbose_name='متن اول')
    titelll=models.CharField(max_length=50,verbose_name='تیتر دوم',blank=True,null=True)
    texttt=RichTextField(verbose_name='متن دوم',blank=True,null=True)
class Addres(models.Model):
    phoone1=models.CharField(max_length=11,verbose_name='شماره تماس')
    phoone2=models.CharField(max_length=11,verbose_name='شماره تماس',blank=True,null=True)
    phoone3=models.CharField(max_length=11,verbose_name='شماره تماس',blank=True,null=True)
    phoone4=models.CharField(max_length=11,verbose_name='شماره تماس',blank=True,null=True)
    email1=models.EmailField(verbose_name='ایمیل')
    email2=models.EmailField(verbose_name='ایمیل',blank=True,null=True)
    email3=models.EmailField(verbose_name='ایمیل',blank=True,null=True)
    adres=RichTextField(verbose_name='نشانی')
    op=models.IntegerField()
    cl=models.IntegerField()
class Subscriber(models.Model):
    phone=models.CharField(max_length=11,unique=True,verbose_name='شماره موبایل')
    creatat=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.phone


from django.db import models
from shop.models import ProductVariants
from django.db.models.signals import post_save
from django.contrib.auth.models import User



class CartItem(models.Model):
    product = models.ForeignKey(ProductVariants,on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    item_total = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        price_item = self.product.get_prices()
        self.item_total = int(price_item) * int(self.qty)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.product.product.name) + ' / ' + str(self.product.color.name) \
            if self.product.color else '' + ' / ' + str(self.product.size) \
            if len(self.product.size) else ''


class Cart(models.Model):

    items = models.ManyToManyField(CartItem,blank=True)
    cart_total = models.IntegerField(default=0)


    def __str__(self):
        return str(self.id)



class State(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Մարզեր'
        verbose_name_plural='Մարզեր'
    
class City(models.Model):
    
    state = models.ForeignKey(State,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name='Քաղաք/գյուղ'
        verbose_name_plural='Քաղաք/գյուղ'


class PaymentTypes(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Վճարային համակարգեր'
        verbose_name_plural='Վճարային համակարգեր'

    def __str__(self):
        return self.name

class PaymentTypeIcons(models.Model):

    payment = models.ForeignKey(PaymentTypes,on_delete=models.CASCADE,blank=True,null=True)
    icon = models.FileField(upload_to='payment_icons')

    def __str__(self) -> str:
        return self.payment.name
    

class OrderStatuses(models.Model):
    
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Պատվերի կարգավիճակներ'
        verbose_name_plural='Պատվերի կարգավիճակներ'

    def __str__(self):
        return self.name

class Order(models.Model):

    """ Պատվեր """

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    payments = models.ForeignKey(PaymentTypes,on_delete=models.SET_NULL,null=True,blank=True)
    order_status = models.ForeignKey(OrderStatuses,on_delete=models.SET_NULL,null=True,blank=True)
    total_price = models.PositiveIntegerField(default=0,blank=True,null=True)
    all_total_price = models.PositiveIntegerField(default=0,blank=True,null=True)
    order_id_ecc = models.CharField(max_length=80,blank=True,null=True)
    order_status_code = models.CharField(max_length=80,blank=True,null=True)
    session_key =models.CharField(max_length=50,blank=True,null=True)
    name = models.CharField(max_length=60,blank=True)
    phone = models.CharField(max_length=32,blank=True)
    email = models.EmailField(blank=True)
    delivery_price = models.PositiveIntegerField(default=0,null=True,blank=True)
    comments = models.TextField(blank=True)
    state_name = models.ForeignKey(State,on_delete=models.SET_NULL,null=True,blank=True)
    city_name = models.ForeignKey(City,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=150,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):

        return f"{self.first_name} {self.last_name} - {self.all_total_price}"
        
    class Meta:
        ordering = ['-id']
        verbose_name='Պատվերներ'
        verbose_name_plural='Պատվերներ'

class ProductInOrder(models.Model):

    """ Պատվերում գտնվող ապրանք """

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=120,blank=True)
    product_price = models.PositiveIntegerField(default=0,blank=True)
    product_image = models.ImageField(blank=True)
    item_total_price = models.PositiveIntegerField(default=0,blank=True)
    qty = models.PositiveIntegerField(default=0,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def save(self,*args,**kwargs):
        price_per_item = self.product.get_prices()
        self.product_price = price_per_item
        self.product_name = self.product.product.name
        self.product_image = self.product.productvariantimages_set.first().image
       
        super().save(*args,**kwargs)


    def __str__(self):
        
        if self.product and self.product.product.name is None:
            return self.product_name
        else:
            return self.product_name

        
def post_save_order_total_price(sender,instance,*args,**kwargs):
     product_in_order = instance

     products = ProductInOrder.objects.all().filter(order=product_in_order.order)

     total_counter = 0
     for item in products:
         total_counter += item.item_total_price
     product_in_order.order.total_price = total_counter
     product_in_order.order.save()


post_save.connect(post_save_order_total_price,sender=ProductInOrder)





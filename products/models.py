from django.core.urlresolvers import reverse 
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime
from datetime import datetime
# Create your models here.

class ProductManager (models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

class Document(models.Model):
    title  = models.CharField(max_length=120)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    #description = models.Textarea()


class Product1(models.Model):
    title  = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)
    objects = ProductManager()
    quantity = models.IntegerField(default=0)
    zip_Code = models.CharField(blank = True, max_length=6)
    address = models.CharField(default=False, max_length=60)
    date_created = models.DateTimeField(default=timezone.now)
    date_Update = models.DateTimeField(blank=True, null=True)
    expire_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return (self.title)
    def get_absolute_url(self):
        return reverse("product_detail", kwargs = {"pk": self.pk})


def upload_to(instance, filename):
    return '/'.join(['products', unicode(instance.pk), filename])


class Product(models.Model):
    user = models.ForeignKey(User)
    title  = models.CharField(max_length=120)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    #description = models.CharField(max_length=120)
    description = models.CharField(default=False, max_length=160)
    active = models.BooleanField(default=True)
    objects = ProductManager()
    #image = models.ImageField(_("ProductImage"), upload_to=upload_to)
    quantity = models.IntegerField(default=0)
    zip_Code = models.CharField(blank = True, max_length=6)
    address = models.CharField(default=False, max_length=60)
    date_created = models.DateTimeField(default=timezone.now)
    date_Update = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField(blank=True, null=True)
    #expire_date = models.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    #user = models.ForeignKey(User)
    #title = models.ForeignKey(Product)
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("products")
        ordering = ("docfile",)

    def __unicode__(self):
        return self.docfile.path






class Variation(models.Model):
    product = models.ForeignKey(Product)
    title  = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    saleprice = models.DecimalField(decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

def product_post_reciever(sender, instance, created, *args, **kwargs):
        
    product = instance
    variations = product.variation_set.all
    varations = Variation.objects.filter(product=product)
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "default"
        new_var.price = product.price
        new_var.save()
    print sender

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)




#Image rename function
def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)

    return "product/%s/%s" %(slug, new_filename)

#product Image
#class ProductImage(models.Model):
   # product = models.ForeignKey(Product)
    #image = models.ImageField(upload_to=image_upload_to)
    

    #def get_absolute_url(self):
      #  return self.product.title()

class Slider(models.Model):
	image = models.ImageField(upload_to=image_upload_to)
	#image = models.FileField(upload_to=slider_upload)
	order = models.IntegerField(default=0)
	url_link = models.CharField(max_length=250, null=True, blank=True)
	header_text = models.CharField(max_length=120, null=True, blank=True)
	text = models.CharField(max_length=120, null=True, blank=True)
	active = models.BooleanField(default=False)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
	end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

	objects = Product()

	def __unicode__(self):
		return str(self.image)

	class Meta:
		ordering = ['order', '-start_date', '-end_date']

	def get_image_url(self):
		return "%s/%s" %(settings.MEDIA_URL, self.image)

post_save.connect(product_post_reciever, sender=ProductManager)

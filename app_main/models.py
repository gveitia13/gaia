from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.db import models
from django.forms import model_to_dict
from django.utils.safestring import mark_safe

from gaia.settings import STATIC_URL

phone_regex = RegexValidator(
    regex=r'\+?1?\d{9,15}$',
    message='El teléfono debe estar en este formato: +9999999999. Hasta 15 dígitos permitidos.'
)


class Category(models.Model):
    description = models.TextField(verbose_name='Descripción', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    image = models.ImageField(upload_to='product/img', verbose_name='Imagen Principal', null=True)

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        return f'{STATIC_URL}img/empty.png'

    @property
    def get_prods_count(self):
        return self.product_set.count() if self.product_set.exists() else 0

    def img_link(self):
        if self.image:
            return mark_safe(
                f'<a href="{self.image.url}"><img src="{self.image.url}" class="agrandar mb-2 mr-2" '
                f'width="40" height="40" /></a>')
        return mark_safe(
            f'<a href="{STATIC_URL}img/empty.png"><img src="{STATIC_URL}img/empty.png" class="agrandar mb-2 mr-2" '
            f'width="40" height="40" /></a>')

    img_link.short_description = 'Imagen'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/img', verbose_name='Imagen Principal', null=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    price = models.DecimalField(max_digits=9, verbose_name='Precio', decimal_places=2)
    old_price = models.DecimalField(max_digits=9, verbose_name='Precio anterior', decimal_places=2, null=True,
                                    help_text='Este precio debería ser mayor al precio actual', blank=True)
    info = RichTextField(max_length=400, verbose_name='Información', null=True, blank=True)
    about = RichTextField(max_length=400, verbose_name='Sobre el producto', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Visible')
    is_important = models.BooleanField(default=True, verbose_name='Destacado')
    stock = models.IntegerField(verbose_name='Cantidad de inventario', default=1)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    # views = models.PositiveIntegerField(verbose_name='Vistos', default=1)
    sales = models.PositiveIntegerField(verbose_name='Ventas', default=0)
    delivery_time = models.PositiveSmallIntegerField('Tiempo de entrega (días)')

    # stars = models.PositiveIntegerField(verbose_name='Estrellas (1-5)', default=1,
    #                                     validators=[MaxValueValidator(5), MinValueValidator(1)], )

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['image'] = self.get_image()
        item['info'] = self.info_tag()
        item['about'] = self.about_tag()
        item['date_updated'] = self.date_updated.strftime('%d-%m-%Y')
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ('category',)

    def info_tag(self):
        return mark_safe(self.info)

    def about_tag(self):
        return mark_safe(self.about)

    def get_image(self):
        if self.image:
            return self.image.url
        return f'{STATIC_URL}img/empty.png'

    def img_link(self):
        if self.image:
            return mark_safe(
                f'<a href="{self.image.url}"><img src="{self.image.url}" class="agrandar mb-2 mr-2" '
                f'width="50" height="50" /></a>')
        return mark_safe(
            f'<a href="{STATIC_URL}img/empty.png"><img src="{STATIC_URL}img/empty.png" class="agrandar mb-2 mr-2" '
            f'width="50" height="50" /></a>')

    img_link.short_description = 'Vista previa'
    info_tag.short_description = 'Información'


class GeneralData(models.Model):
    logo = models.ImageField(upload_to='datos_generales/logo', verbose_name='Logo')
    img_principal = models.ImageField(upload_to='datos_generales/img_principal', verbose_name='Imagen Principal')
    # banner = models.ImageField(upload_to='datos_generales/banner', verbose_name='Banner', null=True)
    enterprise_name = models.CharField(max_length=100, verbose_name='Nombre de la empresa')
    enterprise_address = models.CharField(max_length=100, verbose_name='Dirección de la empresa', null=True, blank=True)
    email = models.EmailField('Correo', unique=True,
                              error_messages={'unique': 'Este correo ya existe'})
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True, error_messages={
        'unique': 'Ya este teléfono está registrado'
    }, verbose_name='Celular', null=True, blank=True)
    facebook = models.URLField(verbose_name='Link de Facebook', null=True, blank=True)
    instagram = models.URLField(verbose_name='Link de Instagram', null=True, blank=True)

    def __str__(self):
        return self.enterprise_name

    def toJSON(self):
        item = model_to_dict(self)
        item['logo'] = self.logo_tag()
        item['img_principal'] = self.img_principal_tag()
        item['pk'] = self.pk
        return item

    def logo_tag(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" class="agrandar" width="45" height="45" />')
        return mark_safe(f'<img src="{STATIC_URL}img/empty.png" class="agrandar" width="45" height="45" />')

    logo_tag.short_description = 'Logo'

    def logo_link(self):
        return mark_safe(f'<a href="{self.logo.url}"> {self.logo_tag()}</a>')

    logo_link.short_description = 'Logo'

    def img_principal_tag(self):
        if self.logo:
            return mark_safe(f'<img src="{self.img_principal.url}" class="agrandar" height="45" />')
        return mark_safe(f'<img src="{STATIC_URL}img/empty.png" class="agrandar" width="45" height="45" />')

    img_principal_tag.short_description = 'Img principal'

    def img_principal_link(self):
        return mark_safe(f'<a href="{self.img_principal.url}"> {self.img_principal_tag()}</a>')

    img_principal_link.short_description = 'Img principal'

    class Meta:
        verbose_name = 'Datos Generales'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    gnd = models.ForeignKey(GeneralData, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='datos_generales/banner', verbose_name='Banner', null=True)


class Suscriptor(models.Model):
    email = models.EmailField('Correo', unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Suscriptor'
        verbose_name_plural = 'Suscriptores'

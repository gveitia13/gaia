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
    description = models.CharField(max_length=500, verbose_name='Descripción', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    image = models.ImageField(upload_to='product/img', verbose_name='Imagen Principal', null=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        return f'{STATIC_URL}img/empty.png'

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
    # hit_count_generic = GenericRelation(
    #     HitCount, object_id_field='object_pk',
    #     related_query_name='hit_count_generic_relation2')
    # ratings = GenericRelation(Rating, related_query_name='stars_product_generic_relation')
    image = models.ImageField(upload_to='product/img', verbose_name='Imagen Principal', null=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    price = models.DecimalField(max_digits=9, verbose_name='Precio', decimal_places=2)
    old_price = models.DecimalField(max_digits=9, verbose_name='Precio anterior', decimal_places=2, null=True,
                                    help_text='Este precio debería ser mayor al precio actual', blank=True)
    info = RichTextField(max_length=400, verbose_name='Información', null=True, blank=True)
    about = RichTextField(max_length=400, verbose_name='Sobre el producto', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Visible')

    # hidden fields
    # views = models.PositiveIntegerField(verbose_name='Vistos', default=1)
    # sales = models.PositiveIntegerField(verbose_name='Ventas', default=0)
    # stars = models.PositiveIntegerField(verbose_name='Estrellas (1-5)', default=1,
    #                                     validators=[MaxValueValidator(5), MinValueValidator(1)], )

    def __str__(self):
        return self.name

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
                f'width="40" height="40" /></a>')
        return mark_safe(
            f'<a href="{STATIC_URL}img/empty.png"><img src="{STATIC_URL}img/empty.png" class="agrandar mb-2 mr-2" '
            f'width="40" height="40" /></a>')

    img_link.short_description = 'Imagen'
    info_tag.short_description = 'Información'


class GeneralData(models.Model):
    # localization = models.ForeignKey(Localization, on_delete=models.CASCADE, verbose_name='Localización')
    logo = models.ImageField(upload_to='datos_generales/logo', verbose_name='Logo')
    img_principal = models.ImageField(upload_to='datos_generales/img_principal', verbose_name='Imagen Principal')
    enterprise_name = models.CharField(max_length=100, verbose_name='Nombre de la empresa')
    enterprise_address = models.CharField(max_length=100, verbose_name='Dirección de la empresa', null=True, blank=True)
    email = models.EmailField('Correo', unique=True,
                              error_messages={'unique': 'Este correo ya existe'})
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True, error_messages={
        'unique': 'Ya este teléfono está registrado'
    }, verbose_name='Celular', null=True, blank=True)
    # responsables_names = models.CharField(max_length=250, verbose_name='Nombre de los responsables comerciales')
    # google_maps = models.CharField(max_length=900, verbose_name='Mapa de google')
    facebook = models.URLField(verbose_name='Link de Facebook', null=True, blank=True)
    # whatsapp = models.URLField(verbose_name='Link de Whatsapp', null=True, blank=True)
    instagram = models.URLField(verbose_name='Link de Instagram', null=True, blank=True)

    # telegram = models.URLField(verbose_name='Link de Telegram', null=True, blank=True)
    # linked_in = models.URLField(verbose_name='Link de LinkedIn', null=True, blank=True)
    # tiktok = models.URLField(verbose_name='Link de TikTok', null=True, blank=True)
    # views = models.PositiveIntegerField(verbose_name='Vistos', default=0)

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

import uuid as uuid

from ckeditor.fields import RichTextField
from crum import get_current_request
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.forms import model_to_dict
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from gaia.settings import STATIC_URL

phone_regex = RegexValidator(
    regex=r'\+?1?\d{9,15}$',
    message='El teléfono debe estar en este formato: +9999999999. Hasta 15 dígitos permitidos.'
)

colors = (
    ('198754', 'Verde'),
    ('ffc107', 'Amarillo'),
    ('8cbf44', 'Verde Claro'),
    ('fd7e14', 'Anaranjado'),
    ('dc3545', 'Rojo'),
    ('6c757d', 'Gris'),
    ('0d6efd', 'Azul'),
)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    image = models.ImageField(upload_to='product/img', verbose_name='Imagen Principal', null=True, blank=True)
    destacado = models.BooleanField('Destacada', default=False)
    color = models.CharField('Color', max_length=100, choices=colors, default='198754')

    def get_color(self):
        return mark_safe(
            f'<span class="badge text-white rounded-pill" '
            f'style="background-color: #{self.color}">{self.get_color_display()}</span>')

    def get_colores(self):
        html = ''
        print(colors)
        for i in range(len(colors)):
            html += f'<span class="badge mx-1 text-white rounded-pill"style="background-color: #{colors[i][0]}">{colors[i][1]}</span>'
        print(html)
        return mark_safe(html)

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ('name',)

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

    img_link.short_description = 'Vista previa'
    get_color.short_description = 'Color'
    get_colores.short_description = 'Colores disponibles'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/img', verbose_name='Imagen Principal', null=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    price = models.DecimalField(max_digits=9, verbose_name='Precio', decimal_places=2, help_text='Poner en base a CUP')
    old_price = models.DecimalField(max_digits=9, verbose_name='Precio anterior', decimal_places=2, null=True,
                                    help_text='Este precio debería ser mayor al precio actual', blank=True)
    info = RichTextField(max_length=400, verbose_name='Información', null=True, blank=True)
    about = RichTextField(max_length=400, verbose_name='Sobre el producto', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Visible')
    is_important = models.BooleanField(default=True, verbose_name='Destacado')
    stock = models.IntegerField(verbose_name='Cantidad de inventario', default=1)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    sales = models.PositiveIntegerField(verbose_name='Ventas', default=0)
    delivery_time = models.PositiveSmallIntegerField('Tiempo de entrega (días)')
    moneda = models.CharField('Moneda', choices=(
        ('CUP', 'CUP'),
        ('Euro', 'Euro'),
        ('Ambas', 'Ambas'),
    ), default='CUP', max_length=200)
    codigo = models.CharField('Código', max_length=100, editable=False, null=True, blank=True)

    def __str__(self):
        return self.name

    def calculate_codigo(self):
        cat = f'00{self.category_id}' if self.category.pk < 10 else f'{self.category_id}' if self.category.pk > 99 \
            else f'0{self.category_id}'
        pk = f'00{self.pk}' if self.pk < 10 else f'{self.pk}' if self.pk > 99 else f'0{self.pk}'
        return 'GAIA-' + cat + '-' + pk

    def save(self, *args, **kwargs):
        # self.codigo = self.calculate_codigo()
        return super().save(*args, **kwargs)

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['image'] = self.get_image()
        item['info'] = self.info_tag()
        item['about'] = self.about_tag()
        item['price'] = float(self.get_price())
        item['get_price'] = float(self.get_price())
        # item['old_price'] = float(self.old_price) if self.old_price else ''
        item['old_price'] = self.get_old_price()
        item['get_old_price'] = self.get_old_price()
        item['date_updated'] = self.date_updated.strftime('%d-%m-%Y')
        return item

    def get_price(self):
        request: HttpRequest = get_current_request()
        if request.path.__contains__('Euro'):
            return float(self.price) / float(GeneralData.objects.first().taza_cambio)
        return float(self.price)

    def get_old_price(self):
        if not self.old_price: return ''
        request: HttpRequest = get_current_request()
        if request.path.__contains__('Euro'):
            return float(self.old_price) / GeneralData.objects.first().taza_cambio
        return float(self.old_price)

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

    def has_old_price(self):
        return mark_safe(f'<img src="{STATIC_URL}admin/img/icon-yes.svg" alt="True">') if self.old_price else mark_safe(
            f'<img src="{STATIC_URL}admin/img/icon-no.svg" alt="False">')

    has_old_price.short_description = 'Tiene descuento'
    img_link.short_description = 'Vista previa'
    info_tag.short_description = 'Información'


class GeneralData(models.Model):
    logo = models.ImageField(upload_to='datos_generales/logo', verbose_name='Logo')
    img_principal = models.ImageField(upload_to='datos_generales/img_principal', verbose_name='Imagen Principal')
    enterprise_name = models.CharField(max_length=100, verbose_name='Nombre de la empresa')
    enterprise_address = models.CharField(max_length=100, verbose_name='Dirección de la empresa', null=True, blank=True)
    taza_cambio = models.FloatField('Taza de cambio', validators=[MinValueValidator(0, 'Debe ser mayor que cero')],
                                    help_text='Valor del Euro en CUP')
    tropipay_impuesto = models.FloatField('Impuesto de Tropipay', default=3.45,
                                          help_text='Porciento del total de la orden aumentado',
                                          validators=[MinValueValidator(0, 'Debe ser mayor que cero')])
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

    def __str__(self):
        return 'Banner de ' + self.gnd.__str__()


class Suscriptor(models.Model):
    email = models.EmailField('Correo', unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Suscriptor'
        verbose_name_plural = 'Suscriptores'


class InfoUtil(models.Model):
    title = models.CharField('Título', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Información útil'
        verbose_name_plural = 'Informaciones útiles'

    def __str__(self):
        return self.title


class ContenidoInfo(models.Model):
    text = RichTextField("Contenido", null=True, blank=True)
    image = models.ImageField('Imagen', null=True, blank=True, upload_to='info/')
    info = models.ForeignKey(InfoUtil, on_delete=models.CASCADE)

    def text_tag(self):
        return mark_safe(self.text)

    def __str__(self):
        return 'Contenido de ' + self.info.__str__()

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" alt="" width="80" height="50">')
        else:
            return mark_safe(f'<img src="{STATIC_URL}/img/empty.png" alt="" width="80" height="50">')

    text_tag.short_description = 'Texto'
    image_tag.short_description = 'Vista previa'


class Municipio(models.Model):
    nombre = models.CharField('Nombre', max_length=255)
    precio = models.FloatField(verbose_name='Precio de envío en CUP', )
    precio_euro = models.FloatField('Precio de envío en Euro', )

    def __str__(self):
        return '{}'.format(self.nombre)


class Orden(models.Model):
    link_de_pago = models.CharField(max_length=500, null=True, blank=True)
    total = models.FloatField(default=0, verbose_name='Importe total')
    precio_envio = models.FloatField(default=0, verbose_name='Precio de envío')
    moneda = models.CharField(max_length=255, default='Euro')
    uuid = models.UUIDField(verbose_name='ID', primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField('Estado', choices=(
        ('1', 'Completada'),
        ('2', 'Pendiente'),
        ('3', 'Cancelada'),
    ), max_length=10, default='2')
    date_created = models.DateTimeField('Fecha', auto_now_add=True, )
    # Campos del form
    tiempo_de_entrega = models.PositiveIntegerField('Tiempo de entrega máximo')
    nombre_comprador = models.CharField('Nombre del comprador', max_length=200)
    telefono_comprador = models.CharField('Teléfono del comprador', max_length=200)
    correo = models.EmailField('Correo del comprador')
    nombre_receptor = models.CharField('Nombre del receptor', max_length=200)
    telefono_receptor = models.CharField('Teléfono del receptor', max_length=200)
    municipio = models.CharField('Municipio', max_length=200)
    calle = models.CharField('Calle', max_length=200)
    calle1 = models.CharField('Entre calle 1', max_length=200)
    calle2 = models.CharField('Entre calle 2', max_length=200)
    numero_edificio = models.CharField('Número de edificio', max_length=200)
    reparto = models.CharField('Reparto', max_length=200, null=True, blank=True)
    detalles_direccion = models.CharField('Detalles de dirección', max_length=200, null=True, blank=True)

    def __str__(self):
        return '{}'.format(str(self.uuid))

    def get_total(self):
        return '{:.2f}'.format(self.total)

    def get_componente(self):
        return mark_safe(''.join(['•' + i.__str__() + '<br>' for i in self.componente_orden.all()]))

    def get_cancel_link(self):
        if self.status != '3':
            return mark_safe(
                f'<a href="{reverse_lazy("cancelar", kwargs={"pk": self.pk})}" class="btn btn-danger rounded-pill '
                f'">Cancelar<a/>')
        else:
            return ''

    get_total.short_description = 'Importe total'
    get_cancel_link.short_description = 'Opciones'
    get_componente.short_description = 'Componentes'

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'
        ordering = ('-date_created', '-status',)

    def toJSON(self):
        item = model_to_dict(self)
        item['date_created'] = self.date_created.strftime('%d-%m-%Y')
        item['uuid'] = str(self.uuid)
        item['componentes'] = [i.toJSON() for i in self.componente_orden.all()]
        return item


class ComponenteOrden(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='componente_producto')
    respaldo = models.FloatField()
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='componente_orden')
    cantidad = models.IntegerField()

    def __str__(self):
        return '{}x {} - {} {}'.format(self.cantidad, self.producto.name, '{:.2f}'.format(self.respaldo),
                                       self.orden.moneda)

    def Componente(self):
        return str(self)

    def toJSON(self):
        item = model_to_dict(self, exclude=['orden'])
        return item

    class Meta:
        ordering = ('orden', 'producto')
        verbose_name = 'Componente de orden'
        verbose_name_plural = 'Componentes de ordenes'

def validate_calification(value):
    if value < 0 or value > 5:
        raise ValidationError(message="La calificacion debe estar entre 0 y 5.")

class Opinion(models.Model):
    """Model definition for Opinion."""

    calification = models.PositiveIntegerField("Calificacion",validators=[validate_calification])
    comment = models.TextField("Commentario",null=True)

    class Meta:
        """Meta definition for Opinion."""

        verbose_name = 'Opinion'
        verbose_name_plural = 'Opinions'

    def __str__(self):
        """Unicode representation of Opinion."""
        return f"Cal: {self.calification}"
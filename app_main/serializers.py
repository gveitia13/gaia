from django.utils.safestring import mark_safe
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app_main.models import Orden, ComponenteOrden, GeneralData, InfoUtil, Category, Municipio, Banner, ContenidoInfo, \
    ExtraPaymentMethod

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    info_tag = serializers.SerializerMethodField()
    about_tag = serializers.SerializerMethodField()
    get_image = serializers.SerializerMethodField()
    get_price = serializers.SerializerMethodField()
    get_old_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'category', 'image', 'name', 'price', 'old_price', 'info', 'about', 'is_active', 'is_important', 'stock',
            'date_updated', 'sales', 'delivery_time', 'moneda', 'codigo', 'info_tag', 'about_tag', 'get_image',
            'get_price',
            'get_old_price', 'id', 'productextraimage_set')
        depth = 3

    def get_info_tag(self, obj):
        return obj.info_tag()

    def get_about_tag(self, obj):
        return mark_safe(obj.about)


    def get_get_image(self, obj):
        return obj.get_image()

    def get_get_price(self, obj):
        return obj.get_price()

    def get_get_old_price(self, obj):
        return obj.get_old_price()

class ContenidoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoInfo
        fields = ('text', 'image')

class InfoUtilSerializer(serializers.ModelSerializer):
    contenidoinfo_set = ContenidoInfoSerializer(many=True, read_only=True)

    class Meta:
        model = InfoUtil
        fields = ('pk','title', 'contenidoinfo_set')

    def to_representation(self, instance):
        # Call the superclass method to get the default serialized data
        data = super().to_representation(instance)

        # Check some condition to determine whether to include all fields or just the title
        if len(instance.contenidoinfo_set.all()) > 0:
            if self.context['esential'] == True:
                # Only include the title field
                data = {'title': data['title'], 'id':data['pk']}

            return data

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('id','nombre', 'precio', 'precio_euro', 'visible', 'is_pickup_place')

class CategorySerializer(serializers.ModelSerializer):
    get_image = serializers.SerializerMethodField()
    get_prods_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id','name', 'image', 'destacado', 'get_image', 'get_prods_count')

    def get_get_image(self, obj):
        return obj.get_image()

    def get_get_prods_count(self, obj):
        return obj.get_prods_count

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('banner','id')

class GeneralDataSerializer(serializers.ModelSerializer):
    logo_tag = serializers.SerializerMethodField()
    img_principal_tag = serializers.SerializerMethodField()
    banner_set = BannerSerializer(many=True, read_only=True)

    class Meta:
        model = GeneralData
        fields = (
            'logo', 'img_principal', 'enterprise_name', 'enterprise_address', 'taza_cambio', 'tasa_mlc','tropipay_impuesto',
            'email', 'phone_number', 'facebook', 'instagram', 'meta_tittle', 'meta_description', 'meta_kw',
            'checkout_allowed', 'closed_message', 'logo_tag', 'img_principal_tag', 'banner_set')

    def get_logo_tag(self, obj):
        return obj.logo_tag()

    def get_img_principal_tag(self, obj):
        return obj.img_principal_tag()


class ComponenteOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponenteOrden
        fields = '__all__'


class OrdenSerializer(serializers.ModelSerializer):
    componente_orden = ComponenteOrdenSerializer(many=True, read_only=True)

    class Meta:
        model = Orden
        fields = '__all__'

class ExtraPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraPaymentMethod
        fields = ['pk', 'active', 'name', 'card', 'confirmation_number', 'type']
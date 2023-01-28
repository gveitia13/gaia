from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app_main.models import Orden, ComponenteOrden


class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = '__all__'


class ComponenteOrdenSerializer(serializers.ModelSerializer):
    orden = OrdenSerializer()

    class Meta:
        model = ComponenteOrden
        fields = '__all__'

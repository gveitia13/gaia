from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app_main.models import Orden, ComponenteOrden


class ComponenteOrdenSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComponenteOrden
        fields = '__all__'


class OrdenSerializer(serializers.ModelSerializer):
    componente_orden = ComponenteOrdenSerializer(many=True, read_only=True)

    class Meta:
        model = Orden
        fields = '__all__'

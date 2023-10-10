import hashlib
import uuid

lista = [123, 233, 34, 23, 34, 12]
lista2 = []
diccionario = {}
cant = 0

for i in range(len(lista)):
    j = i + 1
    for j in range(len(lista)):
        if lista[i] == lista[j]:
            cant += 1
            lista2.append(lista[i])
        cant = 0

for i in lista:
    if diccionario.get(i) is not None:
        diccionario[i] += 1
    else:
        diccionario[i] = 1

x = 0
resultado = "x es positivo" if x > 0 else "x es negativo" if x < 0 else "x es cero"
asd = 500
cat = f'00{asd}' if asd < 10 else f'{asd}' if asd > 99 else f'0{asd}'

from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase

from app_main.models import Opinion, validate_calification, ExtraPaymentMethod
from app_main.serializers import OpinionSerializer

class OpinionTest(APITestCase):
    
    def test_validate_calification(self):
        validate_calification(0)
        validate_calification(4)
        validate_calification(5)
        with self.assertRaises(ValidationError):
            validate_calification(-5)
        with self.assertRaises(ValidationError):
            validate_calification(10)
    
    def test_create_opinion(self):
        opinion = Opinion.objects.create(calification=4,comment="test")
        self.assertEqual(opinion,Opinion.objects.all().first())
        
        Opinion.objects.create(calification=5,comment="test")
        Opinion.objects.create(calification=0,comment="test")
        
        with self.assertRaises(Exception):
            Opinion.objects.create(calification=-4,comment="test")
        
        with self.assertRaises(Exception):
            Opinion.objects.create(calification=8,comment="test")
            
    def test_str(self):
        opinion = Opinion.objects.create(calification=4,comment="test")
        self.assertEqual(str(opinion),"Cal: 4")
        
class OpinionSerializerTest(APITestCase):
    def test_is_valid_ok(self):
        data = {'calification': 4, 'comment':'Test'}
        serializer = OpinionSerializer(data=data)
        valid = serializer.is_valid()
        self.assertTrue(valid)
    
    def test_is_valid_without_comment(self):
        data = {'calification': 4}
        serializer = OpinionSerializer(data=data)
        valid = serializer.is_valid()
        self.assertTrue(valid)
    
    def test_is_valid_with_validation_of_calification(self):
        data = {'calification': 10, 'comment':'Test'}
        serializer = OpinionSerializer(data=data)
        valid = serializer.is_valid()
        self.assertFalse(valid)
        
        data = {'calification': -4, 'comment':'Test'}
        serializer = OpinionSerializer(data=data)
        valid = serializer.is_valid()
        self.assertFalse(valid)
    
    def test_is_valid_without_calification(self):
        data = {'comment':'Test'}
        serializer = OpinionSerializer(data=data)
        valid = serializer.is_valid()
        self.assertFalse(valid)

class OpinionViewsetTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        opinion1 = Opinion.objects.create(calification=4,comment="opinion1")
        opinion2 = Opinion.objects.create(calification=4,comment="opinion2")
    
    def test_list(self):
        url = reverse('opinion-list')
        response = self.client.get(url)
        serializer = OpinionSerializer(Opinion.objects.all(),many=True)
        data_excepted = serializer.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data,data_excepted)
        
    def test_retreive(self):
        url = reverse('opinion-detail',args=[1])
        response = self.client.get(url)
        serializer = OpinionSerializer(Opinion.objects.get(pk=1))
        data_excepted = serializer.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data,data_excepted)
        
        url = reverse('opinion-detail',args=[5])
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
        
    def test_create(self):
        url = reverse('opinion-list')
        data = {'calification': 4, 'comment':'Test'}
        response = self.client.post(url,data=data)
        self.assertEqual(response.status_code,201)
        self.assertDictContainsSubset(data,response.data)
        
class ExtraPaymentMethodTest(APITestCase):

    def test_create(self):
        data_ok = {
                "name": "Transferencia en CUP",
                "card": "9205555555555555",
                "confirmation_number": "55555555",
                "type": "cup"
            }
        ExtraPaymentMethod.objects.create(**data_ok)
        with self.assertRaises(Exception):
            data = data_ok.copy()
            data.pop('card')
            obj = ExtraPaymentMethod.objects.create(**data)
            
        with self.assertRaises(Exception):
            data = data_ok.copy()
            data.pop('confirmation_number')
            ExtraPaymentMethod.objects.create(**data)

        data_ok.update({"name": "Transferencia en MLC","type": "mlc"})
        ExtraPaymentMethod.objects.create(**data_ok)
        
        with self.assertRaises(Exception):
            data = data_ok.copy()
            data.pop('card')
            ExtraPaymentMethod.objects.create(**data)
            
        with self.assertRaises(Exception):
            data = data_ok.copy()
            data.pop('confirmation_number')
            ExtraPaymentMethod.objects.create(**data)
        
        data_efectivo = {
            "name": "Efectivo",
            "type": "efectivo"
        }
        ExtraPaymentMethod.objects.create(**data_efectivo)
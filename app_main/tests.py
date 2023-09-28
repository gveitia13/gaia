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

print(lista2)

for i in lista:
    if diccionario.get(i) is not None:
        diccionario[i] += 1
    else:
        diccionario[i] = 1

print(uuid.uuid4())
print(uuid.uuid3(uuid.uuid4(), 'GAIA'))
print(uuid.uuid5(uuid.uuid4(), 'GAIA'))
x = 0
resultado = "x es positivo" if x > 0 else "x es negativo" if x < 0 else "x es cero"
print(resultado)

asd = 500
cat = f'00{asd}' if asd < 10 else f'{asd}' if asd > 99 else f'0{asd}'
print(cat)

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from app_main.models import Opinion, validate_calification
from app_main.serializers import OpinionSerializer

User = get_user_model()

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
        User.objects.create_user(username="test",password="testing1234")
        url = reverse('opinion-list')
        data = {'calification': 4, 'comment':'Test'}
        response = self.client.post(url,data=data)
        self.assertEqual(response.status_code,403)
        
        self.client.login(username="test",password="testing1234")
        response = self.client.post(url,data=data)
        self.assertEqual(response.status_code,201)
        self.assertDictContainsSubset(data,response.data)
from django.db import models
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
# Create your models here.
class EcommerceStore(models.Model):
    def _fetchAssistant(self, endpoint=None):
        try:
            response = requests.get(f"https://fakestoreapi.com{endpoint if endpoint else '/'}")
            return {"status": "success", "data": response.json()}
        except Exception as error:
            raise error

    def getProductById(self, productId):
        return self._fetchAssistant(f"/products/{productId}")

    def getAllCategories(self):
        return self._fetchAssistant("/products/categories?limit=100")

    def getProductsInCategory(self, categoryId):
        return self._fetchAssistant(f"/products/category/{categoryId}?limit=10")

    def generatePDFInvoice(self, order_details, file_path):
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 25)
        c.drawString(100, 100, order_details)
        c.save()
        return

    def generateRandomGeoLocation(self):
        storeLocations = [
            {
                "latitude": 44.985613,
                "longitude": 20.1568773,
                "address": "New Castle",
            },
            {
                "latitude": 36.929749,
                "longitude": 98.480195,
                "address": "Glacier Hill",
            },
            {
                "latitude": 28.91667,
                "longitude": 30.85,
                "address": "Buena Vista",
            },
        ]
        return random.choice(storeLocations)
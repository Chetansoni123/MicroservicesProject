from rest_framework import viewsets, status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, User
import random
from .producer import publish
from django.http import JsonResponse


class ProductViewSet(viewsets.ViewSet):
    def list(self, request): # /api/products
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    def create(self, request): # /api/products
        serializer = ProductSerializer(data=request.data) #pass request data
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED) #serializer.data is in JSON format

    def retrieve(self, request, pk=None): #/api/products/<str:id> (behind scenes, inside  retrieve [get(), patch()])
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):#/api/products/<str:id>
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):#/api/products/<str:id>
        product = Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })


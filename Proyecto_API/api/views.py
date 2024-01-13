from django.shortcuts import render

# Elementos necesarios para que el API REST funcione 
from rest_framework import viewsets
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Importando Serealizadores
from api.serializers import FoodTruckSerializer

# Importando Modelos
from api.models import FoodTruck

class FoodTruckSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FoodTruck.objects.all().order_by('id')
    serializer_class = FoodTruckSerializer


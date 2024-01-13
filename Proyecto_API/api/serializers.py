from rest_framework import serializers
from api.models import FoodTruck

class FoodTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTruck
        fields = ['id','nombre','descripcion']
        extra_kwargs = {'id': {'required': False}}
from rest_framework import serializers
from api.models import FoodTruck, Usuario, Cliente

class FoodTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTruck
        fields = ['id','nombre','descripcion']
        extra_kwargs = {'id': {'required': False}}

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','password','is_superuser','usernames','email','is_staff','is_active','codigo','verificacion','tipo']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id','nombre','apellido','Usuario_id']
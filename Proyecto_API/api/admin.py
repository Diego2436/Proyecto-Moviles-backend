from django.contrib import admin
from .models import FoodTruck, Usuario, Empleado, Pedido, Producto, DetallesPedido

# Register your models here.
admin.site.register(FoodTruck)
admin.site.register(Usuario)
admin.site.register(Empleado)
admin.site.register(Pedido)
admin.site.register(Producto)
admin.site.register(DetallesPedido)
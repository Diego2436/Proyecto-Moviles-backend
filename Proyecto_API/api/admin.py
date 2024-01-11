from django.contrib import admin
from .models import Usuario, Tienda, Pedido, Producto, DetallesPedido

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Tienda)
admin.site.register(Pedido)
admin.site.register(Producto)
admin.site.register(DetallesPedido)
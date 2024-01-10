from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=255, null=True)
    direccion = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    telefono = models.CharField(max_length=15, null=True)
    codigo = models.CharField(max_length=10, null=True)
    verificacion = models.CharField(max_length=3, default='NO')

class Tienda(models.Model):
    nombre = models.CharField(max_length=255, null=True)
    descripcion = models.TextField(null=True)

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fecha_pedido = models.CharField(max_length=30, null=True)
    estado = models.CharField(max_length=20, null=True)
    direccion = models.CharField(max_length=400, null=True)

class Producto(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=255, null=True)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    imagen = models.CharField(max_length=50, null=True)

class DetallesPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField(null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True)
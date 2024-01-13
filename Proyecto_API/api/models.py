from django.db import models

class FoodTruck(models.Model):
    nombre = models.CharField(max_length=255, null=True, default=None)
    descripcion = models.TextField(null=True, default=None)

class Usuario(models.Model):
    email = models.CharField(max_length=100, null=True, default=None)
    password = models.CharField(max_length=50, null=True, default=None)
    codigo = models.CharField(max_length=10, null=True, default=None)
    verificacion = models.CharField(max_length=3, default='NO')
    tipo = models.CharField(max_length=10, default='user')

class Empleado(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    rol = models.CharField(max_length=10, null=True)
    foodtruck = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Pedido(models.Model):
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_pedido = models.CharField(max_length=45, null=True)
    fecha_entrega = models.CharField(max_length=45, null=True)
    fecha_repartidor = models.CharField(max_length=45, null=True)
    estado = models.CharField(max_length=20, null=True)
    direccion = models.CharField(max_length=400, null=True)
    foodtruck = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Producto(models.Model):
    nombre = models.CharField(max_length=255, null=True, default=None)
    descripcion = models.TextField(null=True, default=None)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    imagen = models.CharField(max_length=50, null=True, default=None)
    foodtruck = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)

class DetallesPedido(models.Model):
    cantidad = models.IntegerField(null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Categoria(models.Model):
    categoria = models.CharField(max_length=45, null=True, default=None)
    informacion = models.CharField(max_length=100, null=True, default=None)

class ProductoHasCategoria(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
